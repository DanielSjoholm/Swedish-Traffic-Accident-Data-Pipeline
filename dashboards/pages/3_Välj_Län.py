import streamlit as st
import pandas as pd
import altair as alt
import json
from helpers.normalize import normalize_lan
from helpers.Connect_and_query import query_trafic_situations

st.set_page_config(
    page_title="Län & Trafikmeddelanden",
    page_icon="🚧",
    layout="wide"
)

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
    # st.set_page_config(layout="wide")
    st.subheader('Trafiksituationer Per Län')

    # Ladda geocode-mappning
    geocode_mapping = prepare_geocode_mapping()

    # Hämta och förbered trafikdata
    df = query_trafic_situations()
    df.columns = df.columns.str.upper()

    # Lägg till länsinformation från mappningen
    def get_lan_from_mapping(row):
        try:
            lat = float(row['WGS84_POINT_LATITUDE'])
            lon = float(row['WGS84_POINT_LONGITUDE'])
        except (ValueError, TypeError):
            return "Okänd län"

        if pd.notna(lat) and pd.notna(lon):
            cache_key = (lat, lon)
            geo_info = geocode_mapping.get(cache_key, {"lan": "Okänd län"})
            return normalize_lan(geo_info["lan"])
        else:
            return "Okänd län"

    df['LAN'] = df.apply(get_lan_from_mapping, axis=1)

    # Räkna antal situationer per län
    lan_counts = df['LAN'].value_counts().reset_index()
    lan_counts.columns = ['Län', 'Antal situationer']

    # Dropdown för att välja län
    selected_lan = st.selectbox("Välj Län", sorted(df['LAN'].unique()))

    # Filtrera data för det valda länet
    filtered_df = df[df['LAN'] == selected_lan]

    # Räknare för totala antal situationer i det valda länet
    total_situations_selected_lan = filtered_df.shape[0]
    st.metric(f"Totalt antal situationer i {selected_lan}", total_situations_selected_lan)

    # Räkna antal message_type för det valda länet
    message_type_counts = filtered_df['MESSAGE_TYPE'].value_counts().reset_index()
    message_type_counts.columns = ['Message Type', 'Antal']

    # Visualisera antal message_type för det valda länet
    st.subheader(f'Antal Meddelande för {selected_lan}')
    message_chart = alt.Chart(message_type_counts).mark_bar().encode(
        x=alt.X('Antal:Q', title='Antal'),
        y=alt.Y('Message Type:N', sort='-x', title='Message Type')
    ).properties(
        width=700,
        height=400
    )
    st.altair_chart(message_chart)

    # Dropdown för att välja message_type
    selected_message_type = st.selectbox("Välj Trafikmeddelande", sorted(df['MESSAGE_TYPE'].unique()))

    # Filtrera data för det valda message_type
    filtered_df = df[df['MESSAGE_TYPE'] == selected_message_type]

    # Räkna antal av det valda message_type per län
    message_type_per_lan = filtered_df['LAN'].value_counts().reset_index()
    message_type_per_lan.columns = ['Län', 'Antal']

    # Visualisera antal av det valda message_type per län
    message_chart = alt.Chart(message_type_per_lan).mark_bar().encode(
        x=alt.X('Län:N', sort='-y', title='Län'),
        y=alt.Y('Antal:Q', title=f'Antal {selected_message_type}')
    ).properties(
        width=700,
        height=400
    ).transform_window(
        rank='rank(Antal)',
        sort=[alt.SortField('Antal', order='descending')]
    )
    st.altair_chart(message_chart)

# Använd layout-funktionen
layout()
