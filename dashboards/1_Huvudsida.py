import streamlit as st
import pandas as pd
import pydeck as pdk
import altair as alt
from helpers.Connect_and_query import query_trafic_situations

# Konfigurera sidan först!
st.set_page_config(
    page_title="Huvudsida - Trafikinformation",
    page_icon="🚦",
    layout="wide"
)
# Funktion för att skapa huvudlayouten för dashboarden
def main_page():
    # st.set_page_config(layout="wide")  # This line is redundant and can be removed
    st.title('Trafiksituationer i realtid')

    # Hämta och förbered trafikdata
    df = query_trafic_situations()
    df.columns = df.columns.str.upper()

    # Konvertera latitud och longitud till numeriska värden
    df['WGS84_POINT_LATITUDE'] = pd.to_numeric(df['WGS84_POINT_LATITUDE'], errors='coerce')
    df['WGS84_POINT_LONGITUDE'] = pd.to_numeric(df['WGS84_POINT_LONGITUDE'], errors='coerce')

    # Filtrera bort rader utan koordinater
    df = df.dropna(subset=['WGS84_POINT_LATITUDE', 'WGS84_POINT_LONGITUDE'])

    # Filtrera data för dagens datum
    df['START_TIME'] = pd.to_datetime(df['START_TIME'])
    today = (pd.Timestamp.now().normalize() - pd.Timedelta(days=1))
    df_today = df[df['START_TIME'].dt.date == today.date()]

    # Översiktsdata
    total_situations = len(df_today)
    severe_situations = df_today[df_today['SEVERITY_TEXT'] == 'Severe'].shape[0]

    st.subheader('Sammanfattning')
    col1, col2 = st.columns(2)
    col1.metric("Totalt antal störningar", total_situations)
    col2.metric("Allvarliga störningar", severe_situations)

    # Interaktiv karta
    st.subheader('Interaktiv karta över aktuella störningar')

    view_state = pdk.ViewState(
        latitude=df_today['WGS84_POINT_LATITUDE'].mean(),
        longitude=df_today['WGS84_POINT_LONGITUDE'].mean(),
        zoom=5,
        pitch=0
    )

    layer = pdk.Layer(
        'ScatterplotLayer',
        data=df_today,
        get_position='[WGS84_POINT_LONGITUDE, WGS84_POINT_LATITUDE]',
        get_color='[255, 0, 0, 160]' if 'SEVERITY_TEXT' == 'Severe' else '[0, 0, 255, 160]',
        get_radius=2000,
        pickable=True
    )

    tooltip = {
        "html": "<b>Situation:</b> {SITUATION_TYPE}<br>"
                "<b>Severity:</b> {SEVERITY_TEXT}<br>"
                "<b>Road Name:</b> {ROAD_NAME}<br>"
                "<b>Description:</b> {LOCATION_DESCRIPTOR}<br>",
        "style": {"backgroundColor": "steelblue", "color": "white"}
    }

    r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip)
    st.pydeck_chart(r)



    # Top 5 mest drabbade vägar
    st.subheader('Mest Drabbade Vägar')
    top_roads = df_today['ROAD_NAME'].value_counts().reset_index()
    top_roads.columns = ['Väg', 'Antal Störningar']
    # Flytta "Ej Specifierat" till slutet av listan
    top_roads = top_roads.sort_values(by=['Väg'], key=lambda x: x == 'Ej Specifierat').head(5)
    st.table(top_roads)
    # Senaste trafiksituationerna
    
    st.subheader('De senaste trafiksituationerna')
    latest_situations = df_today.sort_values(by='START_TIME', ascending=False).head(5)
    st.dataframe(latest_situations[['START_TIME', 'ROAD_NAME', 'SITUATION_TYPE', 'SEVERITY_TEXT', 'LOCATION_DESCRIPTOR']])

# Kör funktionen
if __name__ == "__main__":
    main_page()
