import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from PIL import Image
from natsort import natsorted, index_natsorted, order_by_index
from scipy.stats import chi2_contingency

@st.cache_data
def load_csv():
    return pd.read_csv('df_2.csv', index_col=0)
    
def flatten(l):
    return [item for sublist in l for item in sublist]

# Define a custom function to convert strings to lists
def string_to_list(string):
    try:
        return eval(string)
    except:
        return string

def plot_and_layout(fig_data, filter1, filter2, barnorm, horizontal_flag, font_size_factor, color_scale_flag):
    # Natsort by filter2 for legend sorting
    fig_data_natsorted = []

    for k in natsorted(fig_data[filter2].unique()):
        fig_data_natsorted.append(fig_data[fig_data[filter2]==k])
    
    fig_data = pd.concat(fig_data_natsorted, axis=0)
    
    if horizontal_flag:
        if color_scale_flag:
            fig = px.histogram(fig_data,
                       y=filter1, x='counts', color=filter2, barnorm=barnorm, text_auto='.0f', color_discrete_sequence=px.colors.diverging.RdYlBu,
                       width=1000, height=750)
        else:
            fig = px.histogram(fig_data,
                       y=filter1, x='counts', color=filter2, barnorm=barnorm, text_auto='.0f', width=1000, height=750)
    else:
        if color_scale_flag:
            fig = px.histogram(fig_data,
                       x=filter1, y='counts', color=filter2, barnorm=barnorm, text_auto='.0f', color_discrete_sequence=px.colors.diverging.RdYlBu,
                       width=1000, height=750)
        else:
            fig = px.histogram(fig_data,
                       x=filter1, y='counts', color=filter2, barnorm=barnorm, text_auto='.0f', width=1000, height=750)
        
    fig.update_layout(legend=dict(itemwidth=30, title_text='', font_size=int(font_size_factor*25), traceorder='reversed'), margin=dict(l=0, r=0, t=75, b=0),
                      title=dict(text=filter_split(filter2), x=0.5, xanchor='right', y=0.96, font_size=int(font_size_factor*40)),
                      font=dict(size=int(font_size_factor*25)))
    
    fig.update_xaxes(title=filter_split(filter1), titlefont_size=int(font_size_factor*25), tickfont_size=int(font_size_factor*25), categoryarray=natsorted(fig_data[filter1].unique()), categoryorder='array')
    fig.update_yaxes(title='Anzahl', titlefont_size=int(font_size_factor*25), tickfont_size=int(font_size_factor*25), nticks=20, tickmode='auto')
    st.plotly_chart(fig, use_container_width=True)
    
def significance_test(df, filter1, filter2, filter1_items, filter2_items):

    # Führe den Chi-Quadrat-Test für Zusammenhänge durch
    pivot_table = df.pivot(index=filter1, columns=filter2, values='counts').fillna(0)
    chi2_stat, p_val, dof, expected = chi2_contingency(pivot_table)

    # Gib die Testergebnisse aus
    with st.expander('Einzelheiten Signifikanztest'):
        filter1_items = [x for x in filter1_items if x == x] # Drop nan
        filter2_items = [x for x in filter2_items if x == x] # Drop nan
        
        st.text('Beobachtete Häufigkeiten')
        st.dataframe(pd.DataFrame(np.array(pivot_table).astype(int), columns=pivot_table.columns, index=pivot_table.index),  use_container_width=True)
        
        st.text("Chi-Quadrat-Statistik = " + str(chi2_stat))
        st.text("p-Wert = " + str(p_val))
        st.text("Freiheitsgrade = " + str(dof))
        
        st.text("Erwartete Häufigkeiten")
        st.dataframe(pd.DataFrame(np.array(expected).astype(int), columns=pivot_table.columns, index=pivot_table.index),  use_container_width=True)

    # Interpretiere die Ergebnisse
    alpha = 0.05
    
    if p_val < alpha:
        st.text("Es gibt einen signifikanten Zusammenhang zwischen " + filter_split(filter2) + " und " + filter_split(filter1))
        
    else:
        st.text("Es gibt KEINEN signifikanten Zusammenhang zwischen " + filter_split(filter2) + " und " + filter_split(filter1))
        
def filter_split(filter):    
    try:
        if len(filter.split(') ')[0])>7:
            return filter
        else:
            return filter.split(') ')[1]
    except:
        return filter
    
#######################################################################################################################################################
st.set_page_config(layout="wide")

mehrfach = ['5b) Fachlicher Schwerpunkt',
            '6b) Ich arbeite auch am...',
            '12a) Nicht als Arbeitszeit gerechnete und nicht vergütete Arbeitsleistungen am Arbeitsplatz',
            '15b) Wesentliche Verschlechterungen der Arbeitsbedingungen in den letzten 2 Jahren',
            '15c) Wesentliche Verbesserungen der Arbeitsbedingungen in den letzten 2 Jahren',
            '18a) Welche Serviceleistungen des DVE für Angestellte sind Ihnen bekannt?',
            '18b) Welche Serviceleistungen des DVE für Angestellte haben Sie im letzten Jahren genutzt?']

