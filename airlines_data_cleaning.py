import pandas as pd
import numpy as np

file_path = r"C:\Users\LENOVO\Desktop\Airlines_Data_Engineering\data\UseCase - Airlines.xlsx"

excel_file = pd.ExcelFile(file_path)

flights = pd.read_excel(
    file_path,
    sheet_name="flights"
)

print("\nFirst 5 rows:")
print(flights.head())

print("\nShape:")
print(flights.shape)

print("\nColumns:")
print(flights.columns.tolist())

print("\nData types:")
print(flights.dtypes)

print("\nMissing values:")
print(flights.isnull().sum())

print("\nDuplicate rows:")
print(flights.duplicated().sum())

duplicate_rows = flights[flights.duplicated(keep=False)]

print("\nDuplicate records:")
print(duplicate_rows.sort_values("flight_id").to_string(index=False))

print("\nNumber of exact duplicate rows:", flights.duplicated().sum())

missing_airline = flights[flights["airline"].isna()]

print("\nRows with missing airline:")
print(missing_airline.to_string(index=False))

print("\nAirline value counts:")
print(flights["airline"].value_counts(dropna=False))

print("\nFlight ID examples:")
print(flights["flight_id"].head(20).to_string(index=False))

print("\nFlight ID lengths:")
print(flights["flight_id"].astype(str).str.len().value_counts().sort_index())

print("\nFirst characters of flight IDs:")
print(flights["flight_id"].astype(str).str[:2].value_counts())

print("\nDuration examples:")
print(flights["duration"].head(20).to_string(index=False))

print("\nDuration data type:")
print(flights["duration"].dtype)

print("\nUnique duration formats/examples:")
print(flights["duration"].dropna().astype(str).head(30).to_list())

print(
    flights[
        ["flight_id", "departure_time", "arrival_time", "duration"]
    ].head(20).to_string(index=False)
)

time_difference = flights["arrival_time"] - flights["departure_time"]

print("\nTime differences:")
print(time_difference.head(20))

flights["flight_prefix"] = flights["flight_id"].str[:2]

print("\nFlight prefix vs airline:")
print(
    pd.crosstab(
        flights["flight_prefix"],
        flights["airline"],
        dropna=False
    )
)

unknown_airline = flights[flights["airline"] == "UNKNOWN"]

print("\nUNKNOWN airline records:")
print(
    unknown_airline[
        ["flight_id", "source", "destination", "departure_time", "arrival_time"]
    ].to_string(index=False)
)

valid_pattern = flights["flight_id"].str.match(r"^[A-Z0-9]{2}[0-9]{3}$")

print("\nFlight IDs matching expected pattern:")
print(valid_pattern.value_counts())

invalid_ids = flights[~valid_pattern]

print("\nInvalid flight IDs:")
print(invalid_ids[["flight_id", "airline"]].to_string(index=False))

print("\nSource airports:")
print(flights["source"].value_counts())

print("\nDestination airports:")
print(flights["destination"].value_counts())

same_route = flights[flights["source"] == flights["destination"]]

print("\nFlights with same source and destination:")
print(same_route.to_string(index=False))

calculated_duration = (
    flights["arrival_time"] - flights["departure_time"]
)

provided_duration = flights["duration"].apply(
    lambda x: pd.Timedelta(
        hours=x.hour,
        minutes=x.minute,
        seconds=x.second
    )
)

duration_check = calculated_duration == provided_duration

print("\nDuration comparison:")
print(duration_check.value_counts())

duration_mismatch = flights[~duration_check]

print("\nDuration mismatches:")
print(
    duration_mismatch[
        [
            "flight_id",
            "departure_time",
            "arrival_time",
            "duration"
        ]
    ].to_string(index=False)
)

print("\nMismatch details:")

duration_mismatch = duration_mismatch.copy()

duration_mismatch["calculated_duration"] = (
    duration_mismatch["arrival_time"]
    - duration_mismatch["departure_time"]
)

print(
    duration_mismatch[
        [
            "flight_id",
            "departure_time",
            "arrival_time",
            "duration",
            "calculated_duration"
        ]
    ].to_string(index=False)
)

