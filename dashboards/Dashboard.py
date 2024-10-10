import streamlit as st
import pandas as pd
import altair as alt
from Connect_and_query import query_trafic_situations
from geopy.geocoders import Nominatim

def layout():
    st.set_page_config(layout="wide")
    st.subheader('Traffic Situations Dashboard')

    # Skapa anslutning till datakällan
    df = query_trafic_situations()

    # Ändra alla kolumnnamn till stora bokstäver
    df.columns = df.columns.str.upper()

    # Geopy för reverse geocoding
    geolocator = Nominatim(user_agent="geoapiExercises")

    # Funktion för att omvandla latitud och longitud till region
    def get_region_from_coordinates(lat, lon):
        try:
            location = geolocator.reverse(f"{lat}, {lon}")
            return location.raw.get('address', {}).get('state', 'Okänd region')
        except:
            return 'Okänd region'

    # Applicera funktionen på dina latitud- och longitudkolumner för att få region
    df['REGION'] = df.apply(lambda row: get_region_from_coordinates(row['WGS84_POINT_LATITUDE'], row['WGS84_POINT_LONGITUDE']), axis=1)

    # Räkna antal trafikincidenter per region
    incidents_per_region = df.groupby('REGION').size().reset_index(name='TOTAL_SITUATIONS')
    incidents_per_region = incidents_per_region.sort_values(by='TOTAL_SITUATIONS', ascending=False)

    # KPI cards med kolumnreferenser i stora bokstäver
    total_situations = df.shape[0]
    total_lanes_restricted = df['NUMBER_OF_LANES_RESTRICTED'].sum()
    most_common_situation = df['SITUATION_TYPE'].mode()[0]
    situations_per_type = df.groupby('SITUATION_TYPE').size().reset_index(name='ANTAL_SITUATIONER')
    situations_per_type = situations_per_type.sort_values(by='ANTAL_SITUATIONER', ascending=False)
    situations_per_road = df.groupby('ROAD_NAME').size().reset_index(name='ANTAL_SITUATIONER_PER_VÄG')
    situations_per_road = situations_per_road.sort_values(by='ANTAL_SITUATIONER_PER_VÄG', ascending=False)

    # Affected directions
    most_affected_direction = df['AFFECTED_DIRECTION'].mode()[0]  # Most common affected direction
    situations_per_direction = df.groupby('AFFECTED_DIRECTION').size().reset_index(name='ANTAL_SITUATIONER_PER_RIKTNING')

    # Severity of messages
    high_severity_situations = df[df['SEVERITY_TEXT'] == 'Hög'].shape[0]  # Number of high severity situations
    severity_distribution = df['SEVERITY_TEXT'].value_counts().reset_index(name='SEVERITY_COUNT')  # Severity distribution
    severity_distribution.rename(columns={'index': 'SEVERITY'}, inplace=True)

    # Upcoming traffic situations (based on start time)
    df['START_TIME'] = pd.to_datetime(df['START_TIME'], errors='coerce')
    upcoming_situations = df[df['START_TIME'] <= pd.Timestamp.today() + pd.Timedelta(weeks=1)].shape[0]  # Traffic situations starting within a week

    # Traffic situation duration
    df['END_TIME'] = pd.to_datetime(df['END_TIME'], errors='coerce')
    df['DURATION_HOURS'] = (df['END_TIME'] - df['START_TIME']).dt.total_seconds() / 3600  # Calculate duration in hours
    average_duration = df['DURATION_HOURS'].mean()  # Average duration of traffic situations

    # Traffic restriction types
    restriction_type_count = df['TRAFFIC_RESTRICTION_TYPE'].value_counts().reset_index(name='ANTAL_RESTRIKTIONER')  # Count of restriction types
    restriction_type_count.rename(columns={'index': 'RESTRIKTION_TYP'}, inplace=True)

    # KPI output
    print(f"Total traffic situations: {total_situations}")
    print(f"Total lanes restricted: {total_lanes_restricted}")
    print(f"Most common traffic situation type: {most_common_situation}")
    print(f"Most affected direction: {most_affected_direction}")
    print(f"High severity situations: {high_severity_situations}")
    print(f"Upcoming situations (within a week): {upcoming_situations}")
    print(f"Average duration of traffic situations (hours): {average_duration:.2f}")

    # Visa incidenter per region
    print("Total traffic situations per region:")
    print(incidents_per_region)

# Använd layout-funktionen
layout()