col1, col2 = st.columns(2)
image = Image.open('DVE_logo.png')
col1.image(image)
col2.title('Umfrage 2022:sunglasses:')

df_1 = load_csv()
#st.dataframe(df_1)

col3, col4, col5 = st.columns(3)

# WIDGETS

# Filter #1
unique_columns = df_1.columns.to_list()
filter1 = col3.selectbox('Erster Filter', unique_columns, 1)

if filter1 in mehrfach: col3.markdown('Dieser Filter beinhaltet **:blue[Mehrfachnennungen]**')

# Filter #2
unique_columns = df_1.drop(filter1, axis=1).columns.to_list()
filter2 = col4.selectbox('Zweiter Filter', ['keiner']+unique_columns, 3)
    
if filter2 == 'keiner':
    # Nur Histogramm oder Säulendiagramm von filter1
    if filter1 in mehrfach:
        df_temporary = df_1.copy()

        if df_temporary[filter1].isnull().any():
            df_temporary.loc[df_temporary[filter1].isna(), filter1] = df_temporary.loc[df_temporary[filter1].isna(), filter2].apply(lambda x: ['k.A.'])
            df_temporary[filter1] = df_temporary[filter1].apply(string_to_list)

        else:
            df_temporary[filter1] = df_temporary[filter1].apply(string_to_list)

        unique_filter1_items = list(set(flatten([k for k in df_temporary[filter1]])))
        
        with col3.expander('Kategorien wählen'):
            filter1_items = st.multiselect('Kategorien wählen', natsorted(unique_filter1_items), natsorted(unique_filter1_items), label_visibility='collapsed')
        
        figure_data = [word for word in flatten(df_temporary[filter1].to_list()) if word in filter1_items]
        figure_data = pd.Series(figure_data) 
        
    else:
        with col3.expander('Kategorien wählen'):
            filter1_items = st.multiselect('Kategorien wählen', natsorted(df_1[filter1].dropna().unique()), natsorted(df_1[filter1].dropna().unique()), label_visibility='collapsed')

        figure_data = df_1[df_1[filter1].isin(filter1_items)][filter1]

    font_size_factor = st.number_input('Schriftgröße', min_value=0.5, max_value=2.0, value=0.5, step=0.1, key='57')
    
    col10, col11 = st.columns(2)
    fig = px.histogram(figure_data, text_auto='.0f')

    fig.update_layout(showlegend=False, margin=dict(l=0, r=0, t=75, b=0), title=dict(text=filter_split(filter1), x=0.1, y=0.98, 
                                                                                     font_size=int(font_size_factor*40)), font=dict(size=int(font_size_factor*25)))

    fig.update_xaxes(title=filter_split(filter1), titlefont_size=int(font_size_factor*25), tickfont_size=int(font_size_factor*25), categoryarray=natsorted(filter1_items), categoryorder='array')
    fig.update_yaxes(title='Anzahl', titlefont_size=int(font_size_factor*25), tickfont_size=int(font_size_factor*25), nticks=20, tickmode='auto')
    col10.plotly_chart(fig, use_container_width=True)
    
    pie_chart = px.pie(figure_data.value_counts(), values='count', names=figure_data.value_counts().index)
    pie_chart.update_layout(legend=dict(itemwidth=30, title_text='', font_size=int(font_size_factor*25)), margin=dict(l=0, r=0, t=75, b=0),
                      title=dict(text=filter_split(filter1), x=0.5, xanchor='right', y=0.98, font_size=int(font_size_factor*40)),
                      font=dict(size=int(font_size_factor*25)))
    
    col11.plotly_chart(pie_chart, use_container_width=True)
    
    try:
        histogram = figure_data.value_counts()
        
        try:
            st.dataframe(histogram.rename(filter1), use_container_width=True)
        except:
            st.dataframe(histogram, use_container_width=True)
                         
        histogram = histogram.reset_index()
        #gewichteter_mittelwert = round((histogram['index'] * histogram[filter1]).sum() / histogram[filter1].sum(), 2)
        #st.write(histogram, histogram.index, histogram.reset_index(), histogram[filter1].sum())
        gewichteter_mittelwert = round((histogram[filter1] * histogram['count']).sum() / histogram['count'].sum(), 2)
        st.write('Gewichteter Mittelwert = '+str(gewichteter_mittelwert))
    except:
        pass
