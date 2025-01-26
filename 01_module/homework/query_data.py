from sqlalchemy import create_engine
import pandas as pd

# PostgreSQL connection string
postgres_user = "postgres"
postgres_password = "postgres"
postgres_host = "db"  # Docker service name for Postgres
postgres_port = "5432"
postgres_db = "ny_taxi"

engine = create_engine(f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}")

# Query for trip segmentation
query = """
SELECT 
    SUM(CASE WHEN trip_distance <= 1 THEN 1 ELSE 0 END) AS "Up to 1 mile",
    SUM(CASE WHEN trip_distance > 1 AND trip_distance <= 3 THEN 1 ELSE 0 END) AS "1-3 miles",
    SUM(CASE WHEN trip_distance > 3 AND trip_distance <= 7 THEN 1 ELSE 0 END) AS "3-7 miles",
    SUM(CASE WHEN trip_distance > 7 AND trip_distance <= 10 THEN 1 ELSE 0 END) AS "7-10 miles",
    SUM(CASE WHEN trip_distance > 10 THEN 1 ELSE 0 END) AS "Over 10 miles"
FROM green_taxi_trips
WHERE lpep_pickup_datetime >= '2019-10-01' 
  AND lpep_pickup_datetime < '2019-11-01';
"""

# Execute the query
print("Executing trip segmentation query...")
result = pd.read_sql(query, engine)
print("Query Results:")
print(result)
