import dlt
from pathlib import Path
import os
from helpers.trafic import trafikverket_resource

def run_pipeline_for_trafikverket(table_name):
    pipeline = dlt.pipeline(
        pipeline_name="trafikverket_pipeline",
        destination="snowflake",
        dataset_name="staging", 
    )

    load_info = pipeline.run(trafikverket_resource(), table_name=table_name)
    print("Trafikverket pipeline complete:", load_info)

if __name__ == "__main__":
    working_directory = Path(__file__).parent
    os.chdir(working_directory)

    trafikverket_table_name = "trafikverket_data"
    run_pipeline_for_trafikverket(table_name=trafikverket_table_name)