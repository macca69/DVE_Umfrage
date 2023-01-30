import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image

col1, col2 = st.columns(2)
image = Image.open('DVE_logo.png')
col1.image(image)

col2.title('Umfrage 2022:sunglasses:')

df_1 = pd.read_csv('df_1.csv', index_col=0)

unique_columns = df_1.columns.to_list()
unique_columns = [k for k in unique_columns if 'Mehrfach' not in k]

erste_achse = st.selectbox('Erste Achse', unique_columns)

#unique_columns.remove(erste_achse)

zweite_achse = st.selectbox('Zweite Achse', unique_columns)

col3, col4 = st.columns(2)
typ = col3.checkbox("Percent")
#swap = col4.checkbox('Achse tauschen')

if typ:
    barnorm='percent'
else:
    barnorm=''
    
try:
    histogram = df_1[[erste_achse, zweite_achse]].value_counts().to_frame('counts').reset_index()
    
    fig = px.histogram(histogram, x=erste_achse, y='counts', color=zweite_achse, barnorm=barnorm, text_auto='.1f', width=1000, height=750)
    fig.update_layout(legend=dict(orientation="v", yanchor="top", y=-0.25, xanchor="left", x=0),
                      margin=dict(l=0, r=0, t=50, b=0))
    
    fig.update_xaxes(title=erste_achse.split(') ')[1])
    fig.update_yaxes(title=zweite_achse.split(') ')[1])
    
    st.plotly_chart(fig, use_container_width=True)

except:
    st.error('Unteschiedliche Achsen wählen', icon="🚨")
    st.stop()
