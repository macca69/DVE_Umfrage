import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image

image = Image.open('DVE_logo.png')

st.image(image)

st.title('Umfrage 2022:sunglasses:')

df_1 = pd.read_csv('df_1.csv', index_col=0)

unique_columns = df_1.columns.to_list()
unique_columns = [k for k in unique_columns if 'Mehrfach' not in k]

st.write(unique_columns)

erste_achse = st.selectbox('Erste Achse', unique_columns, 13)

st.write(erste_achse, unique_columns)

zweite_achse = st.selectbox('Zweite Achse', unique_columns.remove(erste_achse), 12)

typ = st.checkbox("Percent", key="disabled")

if typ:
    barnorm='percent'
else:
    barnorm=''

histogram = df_1[[erste_achse, zweite_achse]].value_counts().to_frame('counts').reset_index()
fig = px.histogram(histogram, x=erste_achse, y='counts', color=zweite_achse, barnorm=barnorm, text_auto='.1f', width=1000, height=750)
fig.update_layout(legend=dict(
    orientation="v",
    yanchor="top",
    y=-0.25,
    xanchor="left",
    x=0), margin=dict(l=0, r=0, t=50, b=0))
st.plotly_chart(fig, use_container_width=True)
