import os
import pandas as pd
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()  # Load env variables from .env

# Fetch Snowflake connection info from environment variables
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")  # e.g. QOZLOTH-NWC71749
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")  # e.g. OIL_GAS_DB
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")  # e.g. OIL_GAS_SCHEMA
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")  # e.g. COMPUTE_WH
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE")  # e.g. ACCOUNTADMIN

CSV_FILE_PATH = 'sample_oil_gas_market_data.csv'

# Connect to Snowflake
ctx = snowflake.connector.connect(
    user=SNOWFLAKE_USER,
    password=SNOWFLAKE_PASSWORD,
    account=SNOWFLAKE_ACCOUNT,
    warehouse=SNOWFLAKE_WAREHOUSE,
    database=SNOWFLAKE_DATABASE,
    schema=SNOWFLAKE_SCHEMA,
    role=SNOWFLAKE_ROLE,
)

cs = ctx.cursor()

try:
    # Step 1: Create a staging area (named internal stage)
    stage_name = 'MY_STAGE'
    cs.execute(f"CREATE OR REPLACE STAGE {stage_name}")

    # Step 2: Put local CSV file to the Snowflake internal stage
    print("Uploading CSV file to Snowflake stage...")
    put_command = f"PUT file://{os.path.abspath(CSV_FILE_PATH)} @{stage_name} OVERWRITE = TRUE"
    cs.execute(put_command)

    # Step 3: Copy data from stage to your MarketData table
    print("Copying data into MarketData table...")
    copy_command = f"""
        COPY INTO MarketData (date, commodity, price, volume)
        FROM @{stage_name}/{os.path.basename(CSV_FILE_PATH)}
        FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY='"' SKIP_HEADER=1)
        ON_ERROR = 'ABORT_STATEMENT'
    """
    cs.execute(copy_command)

    print("Data loaded successfully!")

finally:
    cs.close()
    ctx.close()
