import streamlit as st
import pandas as pd
from helpers.reverse_geocode import reverse_geocode
from helpers.normalize import normalize_lan
from helpers.Connect_and_query import query_trafic_situations

def layout():
    st.set_page_config(layout="wide")
    st.subheader('Traffic Situations Search Dashboard')

    # Hämta och förbered trafikdata
    df = query_trafic_situations()
    df.columns = df.columns.str.upper()

    # Lägg till adress och län baserat på koordinater
    def get_address_and_lan(row):
        lat = row['WGS84_POINT_LATITUDE']
        lon = row['WGS84_POINT_LONGITUDE']
        if pd.notna(lat) and pd.notna(lon):
            geo_info = reverse_geocode(lat, lon)
            return geo_info.get('address', 'Okänd adress'), normalize_lan(geo_info.get('lan', 'Okänd län'))
        else:
            return 'Okänd adress', 'Okänd län'

    df[['ADRESS', 'LAN']] = df.apply(lambda row: pd.Series(get_address_and_lan(row)), axis=1)

    # Sökfunktion
    search_input = st.text_input("Sök efter vägnummer eller vägnamn (ex. '251' eller 'E4'):")

    if search_input:
        # Filtrera data baserat på sökningen
        filtered_df = df[
            (df['ROAD_NUMBER'].astype(str).str.contains(search_input, case=False, na=False)) |
            (df['ROAD_NAME'].str.contains(search_input, case=False, na=False))
        ]

        # Visa resultat om matchningar hittas
        if not filtered_df.empty:
            st.subheader(f"Trafiksituationer för sökning '{search_input}'")

            # Välj kolumner att visa
            display_columns = ['START_TIME', 'END_TIME', 'SITUATION_TYPE', 'ADRESS', 'LAN']
            st.dataframe(filtered_df[display_columns])
        else:
            st.warning(f"Inga resultat hittades för sökning '{search_input}'.")
    else:
        st.info("Ange ett vägnummer eller vägnamn för att börja söka.")

# Använd layout-funktionen
layout()
