import dlt
from pathlib import Path
import os
from helpers.trafic import trafikverket_resource
from helpers.connect_db import connect_db, close_db
from helpers.create_schema import create_schema

def run_pipeline_for_trafikverket(table_name):
    pipeline = dlt.pipeline(
        pipeline_name="trafikverket_pipeline",
        destination="postgres", 
        dataset_name="staging", 
    )

    load_info = pipeline.run(trafikverket_resource(), table_name=table_name)
    print("Trafikverket pipeline complete:", load_info)
    try:
        conn, cur = connect_db()
        create_schema(conn, cur)
        close_db(conn, cur)
    except Exception as e:
        print(f"Failed to create schema: {e}")

if __name__ == "__main__":
    working_directory = Path(__file__).parent
    os.chdir(working_directory)

    trafikverket_table_name = "trafikverket_data"
    run_pipeline_for_trafikverket(table_name=trafikverket_table_name)