print("\nDuration Python types:")
print(flights["duration"].map(type).value_counts())
print("\nSJ192 duration:")
print(flights.loc[flights["flight_id"] == "SJ192", "duration"].to_string())


def convert_duration(value):
    if pd.isna(value):
        return pd.NaT

    if isinstance(value, pd.Timestamp):
        return (
            pd.Timedelta(hours=value.hour)
            + pd.Timedelta(minutes=value.minute)
            + pd.Timedelta(seconds=value.second)
        )

    if hasattr(value, "hour"):
        return (
            pd.Timedelta(hours=value.hour)
            + pd.Timedelta(minutes=value.minute)
            + pd.Timedelta(seconds=value.second)
        )

    return pd.to_timedelta(str(value))


flights["duration_clean"] = flights["duration"].apply(convert_duration)

print("\nClean duration examples:")
print(
    flights[
        ["flight_id", "duration", "duration_clean"]
    ].head(20).to_string(index=False)
)

flights["calculated_duration"] = (
    flights["arrival_time"] - flights["departure_time"]
)

print("\nNegative durations:")
print(
    flights[flights["calculated_duration"] < pd.Timedelta(0)][
        ["flight_id", "departure_time", "arrival_time",
         "duration_clean", "calculated_duration"]
    ].to_string(index=False)
)

tolerance = pd.Timedelta(seconds=1)

duration_valid = (
    (flights["calculated_duration"] >= pd.Timedelta(0))
    &
    (
        abs(
            flights["calculated_duration"]
            - flights["duration_clean"]
        ) <= tolerance
    )
)

print("\nDuration validation:")
print(duration_valid.value_counts())

print("\nRecords failing duration validation:")

print(
    flights[~duration_valid][
        ["flight_id", "departure_time", "arrival_time",
         "duration_clean", "calculated_duration"]
    ].to_string(index=False)
)

airline_mapping = {
    "AI": "Air India",
    "SJ": "SpiceJet",
    "UK": "Vistara",
    "6F": "IndiGo"
}
flights["airline_clean"] = flights["flight_prefix"].map(airline_mapping)
print("\nAirline cleaning comparison:")
print(
    flights[
        ["flight_id", "airline", "airline_clean"]
    ].head(30).to_string(index=False)
)
print("\nClean airline value counts:")
print(flights["airline_clean"].value_counts(dropna=False))
airline_mismatch = flights[
    flights["airline"].notna()
    & (flights["airline"] != "UNKNOWN")
    & (flights["airline"] != flights["airline_clean"])
]

print("\nAirline mismatches:")
print(
    airline_mismatch[
        ["flight_id", "airline", "airline_clean"]
    ].to_string(index=False)
)

cleaned_flights = flights.copy()
cleaned_flights = cleaned_flights.drop_duplicates()
print("\nRows before duplicate removal:", len(flights))
print("Rows after duplicate removal:", len(cleaned_flights))
print("Duplicates remaining:", cleaned_flights.duplicated().sum())

cleaned_flights["airline"] = cleaned_flights["airline_clean"]
cleaned_flights = cleaned_flights.drop(
    columns=["flight_prefix", "airline_clean"]
)
print("\nCleaned columns:")
print(cleaned_flights.columns.tolist())
print("\nInvalid timestamp records:")

print(
    cleaned_flights[
        cleaned_flights["arrival_time"] < cleaned_flights["departure_time"]
    ][
        ["flight_id", "departure_time", "arrival_time", "duration"]
    ].to_string(index=False)
)

invalid_flights = cleaned_flights[
    cleaned_flights["arrival_time"] < cleaned_flights["departure_time"]
].copy()

print("\nInvalid flights:")
print(invalid_flights[["flight_id", "departure_time", "arrival_time"]])
cleaned_flights = cleaned_flights[
    cleaned_flights["arrival_time"] >= cleaned_flights["departure_time"]
].copy()
print("\nCleaned flight row count:", len(cleaned_flights))
print("Invalid flight row count:", len(invalid_flights))
cleaned_flights["duration_minutes"] = (
    cleaned_flights["calculated_duration"].dt.total_seconds() / 60
)
print("\nDuration in minutes:")
print(
    cleaned_flights[
        ["flight_id", "duration_minutes"]
    ].head(20).to_string(index=False)
)
cleaned_flights = cleaned_flights.drop(
    columns=[
        "duration_clean",
        "calculated_duration"
    ]
)
print("\nFinal columns:")
print(cleaned_flights.columns.tolist())
print("\nFINAL DATA QUALITY CHECK")

