import streamlit as st
import pandas as pd
from helpers.Connect_and_query import query_trafic_situations

def layout():
    st.set_page_config(layout="wide")
    st.subheader('Raw Data Dashboard')

    # Hämta trafikdata
    df = query_trafic_situations()
    df.columns = df.columns.str.upper()

    # Visa hela dataframen
    st.write("### Hela rådata från Trafikverket")
    st.dataframe(df)

    # Ge möjlighet att ladda ner rådata som CSV
    csv = df.to_csv(index=False)
    st.download_button(
        label="Ladda ner data som CSV",
        data=csv,
        file_name="raw_data.csv",
        mime="text/csv"
    )

# Använd layout-funktionen
layout()
