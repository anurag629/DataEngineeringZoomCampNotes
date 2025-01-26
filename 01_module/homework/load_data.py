import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection string
postgres_user = "postgres"
postgres_password = "postgres"
postgres_host = "db"  # Docker service name for Postgres
postgres_port = "5432"
postgres_db = "ny_taxi"

engine = create_engine(f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}")

# Load the green taxi trip data
print("Loading green taxi trip data...")
trip_data = pd.read_csv("https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz", compression="gzip")
trip_data.to_sql("green_taxi_trips", engine, if_exists="replace", index=False)
print("Green taxi trip data loaded successfully!")

# Load the taxi zone lookup data
print("Loading taxi zone lookup data...")
zone_data = pd.read_csv("https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv")
zone_data.to_sql("taxi_zone_lookup", engine, if_exists="replace", index=False)
print("Taxi zone lookup data loaded successfully!")