print("Rows:", len(cleaned_flights))
print("Duplicate rows:", cleaned_flights.duplicated().sum())
print("Missing airlines:", cleaned_flights["airline"].isna().sum())
print("Missing flight IDs:", cleaned_flights["flight_id"].isna().sum())
print(
    "Negative durations:",
    (cleaned_flights["duration_minutes"] < 0).sum()
)
print("\nFinal airline distribution:")
print(cleaned_flights["airline"].value_counts())

cleaned_flights.to_csv(
    "output/cleaned_flights.csv",
    index=False
)

invalid_flights.to_csv(
    "output/invalid_flights.csv",
    index=False
)

print("\nFiles exported successfully.")

import os

print("\nOutput files:")
print(os.listdir("output"))

#booking
bookings = pd.read_excel(
    file_path,
    sheet_name="bookings"
)

print("\nBOOKINGS DATA")
print("Shape:", bookings.shape)

print("\nColumns:")
print(bookings.columns.tolist())

print("\nFirst 5 rows:")
print(bookings.head().to_string(index=False))


print("\nData types:")
print(bookings.dtypes)

print("\nMissing values:")
print(bookings.isnull().sum())

print("\nDuplicate rows:")
print(bookings.duplicated().sum())
print("\nPotential PII columns:")

for column in bookings.columns:
    print(column)
print("\nSample booking records:")
print(bookings.head(10).to_string(index=False))
print("\nBooking columns and unique counts:")

for column in bookings.columns:
    print(
        column,
        "->",
        bookings[column].nunique(),
        "unique values"
    )
print("\nBooking status distribution:")
print(bookings["status"].value_counts(dropna=False))
missing_status = bookings[bookings["status"].isna()].copy()

print("\nBookings with missing status:")
print(
    missing_status[
        ["booking_id", "passenger_id", "flight_id", "booking_date", "seat_number"]
    ].to_string(index=False)
)
flight_ids = set(cleaned_flights["flight_id"])

bookings_with_invalid_flight = bookings[
    ~bookings["flight_id"].isin(flight_ids)
]

print("\nBookings with flight IDs not found in cleaned flights:")
print(
    bookings_with_invalid_flight[
        ["booking_id", "passenger_id", "flight_id"]
    ].to_string(index=False)
)

print(
    "\nCount of bookings with invalid flight IDs:",
    len(bookings_with_invalid_flight)
)
print("\nBooking ID uniqueness:")
print("Total:", len(bookings))
print("Unique:", bookings["booking_id"].nunique())
print("\nPassenger ID statistics:")
print("Unique passengers:", bookings["passenger_id"].nunique())
print("\nBooking date range:")
print("Earliest:", bookings["booking_date"].min())
print("Latest:", bookings["booking_date"].max())
print("\nFuture booking dates:")
print(
    (bookings["booking_date"] > pd.Timestamp.now()).sum()
)

invalid_bookings = bookings[
    bookings["status"] == "INVALID"
].copy()

print("\nINVALID booking records:")
print(
    invalid_bookings[
        [
            "booking_id",
            "passenger_id",
            "flight_id",
            "booking_date",
            "status",
            "seat_number"
        ]
    ].to_string(index=False)
)

print("\nNumber of INVALID bookings:", len(invalid_bookings))
print("\nMissing status count:", bookings["status"].isna().sum())
print("\nMissing-status booking IDs:")
print(
    bookings.loc[
        bookings["status"].isna(),
        "booking_id"
    ].to_list()
)
passengers = pd.read_excel(
    file_path,
    sheet_name="passengers"
)

print("\nPASSENGERS DATA")
print("Shape:", passengers.shape)

print("\nColumns:")
print(passengers.columns.tolist())

print("\nFirst 5 rows:")
print(passengers.head().to_string(index=False))
booking_passenger_ids = set(bookings["passenger_id"])

missing_passengers = bookings[
    ~bookings["passenger_id"].isin(passengers["passenger_id"])
]

