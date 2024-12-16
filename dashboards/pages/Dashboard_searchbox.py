import streamlit as st
import pandas as pd
import json
from helpers.normalize import normalize_lan
from helpers.Connect_and_query import query_trafic_situations

@st.cache_data
def prepare_geocode_mapping():
    """Förbered en mappning av koordinater till län och adress baserat på cache."""
    with open("geocode_cache_lan.json", "r") as cache_file:
        geocode_cache = json.load(cache_file)
    # Omvandla nycklar från "latitude,longitude" till tuple (latitude, longitude)
    return {
        tuple(map(float, key.split(','))): value for key, value in geocode_cache.items()
    }

def layout():
    st.set_page_config(layout="wide")
    st.subheader('Traffic Situations Search Dashboard')

    # Ladda geocode-mappning
    geocode_mapping = prepare_geocode_mapping()

    # Hämta och förbered trafikdata
    df = query_trafic_situations()
    df.columns = df.columns.str.upper()

    # Lägg till adress och län från mappningen
    def get_address_and_lan(row):
        try:
            lat = float(row['WGS84_POINT_LATITUDE'])
            lon = float(row['WGS84_POINT_LONGITUDE'])
        except (ValueError, TypeError):
            return "Okänd adress", "Okänd län"

        if pd.notna(lat) and pd.notna(lon):
            # Formatera koordinaterna med samma precision som JSON-filen
            cache_key = (lat, lon)
            geo_info = geocode_mapping.get(cache_key, {"address": "Okänd adress", "lan": "Okänd län"})
            return geo_info["address"], normalize_lan(geo_info["lan"])
        else:
            return "Okänd adress", "Okänd län"

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
