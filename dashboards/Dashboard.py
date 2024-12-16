import streamlit as st
import pandas as pd
import altair as alt
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
    st.subheader('Traffic Situations Dashboard: Overview')

    # Ladda geocode-mappning
    geocode_mapping = prepare_geocode_mapping()

    # Hämta och förbered trafikdata
    df = query_trafic_situations()
    df.columns = df.columns.str.upper()

    # Lägg till adress och län från mappningen
    def get_address_and_lan_from_mapping(row):
        try:
            lat = float(row['WGS84_POINT_LATITUDE'])
            lon = float(row['WGS84_POINT_LONGITUDE'])
        except (ValueError, TypeError):
            return "Okänd adress", "Okänd län"

        if pd.notna(lat) and pd.notna(lon):
            # Formatera koordinaterna med samma precision som JSON-filen
            cache_key = f"{lat:.7f},{lon:.7f}"
            geo_info = geocode_mapping.get(tuple(map(float, cache_key.split(','))), {"address": "Okänd adress", "lan": "Okänd län"})
            return geo_info["address"], normalize_lan(geo_info["lan"])
        else:
            return "Okänd adress", "Okänd län"


    df[['ADRESS', 'LAN']] = df.apply(lambda row: pd.Series(get_address_and_lan_from_mapping(row)), axis=1)

    # Omvandla datumfält till datetime för filtrering
    df['CREATION_TIME'] = pd.to_datetime(df['CREATION_TIME'])
    df['START_TIME'] = pd.to_datetime(df['START_TIME'])
    df['END_TIME'] = pd.to_datetime(df['END_TIME'])

    # Totalt antal situationer
    total_situations = df.shape[0]
    st.metric("Totalt antal situationer", total_situations)

    # Trafiksituationer från föregående dag
    yesterday = pd.Timestamp.now().normalize() - pd.Timedelta(days=1)
    yesterday_situations = df[df['CREATION_TIME'].dt.date == yesterday.date()]
    st.metric(f"Situationer den {yesterday.strftime('%Y-%m-%d')}", yesterday_situations.shape[0])

    # Mest påverkade län (Top 3)
    lan_counts = df['LAN'].value_counts().head(3).reset_index()
    lan_counts.columns = ['Län', 'Antal situationer']
    st.subheader('Mest påverkade län (Top 3)')
    st.dataframe(lan_counts)

    # Fördelning av allvarlighetsnivåer
    severity_counts = df['SEVERITY_TEXT'].value_counts().reset_index()
    severity_counts.columns = ['Allvarlighetsnivå', 'Antal situationer']

    st.subheader('Fördelning av allvarlighetsnivåer')
    severity_chart = alt.Chart(severity_counts).mark_bar().encode(
        x=alt.X('Antal situationer:Q', title='Antal situationer'),
        y=alt.Y('Allvarlighetsnivå:N', sort='-x', title='Allvarlighetsnivå')
    ).properties(
        width=700,
        height=400
    )
    st.altair_chart(severity_chart)

    # Rullande lista med senaste trafiksituationerna
    st.subheader('Senaste trafiksituationerna')
    recent_situations = df.sort_values(by='CREATION_TIME', ascending=False).head(10)[
        ['CREATION_TIME', 'LAN', 'ROAD_NUMBER', 'SITUATION_TYPE']
    ]
    recent_situations.columns = ['Tid', 'Län', 'Vägnummer', 'Situationstyp']
    st.dataframe(recent_situations)

# Använd layout-funktionen
layout()