print("\nBookings with missing passenger records:")
print(
    missing_passengers[
        ["booking_id", "passenger_id"]
    ].to_string(index=False)
)

print(
    "\nCount:",
    len(missing_passengers)
)
print("\nPassenger data types:")
print(passengers.dtypes)

print("\nPassenger missing values:")
print(passengers.isnull().sum())

print("\nPassenger duplicates:")
print(passengers.duplicated().sum())
print("\nPassenger columns:")
for column in passengers.columns:
    print(column, "->", passengers[column].nunique(), "unique values")
missing_last_name = passengers[
    passengers["last_name"].isna()
]

print("\nPassengers with missing last name:")
print(
    missing_last_name[
        ["passenger_id", "first_name", "last_name", "age", "gender"]
    ].to_string(index=False)
)

print("\nCount:", len(missing_last_name))

# Clean passenger data
cleaned_passengers = passengers.copy()

# Handle missing last names
cleaned_passengers["last_name"] = (
    cleaned_passengers["last_name"].fillna("UNKNOWN")
)

# Check remaining missing values
print("\nMissing values after passenger cleaning:")
print(cleaned_passengers.isna().sum())

# Passenger data quality checks

print("\nPassenger rows:", len(cleaned_passengers))
print("Duplicate rows:", cleaned_passengers.duplicated().sum())
print("Duplicate passenger IDs:", cleaned_passengers["passenger_id"].duplicated().sum())
print("Minimum age:", cleaned_passengers["age"].min())
print("Maximum age:", cleaned_passengers["age"].max())
print("Gender values:", cleaned_passengers["gender"].unique())
# Check duplicate passenger IDs
duplicate_passengers = cleaned_passengers[
    cleaned_passengers["passenger_id"].duplicated(keep=False)
].sort_values("passenger_id")

print("\nDuplicate passenger IDs:")
print(duplicate_passengers.to_string(index=False))

print("\nNumber of duplicate passenger IDs:",
      duplicate_passengers["passenger_id"].nunique())
# Identify passenger IDs with conflicting duplicate records
duplicate_passenger_ids = (
    cleaned_passengers[
        cleaned_passengers["passenger_id"].duplicated(keep=False)
    ]["passenger_id"]
    .unique()
)

# Check bookings affected by duplicate passenger IDs
affected_bookings = bookings[
    bookings["passenger_id"].isin(duplicate_passenger_ids)
]

print("\nDuplicate passenger IDs:", len(duplicate_passenger_ids))
print("Bookings linked to duplicate passenger IDs:", len(affected_bookings))
print(
    "Unique affected passenger IDs:",
    affected_bookings["passenger_id"].nunique()
)

# Load payments data
payments = pd.read_excel(file_path, sheet_name="payments")

print("\nPayments shape:", payments.shape)
print("\nPayments columns:")
print(payments.columns.tolist())

print("\nPayments data types:")
print(payments.dtypes)

print("\nMissing values:")
print(payments.isna().sum())

print("\nDuplicate rows:", payments.duplicated().sum())

# Payment data quality checks

print("\nPayment amount summary:")
print(payments["amount"].describe())

print("\nPayment amount data types:")
print(payments["amount"].map(type).value_counts())

print("\nPayment methods:")
print(payments["payment_method"].value_counts(dropna=False))

# Check invalid/non-positive amounts
# Inspect non-numeric payment amounts
non_numeric_amounts = payments[
    pd.to_numeric(payments["amount"], errors="coerce").isna()
    & payments["amount"].notna()
]

print("\nNon-numeric payment amounts:")
print(non_numeric_amounts["amount"].value_counts().to_string())

print("\nNumber of non-numeric amounts:", len(non_numeric_amounts))
# Convert valid numeric amounts for quality checking
numeric_amounts = pd.to_numeric(payments["amount"], errors="coerce")

# Check for zero or negative amounts
invalid_numeric_amounts = payments[
    numeric_amounts.notna() & (numeric_amounts <= 0)
]

print("\nZero or negative payment amounts:")
print(invalid_numeric_amounts[["payment_id", "booking_id", "amount"]].to_string(index=False))

print("\nCount:", len(invalid_numeric_amounts))
# Check payment -> booking references

invalid_booking_refs = payments[
    ~payments["booking_id"].isin(bookings["booking_id"])
]

