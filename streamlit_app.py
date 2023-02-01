import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image
from natsort import natsorted

def flatten(l):
    return [item for sublist in l for item in sublist]

mehrfach = ['5b) Fachlicher Schwerpunkt',
            '6b) Ich arbeite auch am...',
            '12a) Nicht als Arbeitszeit gerechnete und nicht vergütete Arbeitsleistungen am Arbeitsplatz',
            '15b) Wesentliche Verschlechterungen der Arbeitsbedingungen in den letzten 2 Jahren',
            '15c) Wesentliche Verbesserungen der Arbeitsbedingungen in den letzten 2 Jahren',
            '18a) Welche Serviceleistungen des DVE für Angestellte sind Ihnen bekannt?',
            '18b) Welche Serviceleistungen des DVE für Angestellte haben Sie im letzten Jahren genutzt?']

#col1, col2 = st.columns(2)
#image = Image.open('DVE_logo.png')
#col1.image(image)
#col2.title('Umfrage 2022:sunglasses:')

df_1 = pd.read_csv('df_1.csv', index_col=0)

unique_columns = df_1.columns.to_list()

filter1 = st.selectbox('Erster Filter', unique_columns, 1)

#unique_columns.remove(erste_achse)

filter2 = st.selectbox('Zweiter Filter', unique_columns, 3)

col3, col4 = st.columns(2)
typ = col3.checkbox("Percent")

if typ:
    barnorm='percent'
else:
    barnorm=''
    
###########

st.write(filter2 in mehrfach)

if filter2 in mehrfach:

    df_2 = []

    for ii in df_1[filter1].unique():
        df_filter1 = df_1[df_1[filter1]==ii]
        df_2.append(pd.Series(flatten([k for k in df_filter1[filter2]])).value_counts().to_frame().assign(filter1=ii))

    df_2 = pd.concat(df_2).reset_index().rename(columns={'index': filter2, 0: 'counts', 'filter1': filter1})
    st.write(df_2)
    fig = px.histogram(df_2, x=filter1, y='counts', color=filter2, barnorm='', text_auto='.1f', width=1000, height=750)

else:
    df_2 = df_1[[filter1, filter2]].value_counts().to_frame('counts').reset_index()
    fig = px.histogram(df_2, x=filter1, y='counts', color=filter2, barnorm=barnorm, text_auto='.1f', width=1000, height=750)
    
fig.update_layout(legend=dict(orientation="v", yanchor="top", y=-0.25, xanchor="left", x=0),
                  margin=dict(l=0, r=0, t=40, b=0))

fig.update_xaxes(title=filter1.split(') ')[1], categoryarray=natsorted(df_1[filter1].unique()), categoryorder='array')
fig.update_yaxes(title='Anzahl '+filter2.split(') ')[1])#, categoryarray=natsorted(histogram[filter2].unique()), categoryorder='array')

st.plotly_chart(fig, use_container_width=True)

#except:
#    st.error('Unterschiedliche Achsen wählen', icon="🚨")
#    st.stop()
