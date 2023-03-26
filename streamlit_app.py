import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image
from natsort import natsorted

#@st.cache_data
def load_csv():
    
    df_1 = pd.read_csv('df_1.csv', index_col=0)
    
    mehrfach = ['5b) Fachlicher Schwerpunkt',
            '6b) Ich arbeite auch am...',
            '12a) Nicht als Arbeitszeit gerechnete und nicht vergütete Arbeitsleistungen am Arbeitsplatz',
            '15b) Wesentliche Verschlechterungen der Arbeitsbedingungen in den letzten 2 Jahren',
            '15c) Wesentliche Verbesserungen der Arbeitsbedingungen in den letzten 2 Jahren',
            '18a) Welche Serviceleistungen des DVE für Angestellte sind Ihnen bekannt?',
            '18b) Welche Serviceleistungen des DVE für Angestellte haben Sie im letzten Jahren genutzt?']
    
    for column in mehrfach:
        try:
            df_1[column] = df_1[column].apply(string_to_list)
        except:
            df_1[column] = df_1[column].fillna({column: ['k.A.']})
            
            df_1[column] = df_1[column].apply(string_to_list)
        
    return mehrfach, df_1
    
def flatten(l):
    return [item for sublist in l for item in sublist]

# Define a custom function to convert strings to lists
def string_to_list(string):
    return eval(string)

def plot_and_layout(fig_data, filter1, filter2, filter_items, barnorm):
    fig = px.histogram(fig_data,
                       x=filter1, y='counts', color=filter2, barnorm=barnorm, text_auto='.0f',
                       width=1000, height=750)

    fig.update_layout(#legend=dict(orientation="v", yanchor="top", y=-0.1, xanchor="left", x=0.15),
                      margin=dict(l=0, r=0, t=75, b=0),
                     title=dict(text=filter2.split(') ')[1], x=0.1, y=0.925, font_size=20),
                     legend_title_text='',
                     legend_font_size=15,
                     font=dict(size=15))
    
    fig.update_xaxes(title=filter1.split(') ')[1], titlefont_size=20, tickfont_size=15, categoryarray=natsorted(filter_items), categoryorder='array')
    
    fig.update_yaxes(title='Anzahl', titlefont_size=20, tickfont_size=15, nticks=20, tickmode='auto')
    
    st.plotly_chart(fig, use_container_width=True)

st.set_page_config(layout="wide")

col1, col2 = st.columns(2)
image = Image.open('DVE_logo.png')
col1.image(image)
col2.title('Umfrage 2022:sunglasses:')

mehrfach, df_1 = load_csv()

st.dataframe(df_1)

col3, col4, col5 = st.columns(3)

unique_columns = df_1.columns.to_list()
filter1 = col3.selectbox('Erster Filter', unique_columns, 1)
with col3.expander('Kategorien wählen'):
    filter1_items = st.multiselect('Kategorien wählen', natsorted(df_1[filter1].unique()), natsorted(df_1[filter1].unique()), label_visibility='collapsed')

unique_columns = df_1.drop(filter1, axis=1).columns.to_list()
filter2 = col4.selectbox('Zweiter Filter', unique_columns, 2)

with col4.expander('Kategorien wählen'):
    filter2_items = st.multiselect('Kategorien wählen', natsorted(df_1[filter2].unique()), natsorted(df_1[filter2].unique()), label_visibility='collapsed')

unique_columns = df_1.drop([filter1, filter2], axis=1).columns.to_list()
filter3 = col5.selectbox('Dritter Filter', unique_columns, 3)
with col5.expander('Kategorien wählen'):
    filter3_items = st.multiselect('Kategorien wählen', natsorted(df_1[filter3].unique()), natsorted(df_1[filter3].unique()), label_visibility='collapsed')

df_slice_1 = df_1[df_1[filter1].isin(filter1_items)]
df_slice_2 = df_slice_1[df_slice_1[filter2].isin(filter2_items)]
df_slice_3 = df_slice_2[df_slice_2[filter3].isin(filter3_items)]

with st.expander('Datensatz'):
    #st.dataframe(df_slice_1, use_container_width=True)
    #st.dataframe(df_slice_2, use_container_width=True)
    st.dataframe(df_slice_3, use_container_width=True)
    
#########################################################

#if filter2 in mehrfach:
#    df_1[filter2] = df_1[filter2].apply(string_to_list)

temporary_2 = []

st.write(filter1_items)