print("\nPayments with invalid booking IDs:")
print(invalid_booking_refs[["payment_id", "booking_id", "amount"]].to_string(index=False))

print("\nCount:", len(invalid_booking_refs))
# Clean payment amounts
cleaned_payments = payments.copy()

cleaned_payments["amount_clean"] = pd.to_numeric(
    cleaned_payments["amount"],
    errors="coerce"
)

# Flag payment amount quality
cleaned_payments["amount_quality"] = np.where(
    cleaned_payments["amount"].isna(),
    "MISSING",
    np.where(
        cleaned_payments["amount"].astype(str).str.upper() == "INVALID",
        "INVALID",
        "VALID"
    )
)

print("\nPayment amount quality:")
print(cleaned_payments["amount_quality"].value_counts())

print("\nValid payment amount count:",
      cleaned_payments["amount_clean"].notna().sum())
# Finalize cleaned payment table
cleaned_payments = cleaned_payments.drop(columns=["amount"])

cleaned_payments = cleaned_payments.rename(
    columns={"amount_clean": "amount"}
)

print("\nCleaned payments:")
print(cleaned_payments.head())

print("\nCleaned payment columns:")
print(cleaned_payments.columns.tolist())

print("\nMissing numeric amounts:",
      cleaned_payments["amount"].isna().sum())
# Load bookings data
bookings = pd.read_excel(file_path, sheet_name="bookings")

print("\nBookings shape:", bookings.shape)

print("\nBookings columns:")
print(bookings.columns.tolist())

print("\nBookings data types:")
print(bookings.dtypes)

print("\nMissing values:")
print(bookings.isna().sum())

print("\nDuplicate rows:", bookings.duplicated().sum())

print("\nBooking status values:")
print(bookings["status"].value_counts(dropna=False))

# Check booking -> passenger references
invalid_passenger_refs = bookings[
    ~bookings["passenger_id"].isin(passengers["passenger_id"])
]

# Check booking -> flight references
invalid_flight_refs = bookings[
    ~bookings["flight_id"].isin(cleaned_flights["flight_id"])
]

print("\nBookings with invalid passenger IDs:", len(invalid_passenger_refs))
print("Bookings with invalid flight IDs:", len(invalid_flight_refs))

if len(invalid_flight_refs) > 0:
    print("\nInvalid flight references:")
    print(
        invalid_flight_refs[
            ["booking_id", "passenger_id", "flight_id", "status"]
        ].to_string(index=False)
    )
    # Clean booking status
cleaned_bookings = bookings.copy()

cleaned_bookings["status"] = (
    cleaned_bookings["status"].fillna("UNKNOWN")
)

print("\nBooking status after cleaning:")
print(cleaned_bookings["status"].value_counts())

print("\nMissing statuses after cleaning:",
      cleaned_bookings["status"].isna().sum())
# Flag booking records with invalid flight references

cleaned_bookings["flight_reference_valid"] = (
    cleaned_bookings["flight_id"].isin(cleaned_flights["flight_id"])
)

print("\nFlight reference quality:")
print(cleaned_bookings["flight_reference_valid"].value_counts())

print("\nBookings with invalid flight references:")
print(
    cleaned_bookings[
        ~cleaned_bookings["flight_reference_valid"]
    ][["booking_id", "passenger_id", "flight_id", "status"]]
)
# Create analytics-safe passenger dataset
analytics_passengers = cleaned_passengers[
    ["passenger_id", "age", "gender"]
].copy()

print("\nAnalytics passenger columns:")
print(analytics_passengers.columns.tolist())

print("\nAnalytics passenger rows:",
      len(analytics_passengers))
# Create analytics_bookings with selected columns
analytics_bookings = cleaned_bookings[
    [
        "booking_id",
        "passenger_id",
        "flight_id",
        "booking_date",
        "status",
        "flight_reference_valid",
    ]
]

# Print columns and row count
print("Columns:", list(analytics_bookings.columns))
print("Row count:", len(analytics_bookings))
# Export cleaned datasets and anomalous records to CSV
cleaned_flights.to_csv("output/cleaned_flights.csv", index=False)
analytics_passengers.to_csv("output/analytics_passengers.csv", index=False)
analytics_bookings.to_csv("output/analytics_bookings.csv", index=False)
cleaned_payments.to_csv("output/cleaned_payments.csv", index=False)
invalid_flights.to_csv("output/invalid_flights.csv", index=False)
# Calculate the mean of the cleaned duration column
avg_duration = cleaned_flights['duration_minutes'].mean()

