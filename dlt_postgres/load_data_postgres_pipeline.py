import dlt
from pathlib import Path
import os
from helpers.trafic import trafikverket_resource
from helpers.unique_id import add_unique_constraint
from helpers.connect_db import connect_db, close_db
from helpers.create_schema import create_schema

def run_pipeline_for_trafikverket(table_name):
    pipeline = dlt.pipeline(
        pipeline_name="trafikverket_pipeline",
        destination="postgres", 
        dataset_name="staging", 
    )

    conn, cur = connect_db()
    try:
        # add_unique_constraint(conn, cur)
        create_schema(conn, cur)
    except Exception as e:
        print(f"Ett fel uppstod: {e}")
    finally:
        close_db(conn, cur)

    load_info = pipeline.run(trafikverket_resource(), table_name=table_name)
    print("Trafikverket pipeline complete:", load_info)


if __name__ == "__main__":
    working_directory = Path(__file__).parent
    os.chdir(working_directory)

    trafikverket_table_name = "trafikverket_data"
    run_pipeline_for_trafikverket(table_name=trafikverket_table_name)