for ii in filter1_items:
    temporary_3 = df_1[df_1[filter1]==ii]
    if filter2 in mehrfach:
        #st.write([k for k in temporary_3[filter2]])
        temporary_2.append(pd.Series(flatten([k for k in temporary_3[filter2]])).value_counts().to_frame().assign(filter1=ii))
    else:
        #st.write([k for k in temporary_3[filter2]])
        temporary_2.append(pd.Series([k for k in temporary_3[filter2]]).value_counts().to_frame().assign(filter1=ii))
        
temporary_2 = pd.concat(temporary_2).reset_index().rename(columns={'index': filter2, 0: 'counts', 'filter1': filter1})
st.write(temporary_2)
plot_and_layout(temporary_2, filter1, filter2, filter1_items, '')
st.stop()
###########################################################    
col6, col7 = st.columns(2)

with col6:
    if st.checkbox("Prozent", key='1'):
        barnorm='percent'
    else:
        barnorm=''

    fig_data = df_slice_2[[filter1, filter2]].value_counts().to_frame().rename(columns={0: 'counts'}).reset_index()
    #fig_data[filter1] = fig_data[filter1].str[:20]
    #fig_data[filter2] = fig_data[filter2].str[:20]
    
    plot_and_layout(fig_data, filter1, filter2, filter1_items, barnorm)
    

with col7:
    if st.checkbox("Prozent", key='2'):
        barnorm='percent'
    else:
        barnorm=''

    fig2_data = df_slice_3[[filter2, filter3]].value_counts().to_frame().rename(columns={0: 'counts'}).reset_index()
    #fig2_data[filter2] = fig2_data[filter2].str[:20]
    #fig2_data[filter3] = fig2_data[filter3].str[:20]
    
    plot_and_layout(fig2_data, filter2, filter3, filter2_items, barnorm)

st.stop()

##################################################################################################################################################
                        
                        
unique_columns = df_1.drop(filter1, axis=1).columns.to_list()
filter2 = col4.selectbox('Zweiter Filter', ['keiner']+unique_columns, 3)
with col4.expander('Kategorien wählen'):
    y_axis_items = st.multiselect('Kategorien wählen', natsorted(df_1[filter1][filter_2].unique()), natsorted(df_1[filter1][filter_2].unique()), label_visibility='collapsed')

if filter2 == 'keiner':
    fig = px.histogram(df_1[filter1][filter2].value_counts().to_frame().rename(columns={filter1: 'counts'}).reset_index(names=filter1), x=filter1, y='counts', barnorm='', text_auto='.1f', width=1000, height=750)
    
elif filter2 in mehrfach:
    
    if st.checkbox("Percent"):
        barnorm='percent'
    else:
        barnorm=''
        
    df_1[filter2] = df_1[filter2].apply(string_to_list)

    df_2 = []

    for ii in df_1[filter1].unique():
        df_filter1 = df_1[df_1[filter1]==ii]
        df_2.append(pd.Series(flatten([k for k in df_filter1[filter2]])).value_counts().to_frame().assign(filter1=ii))

    try:
        df_2 = pd.concat(df_2).reset_index().rename(columns={'index': filter2, 0: 'counts', 'filter1': filter1})
        
    except:
        st.error('Fehler')
        st.stop()
        
    fig = px.histogram(df_2, x=filter1, y='counts', color=filter2, barnorm=barnorm, text_auto='.1f', width=1000, height=750)

else:
    
    if st.checkbox("Percent"):
        barnorm='Prozent'
    else:
        barnorm=''
        
    df_2 = df_1[[filter1, filter2]].value_counts().to_frame('counts').reset_index()
    fig = px.histogram(df_2, x=filter1, y='counts', color=filter2, barnorm=barnorm, text_auto='.1f', width=1000, height=750)
    
fig.update_layout(legend=dict(orientation="v", yanchor="top", y=-0.25, xanchor="left", x=0),
                  margin=dict(l=0, r=0, t=40, b=0))

fig.update_xaxes(title=filter1.split(') ')[1], categoryarray=natsorted(df_1[filter1].unique()), categoryorder='array')
fig.update_yaxes(title='Anzahl')

st.plotly_chart(fig, use_container_width=True)

st.dataframe(df_1, use_container_width=True)
st.download_button(
   "Press to Download",
   df_1.to_csv(index=False).encode('utf-8'),
   "file.csv",
   "text/csv")
                   
st.dataframe(df_2, use_container_width=True)
st.download_button(
   "Press to Download",
   df_2.to_csv(index=False).encode('utf-8'),
   "file_2.csv",
   "text/csv")

#except:
#    st.error('Unterschiedliche Achsen wählen', icon="🚨")
#    st.stop()