###########################################################################################################################################################
else:
    
    with col3.expander('Kategorien wählen'):
        filter1_items = st.multiselect('Kategorien wählen', natsorted(df_1[filter1].dropna().unique()), natsorted(df_1[filter1].dropna().unique()), label_visibility='collapsed')

    if filter2 in mehrfach: col4.markdown('Dieser Filter beinhaltet **:blue[Mehrfachnennungen]**')

    with col4.expander('Kategorien wählen'):

        if filter2 in mehrfach:
            df_temporary = df_1.copy()

            if df_temporary[filter2].isnull().any():
                df_temporary.loc[df_temporary[filter2].isna(), filter2] = df_temporary.loc[df_temporary[filter2].isna(), filter2].apply(lambda x: ['k.A.'])
                df_temporary[filter2] = df_temporary[filter2].apply(string_to_list)

            else:
                df_temporary[filter2] = df_temporary[filter2].apply(string_to_list)
                #st.write(df_temporary[filter2])

            unique_filter2_items = list(set(flatten([k for k in df_temporary[df_temporary[filter1].isin(filter1_items)][filter2]])))
            filter2_items = st.multiselect('Kategorien wählen', natsorted(unique_filter2_items), natsorted(unique_filter2_items), label_visibility='collapsed')

        else:
            filter2_items = st.multiselect('Kategorien wählen', natsorted(df_1[filter2].dropna().unique()), natsorted(df_1[filter2].dropna().unique()), label_visibility='collapsed')

    # Filter #3
    unique_columns = df_1.drop([filter1, filter2], axis=1).columns.to_list()
    filter3 = col5.selectbox('Dritter Filter', unique_columns, 3)

    with col5.expander('Kategorien wählen'):
        filter3_items = st.multiselect('Kategorien wählen', natsorted(df_1[filter3].dropna().unique()), natsorted(df_1[filter3].dropna().unique()), label_visibility='collapsed')

    df_slice_1 = df_1[df_1[filter1].isin(filter1_items)]
    df_slice_2 = df_slice_1[df_slice_1[filter2].isin(filter2_items)]
    df_slice_3 = df_slice_2[df_slice_2[filter3].isin(filter3_items)]

    #########################################################################################################################################################
    # Neuer Ansatz
    if filter2 in mehrfach:

        if df_1[filter2].isnull().any():
            df_1.loc[df_1[filter2].isna(), filter2] = df_1.loc[df_1[filter2].isna(), filter2].apply(lambda x: ['k.A.'])
            df_1[filter2] = df_1[filter2].apply(string_to_list)

        else:
            df_1[filter2] = df_1[filter2].apply(string_to_list)
            #st.write(df_1[filter2])

    # Create slices with filter1 and filter2
    temporary_2 = []

    for ii in filter1_items:
        temporary_3 = df_1[df_1[filter1]==ii]

        if filter2 in mehrfach:
            occurrences = [word for word in flatten([k for k in temporary_3[filter2]]) if word in filter2_items]
            temporary_2.append(pd.Series(occurrences).value_counts().to_frame().assign(filter1=ii))

        else:
            temporary_2.append(pd.Series([k for k in temporary_3[temporary_3[filter2].isin(filter2_items)][filter2]]).value_counts().to_frame().assign(filter1=ii))

    temporary_2 = pd.concat(temporary_2).reset_index().rename(columns={'index': filter2, 'count': 'counts', 'filter1': filter1})

    col6, col7 = st.columns(2)

    with col6:
        #st.write(temporary_2)
        with st.expander('Einstellungen'):
            barnorm = ''
            horizontal_flag = False
            color_scale_flag = False
            if not filter2 in mehrfach:
                if st.checkbox('Prozent', key='1'):
                    barnorm = 'percent'
            if st.checkbox('Horizontal', key='3'):
                horizontal_flag = True
            font_size_factor = st.number_input('Schriftgröße', min_value=0.5, max_value=2.0, value=0.5, step=0.1, key='5')
            if st.checkbox('Farbverlauf', key='10'):
                color_scale_flag = True
                
        plot_and_layout(temporary_2, filter1, filter2, barnorm, horizontal_flag, font_size_factor, color_scale_flag)
        significance_test(temporary_2, filter1, filter2, filter1_items, filter2_items)

    # Create slices with filter2 and filter3
    if filter2 in mehrfach: st.stop()

    with col7:
        fig2_data = df_slice_3[[filter2, filter3]].value_counts().to_frame().rename(columns={'count': 'counts'}).reset_index()
        
        with st.expander('Einstellungen'):
            barnorm = ''
            horizontal_flag = False
            color_scale_flag = False
            if not filter3 in mehrfach:
                if st.checkbox('Prozent', key='2'):
                    barnorm = 'percent'
            if st.checkbox('Horizontal', key='4'):
                horizontal_flag = True
            font_size_factor = st.number_input('Schriftgröße', min_value=0.5, max_value=2.0, value=0.5, step=0.1, key='6')
            if st.checkbox('Farbverlauf', key='11'):
                color_scale_flag = True
        
        plot_and_layout(fig2_data, filter2, filter3, barnorm, horizontal_flag, font_size_factor, color_scale_flag)
        significance_test(fig2_data, filter2, filter3, filter2_items, filter3_items)

    with st.expander('Datensatz'):
        #st.dataframe(df_slice_1, use_container_width=True)
        #st.dataframe(df_slice_2, use_container_width=True)
        st.dataframe(df_slice_3[[filter1, filter2, filter3]], use_container_width=True)
