# Swedish-Traffic-Accident-Data-Pipeline
https://rx96840.west-europe.azure.snowflakecomputing.com/
# Thesis Project: Data Management of Traffic Accidents in Sweden

## Project Description
This project aims to develop a data-driven solution to collect, process, and analyze data on traffic accidents in Sweden. By utilizing the Swedish Transport Administration's API, accident data will be retrieved, processed, and stored in a Snowflake database. Finally, statistics on the accidents will be visualized in a Power BI dashboard.

## Technologies and Tools
- **Python**: Used for fetching and processing data from the Swedish Transport Administration's API.
- **Visual Studio Code (VSC)**: Main development environment for Python scripts.
- **Snowflake**: Cloud-based solution for storing and managing data with ELT processes.
- **Delta Live Tables (DLT)**: Used to automate and manage data pipelines in Snowflake.
- **Power BI**: Used for creating visualizations and dashboards from the processed data.

## Project Structure
- `scripts/`: Python scripts for fetching and processing data from the Swedish Transport Administration's API.
- `data/`: Temporary storage of data before uploading it to Snowflake.
- `snowflake/`: SQL scripts and configurations for the database structure in Snowflake.
- `powerbi/`: Power BI reports and dashboard files.
- `README.md`: Project documentation.

## Installation
1. **Clone this repository:**
    ```bash
    git clone [repo-url]
    ```
2. **Install necessary Python packages:**
    ```bash
    pip install -r requirements.txt
    ```
3. **Configure Snowflake connection:**
    - Create a `.env` file in the root directory and add your Snowflake credentials.

4. **Configure the Swedish Transport Administration API key:**
    - Add the API key to the `.env` file.

## Usage
1. **Fetch data from the Swedish Transport Administration's API:**
    ```bash
    python scripts/fetch_data.py
    ```

2. **Upload and process data in Snowflake using DLT:**
    - Follow the instructions in `snowflake/README.md`.

3. **Visualize data in Power BI:**
    - Open the Power BI files in `powerbi/` and update the data sources.

## Contact
For questions or support, please contact [Your Name] at [your-email@example.com].
