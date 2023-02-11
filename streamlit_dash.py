import streamlit as st
import pandas as pd

df = pd.read_csv('startup_funding.csv')

st.dataframe(df)
