import pandas as pd

# Load the green taxi trip data
data_file = "green_tripdata_2019-10.csv"
df = pd.read_csv(data_file)

# Convert pickup datetime column to datetime format
df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])

# Extract only the pickup date from the datetime column
df['pickup_date'] = df['lpep_pickup_datetime'].dt.date

# Find the longest trip distance for each day
longest_trips = df.groupby('pickup_date')['trip_distance'].max().reset_index()

# Find the day with the longest trip
longest_trip_day = longest_trips.loc[longest_trips['trip_distance'].idxmax()]

# Print the results
print(f"The day with the longest trip is: {longest_trip_day['pickup_date']}")
print(f"The longest trip distance on that day is: {longest_trip_day['trip_distance']}")
