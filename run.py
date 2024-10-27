import os
import subprocess

# Klona hela repository från GitHub
repo_url = "https://github.com/DanielSjoholm/Swedish-Traffic-Accident-Data-Pipeline"
subprocess.run(["git", "clone", repo_url])

# Navigera till den klonade mappen
os.chdir("Swedish-Traffic-Accident-Data-Pipeline")

# Installera dbt och andra beroenden om nödvändigt
subprocess.run(["pip", "install", "-r", "requirements.txt"])

# Navigera till dlt_postgres för att köra DLT-koden
os.chdir("dlt_postgres")

# Köra DLT-koden för att hämta data från API och ladda det i PostgreSQL
subprocess.run(["python", "load_data_postgres_pipeline.py"])  # Denna laddar in till PostgreSQL

# Gå tillbaka till huvudkatalogen för att köra dbt
os.chdir("..")

# Navigera till dbt-mappen
os.chdir("dbt_transform")

# Kör dbt run för att transformera data
subprocess.run(["dbt", "run"])