# Print the result formatted to 2 decimal places
print(f"Average flight duration: {avg_duration:.2f} minutes")

# Calculate route-wise flight traffic
route_traffic = (
    cleaned_flights.groupby(['source', 'destination'])
    .size()
    .reset_index(name='flight_count')
    .sort_values(by='flight_count', ascending=False)
)

# Display the resulting DataFrame
print(route_traffic)

# Alternative concise method using value_counts
airline_traffic = (
    cleaned_flights['airline']
    .value_counts()
    .reset_index(name='flight_count')
)

print(airline_traffic)

# Calculate counts
anomalous_count = len(invalid_flights)
valid_count = len(cleaned_flights)
total_count = len(flights)  # Original flights row count

# Calculate anomaly rate
anomaly_rate = (anomalous_count / total_count) * 100

# Print KPI summary
print(f"Anomalous flights: {anomalous_count}")
print(f"Valid flights: {valid_count}")
print(f"Anomaly rate: {anomaly_rate:.2f}%")

booking_status_df = (
    cleaned_bookings['status']
    .value_counts()
    .reset_index(name='booking_count')
)

print(booking_status_df)

# Calculate cancellation rate
cancelled_count = (cleaned_bookings["status"] == "CANCELLED").sum()
total_bookings = len(cleaned_bookings)

cancellation_rate = (cancelled_count / total_bookings) * 100

print(f"Cancellation rate: {cancellation_rate:.2f}%")

# Calculate total valid payment revenue
valid_payments = cleaned_payments[
    cleaned_payments["amount_quality"] == "VALID"
]

total_revenue = valid_payments["amount"].sum()

print(f"Total valid payment revenue: {total_revenue:.2f}")
# Calculate the average valid payment amount
average_payment = valid_payments["amount"].mean()

# Print the result formatted to 2 decimal places
print(f"Average valid payment amount: {average_payment:.2f}")

# Calculate total revenue grouped by payment method
revenue_by_method = (
    valid_payments.groupby("payment_method")["amount"]
    .sum()
    .reset_index(name="total_revenue")
    .sort_values("total_revenue", ascending=False)
)

# Display the resulting breakdown
print(revenue_by_method)

# Check duplicate flight IDs
duplicate_flight_ids = cleaned_flights[
    cleaned_flights["flight_id"].duplicated(keep=False)
].sort_values("flight_id")

print("\nDuplicate flight IDs:")
print(duplicate_flight_ids.to_string(index=False))

print("\nNumber of duplicate flight IDs:",
      duplicate_flight_ids["flight_id"].nunique())

# Check whether any bookings reference the duplicate flight ID
duplicate_flight_bookings = bookings[
    bookings["flight_id"] == "6F250"
]

print("\nBookings referencing 6F250:")
print(duplicate_flight_bookings.to_string(index=False))

print("\nNumber of bookings:", len(duplicate_flight_bookings))

# --- STEP 1: Identify Duplicate Flight IDs in existing cleaned_flights ---

# Boolean mask to select ALL occurrences of duplicate flight_id values (e.g., both 6F250 rows)
duplicate_ids_mask = cleaned_flights.duplicated(subset=['flight_id'], keep=False)

# Extract duplicate flight rows to append to invalid_flights
duplicate_flights = cleaned_flights[duplicate_ids_mask].copy()

# Append duplicate records to existing invalid_flights dataframe
invalid_flights = pd.concat([invalid_flights, duplicate_flights], ignore_index=True)

# Remove duplicate flight_ids from cleaned_flights
cleaned_flights = cleaned_flights[~duplicate_ids_mask].copy()


# --- STEP 2: Recalculate Booking Validity ---

cleaned_bookings['flight_reference_valid'] = cleaned_bookings['flight_id'].isin(cleaned_flights['flight_id'])


# --- STEP 3: Verification Checks ---

