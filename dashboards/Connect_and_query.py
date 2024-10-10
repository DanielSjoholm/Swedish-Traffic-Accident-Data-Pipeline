from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import pandas as pd

def query_trafic_situations(query='SELECT * FROM mart.mart_traffic_situations'):
    try:
        # Ladda miljövariabler
        load_dotenv()

        # Skapa en SQLAlchemy engine
        engine = create_engine(f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}')
        
        # Använd engine i pandas read_sql
        df = pd.read_sql(query, engine)
        return df

    except Exception as e:
        print(f"Fel vid anslutning till databasen: {e}")
