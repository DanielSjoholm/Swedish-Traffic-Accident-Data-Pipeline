import streamlit as st
import pandas as pd
import altair as alt
from helpers.normalize import normalize_lan
from helpers.reverse_geocode import reverse_geocode
from helpers.Connect_and_query import query_trafic_situations

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

    # Räkna antal situationer per län
    lan_counts = df['LAN'].value_counts().reset_index()
    lan_counts.columns = ['Län', 'Antal situationer']

    # Dropdown för att välja län
    selected_lan = st.selectbox("Välj Län", df['LAN'].unique())

    # Filtrera data för det valda länet
    filtered_df = df[df['LAN'] == selected_lan]

    # Räknare för totala antal situationer i det valda länet
    total_situations_selected_lan = filtered_df.shape[0]
    st.metric(f"Totalt antal situationer i {selected_lan}", total_situations_selected_lan)

    # Räkna antal message_type för det valda länet
    message_type_counts = filtered_df['MESSAGE_TYPE'].value_counts().reset_index()
    message_type_counts.columns = ['Message Type', 'Antal']

    # Visualisera antal message_type för det valda länet
    st.subheader(f'Antal Message Types för {selected_lan}')
    message_chart = alt.Chart(message_type_counts).mark_bar().encode(
        x=alt.X('Antal:Q', title='Antal'),
        y=alt.Y('Message Type:N', sort='-x', title='Message Type')
    ).properties(
        width=700,
        height=400
    )
    st.altair_chart(message_chart)

    # Dropdown för att välja message_type
    selected_message_type = st.selectbox("Välj Message Type", df['MESSAGE_TYPE'].unique())

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