print(f"Cleaned flights: {len(cleaned_flights)}")                       # Expected: 1002
print(f"Invalid flight records: {len(invalid_flights)}")               # Expected: 3
print(f"Valid booking references: {cleaned_bookings['flight_reference_valid'].sum()}")       # Expected: 997
print(f"Invalid booking references: {(~cleaned_bookings['flight_reference_valid']).sum()}")  # Expected: 3

# Verify rejected flight IDs
print("\nInvalid Flight IDs in invalid_flights:")
print(invalid_flights['flight_id'].tolist())  # Expected: ['SJ192', '6F250', '6F250']

# Verify affected booking IDs
invalid_b_ids = cleaned_bookings[~cleaned_bookings['flight_reference_valid']]['booking_id'].tolist()
print("\nAffected Booking IDs:")
print(invalid_b_ids)  # Expected: ['B1235', 'B1294', 'B1636']


# --- STEP 4: Re-export to output/ ---

cleaned_flights.to_csv('output/cleaned_flights.csv', index=False)
invalid_flights.to_csv('output/invalid_flights.csv', index=False)
cleaned_bookings.to_csv('output/cleaned_bookings.csv', index=False)

analytics_bookings = cleaned_bookings[
    [
        "booking_id",
        "passenger_id",
        "flight_id",
        "booking_date",
        "status",
        "flight_reference_valid",
    ]
].copy()

analytics_bookings.to_csv(
    "output/analytics_bookings.csv",
    index=False
)

avg_duration = cleaned_flights["duration_minutes"].mean()

print(f"Final average flight duration: {avg_duration:.2f} minutes")
route_traffic = (
    cleaned_flights.groupby(["source", "destination"])
    .size()
    .reset_index(name="flight_count")
    .sort_values("flight_count", ascending=False)
)

print("\nFinal route traffic:")
print(route_traffic)
airline_traffic_final = (
    cleaned_flights["airline"]
    .value_counts()
    .reset_index(name="flight_count")
)

print("\nFinal flights by airline:")
print(airline_traffic_final)
anomalous_count = len(invalid_flights)
valid_count = len(cleaned_flights)
total_count = len(flights)

anomaly_rate = (anomalous_count / total_count) * 100

print("\nFinal anomaly KPI:")
print(f"Anomalous flights: {anomalous_count}")
print(f"Valid flights: {valid_count}")
print(f"Anomaly rate: {anomaly_rate:.2f}%")
import os

# 1. Re-evaluate flight reference validity after removing duplicate flight 6F250
cleaned_bookings['flight_reference_valid'] = cleaned_bookings['flight_id'].isin(cleaned_flights['flight_id'])

# 2. Recreate analytics_bookings with the required columns
analytics_bookings = cleaned_bookings[[
    'booking_id',
    'passenger_id',
    'flight_id',
    'booking_date',
    'status',
    'flight_reference_valid'
]].copy()

# 3. Print validation check summary
row_count = len(analytics_bookings)
valid_count = analytics_bookings['flight_reference_valid'].sum()
invalid_count = (~analytics_bookings['flight_reference_valid']).sum()

print(f"Row count: {row_count}")
print(f"Valid flight references: {valid_count}")
print(f"Invalid flight references: {invalid_count}")

invalid_ids = analytics_bookings[~analytics_bookings['flight_reference_valid']]['booking_id'].tolist()
print(f"Invalid booking IDs: {invalid_ids}")

# 4. Export directly to the relative output directory
output_dir = r"output"
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "analytics_bookings.csv")
analytics_bookings.to_csv(output_path, index=False)

print(f"Saved successfully to: {output_path}")
# Filter for valid payments only
valid_payments = cleaned_payments[
    cleaned_payments["amount_quality"] == "VALID"
]

# Calculate total revenue and average payment amount
total_valid_revenue = valid_payments["amount"].sum()
avg_valid_payment = valid_payments["amount"].mean()

# Calculate revenue split by payment method
method_revenue = valid_payments.groupby("payment_method")["amount"].sum()

# Display summary
print(f"Valid payment revenue: {total_valid_revenue:,.2f}")
print(f"Average valid payment: {avg_valid_payment:,.2f}")
print("Revenue by payment method:")
for method, amount in method_revenue.items():
    print(f"  {method}: {amount:,.2f}")