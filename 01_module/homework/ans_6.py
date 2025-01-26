import pandas as pd

# Load the green taxi trip data
data_file = "green_tripdata_2019-10.csv"
zone_file = "taxi_zone_lookup.csv"

# Load the data into DataFrames
df = pd.read_csv(data_file)
zones = pd.read_csv(zone_file)

# Convert pickup datetime column to datetime format
df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])

# Filter for October 2019
filtered_df = df[(df['lpep_pickup_datetime'] >= '2019-10-01') & 
                 (df['lpep_pickup_datetime'] < '2019-11-01')]

# Merge with zone lookup table to get pickup and drop-off zone names
filtered_df = filtered_df.merge(zones, left_on='PULocationID', right_on='LocationID', suffixes=('', '_pickup'))
filtered_df = filtered_df.merge(zones, left_on='DOLocationID', right_on='LocationID', suffixes=('_pickup', '_dropoff'))

# Filter for trips picked up in "East Harlem North"
east_harlem_trips = filtered_df[filtered_df['Zone_pickup'] == 'East Harlem North']

# Find the drop-off zone with the largest tip
largest_tip_trip = east_harlem_trips.loc[east_harlem_trips['tip_amount'].idxmax()]

# Print the results
print(f"Drop-off zone with the largest tip: {largest_tip_trip['Zone_dropoff']}")
print(f"Largest tip amount: {largest_tip_trip['tip_amount']}")
