import pandas as pd

# Load the green taxi trip data
data_file = "green_tripdata_2019-10.csv"
zone_file = "taxi_zone_lookup.csv"

# Load the data into DataFrames
df = pd.read_csv(data_file)
zones = pd.read_csv(zone_file)

# Convert pickup datetime column to datetime format
df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])

# Filter data for October 18, 2019
filtered_df = df[df['lpep_pickup_datetime'].dt.date == pd.to_datetime("2019-10-18").date()]

# Group by pickup location ID and calculate total_amount for each zone
pickup_totals = filtered_df.groupby('PULocationID')['total_amount'].sum().reset_index()

# Merge with zone lookup table to get zone names
pickup_totals = pickup_totals.merge(zones, left_on='PULocationID', right_on='LocationID')

# Sort by total_amount in descending order
pickup_totals = pickup_totals.sort_values(by='total_amount', ascending=False)

# Filter zones where total_amount exceeds 13,000 and get the top 3 zones
top_zones = pickup_totals[pickup_totals['total_amount'] > 13000].head(3)

# Print the results
print("Top three pickup zones with total_amount > 13,000 on 2019-10-18:")
for _, row in top_zones.iterrows():
    print(f"{row['Zone']} - Total Amount: {row['total_amount']}")
