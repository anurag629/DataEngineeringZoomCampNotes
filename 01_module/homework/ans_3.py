import pandas as pd

# Load the green taxi trip data
data_file = "green_tripdata_2019-10.csv"
df = pd.read_csv(data_file)

# Convert pickup and dropoff datetime columns to datetime format
df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])

# Filter data for October 1, 2019 (inclusive) to November 1, 2019 (exclusive)
filtered_df = df[(df['lpep_pickup_datetime'] >= '2019-10-01') & 
                 (df['lpep_pickup_datetime'] < '2019-11-01')]

# Calculate trip segmentation counts based on trip_distance
trip_segmentation = {
    "Up to 1 mile": len(filtered_df[filtered_df['trip_distance'] <= 1]),
    "1-3 miles": len(filtered_df[(filtered_df['trip_distance'] > 1) & (filtered_df['trip_distance'] <= 3)]),
    "3-7 miles": len(filtered_df[(filtered_df['trip_distance'] > 3) & (filtered_df['trip_distance'] <= 7)]),
    "7-10 miles": len(filtered_df[(filtered_df['trip_distance'] > 7) & (filtered_df['trip_distance'] <= 10)]),
    "Over 10 miles": len(filtered_df[filtered_df['trip_distance'] > 10]),
}

# Print the results
for segment, count in trip_segmentation.items():
    print(f"{segment}: {count}")
