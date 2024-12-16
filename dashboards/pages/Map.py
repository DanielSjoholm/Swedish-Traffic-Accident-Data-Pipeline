import streamlit as st
import pandas as pd
import pydeck as pdk
from helpers.Connect_and_query import query_trafic_situations

def layout():
    st.set_page_config(layout="wide")
    st.subheader('Traffic Situations Dashboard with Interactive Map')

    # Hämta och förbered trafikdata
    df = query_trafic_situations()
    df.columns = df.columns.str.upper()

    # Konvertera latitud och longitud till numeriska värden för att undvika strängproblem
    df['WGS84_POINT_LATITUDE'] = pd.to_numeric(df['WGS84_POINT_LATITUDE'], errors='coerce')
    df['WGS84_POINT_LONGITUDE'] = pd.to_numeric(df['WGS84_POINT_LONGITUDE'], errors='coerce')

    # Filtrera bort rader där latitud eller longitud är NaN
    df = df.dropna(subset=['WGS84_POINT_LATITUDE', 'WGS84_POINT_LONGITUDE'])

    # Omvandla start_time och end_time till datetime-format
    df['START_TIME'] = pd.to_datetime(df['START_TIME'])
    df['END_TIME'] = pd.to_datetime(df['END_TIME'])

    # Välj datumintervall
    min_date = df['START_TIME'].min().date()
    max_date = df['START_TIME'].max().date()
    
    selected_date = st.slider('Välj datum:', min_value=min_date, max_value=max_date, value=(min_date, max_date))
    
    # Filtrera datan baserat på valt datumintervall
    filtered_df = df[(df['START_TIME'].dt.date >= selected_date[0]) & (df['START_TIME'].dt.date <= selected_date[1])]

    # Kontrollera att det finns data att visa
    if not filtered_df.empty:
        # Konvertera START_TIME och END_TIME till strängar i ett läsbart format
        filtered_df['START_TIME'] = filtered_df['START_TIME'].dt.strftime('%Y-%m-%d %H:%M:%S')
        filtered_df['END_TIME'] = filtered_df['END_TIME'].dt.strftime('%Y-%m-%d %H:%M:%S')

        # Visa en karta med alla trafiksituationer inom valt datumintervall
        st.subheader(f"Trafiksituationer mellan {selected_date[0]} och {selected_date[1]}")

        # Skapa en pydeck-karta
        view_state = pdk.ViewState(
            latitude=filtered_df['WGS84_POINT_LATITUDE'].mean(),
            longitude=filtered_df['WGS84_POINT_LONGITUDE'].mean(),
            zoom=5,
            pitch=0,
        )

        # Skapa lager för trafiksituationerna
        layer = pdk.Layer(
            'ScatterplotLayer',
            data=filtered_df,
            get_position='[WGS84_POINT_LONGITUDE, WGS84_POINT_LATITUDE]',
            get_color='[200, 30, 0, 160]',
            get_radius=2000,
            pickable=True  # Gör det möjligt att klicka på punkterna
        )

        # Lägg till tooltip för att visa information när man hovrar över en prick
        tooltip = {
            "html": "<b>Situation:</b> {SITUATION_TYPE}<br>"
                    "<b>Severity:</b> {SEVERITY_TEXT}<br>"
                    "<b>Road Name:</b> {ROAD_NAME}<br>"
                    "<b>Description:</b> {LOCATION_DESCRIPTOR}<br>"
                    "<b>Limit:</b> {TEMPORARY_LIMIT}<br>"
                    "<b>Affected Directions:</b> {AFFECTED_DIRECTION}<br>"
                    "<b>Start Time:</b> {START_TIME}<br>"
                    "<b>End Time:</b> {END_TIME}",
            "style": {
                "backgroundColor": "steelblue",
                "color": "white"
            }
        }

        # Visa kartan
        r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip)
        st.pydeck_chart(r)

    else:
        st.write("Ingen data för valt datumintervall.")

# Använd layout-funktionen
layout()
