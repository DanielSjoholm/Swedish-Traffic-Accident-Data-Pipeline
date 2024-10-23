import streamlit as st
import pandas as pd
import altair as alt
from Connect_and_query import query_trafic_situations
from geopy.geocoders import GoogleV3
from dotenv import load_dotenv
from helpers.normalize import normalize_lan
from helpers.reverse_geocode import reverse_geocode

# # Ladda API-nyckeln från .env-filen
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# geolocator = GoogleV3(api_key=GOOGLE_API_KEY)

def layout():
    st.set_page_config(layout="wide")
    st.subheader('Traffic Situations Dashboard')

    # Hämta och förbered trafikdata
    df = query_trafic_situations()
    df.columns = df.columns.str.upper()

    # Lägg till länsinformation från cachen eller API:et till dataframe
    def get_lan_from_cache_or_api(row):
        lat = row['WGS84_POINT_LATITUDE']
        lon = row['WGS84_POINT_LONGITUDE']
        return reverse_geocode(lat, lon)['lan'] if pd.notna(lat) and pd.notna(lon) else 'Okänd län'

    df['LAN'] = df.apply(get_lan_from_cache_or_api, axis=1)

    # Normalisera län/County så att de har samma namn
    df['LAN'] = df['LAN'].apply(normalize_lan)

    # Räknare för totala antal situationer
    total_situations = df.shape[0]
    st.metric("Totalt antal situationer", total_situations)

    # Räkna antal situationer per län
    lan_counts = df['LAN'].value_counts().reset_index()
    lan_counts.columns = ['Län', 'Antal situationer']

    # Visa antal situationer per län i en tabell
    st.subheader('Antal situationer per län')
    st.dataframe(lan_counts)

    # Visualisera antal situationer per län med Altair
    chart = alt.Chart(lan_counts).mark_bar().encode(
        x=alt.X('Antal situationer:Q', title='Antal situationer'),
        y=alt.Y('Län:N', sort='-x', title='Län')
    ).properties(
        width=700,
        height=400
    )

    st.altair_chart(chart)

# Använd layout-funktionen
layout()