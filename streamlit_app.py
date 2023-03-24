import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image
from natsort import natsorted

def flatten(l):
    return [item for sublist in l for item in sublist]

# Define a custom function to convert strings to lists
def string_to_list(string):
    return eval(string)

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

df_1 = pd.read_csv('df_1.csv', index_col=0)

unique_columns = df_1.columns.to_list()

col3, col4 = st.columns(2)

filter1 = col3.selectbox('Erster Filter', unique_columns, 1)

with col3.expander('Kategorien wählen'):
    x_axis_items = st.multiselect('Kategorien wählen', natsorted(df_1[filter1].unique()), natsorted(df_1[filter1].unique()), label_visibility='collapsed')

df_1 = df_1[df_1[filter1].isin(x_axis_items)]

unique_columns = df_1.drop(filter1, axis=1).columns.to_list()
filter2 = col4.selectbox('Zweiter Filter', ['keiner']+unique_columns, 3)


if filter2 == 'keiner':
    fig = px.histogram(df_1[filter1].value_counts().to_frame().rename(columns={filter1: 'counts'}).reset_index(names=filter1), x=filter1, y='counts', barnorm='', text_auto='.1f', width=1000, height=750)
    
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
        barnorm='percent'
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
   "text/csv",
   key='download-csv')
                   
st.dataframe(df_2, use_container_width=True)
st.download_button(
   "Press to Download",
   df_2.to_csv(index=False).encode('utf-8'),
   "file.csv",
   "text/csv",
   key='download-csv')

#except:
#    st.error('Unterschiedliche Achsen wählen', icon="🚨")
#    st.stop()
