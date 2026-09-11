# Airline-DataEngineer
End-to-end airline data engineering pipeline using Python/Pandas for data cleaning, validation, transformation and analytics, with Power BI dashboards for flight operations insights.

🔄 Overall Workflow

Raw Excel Dataset
       ↓
Data Ingestion
       ↓
Data Cleaning
       ↓
Data Transformation
       ↓
Data Validation
       ↓
Cleaned & Analytics-Ready CSV Files
       ↓
Power BI Dashboard
🎯 Project Objectives

Ingest airline data from an Excel workbook.

Identify and handle missing and inconsistent data.

Detect duplicate and invalid flight records.

Standardize airline names.

Clean and validate flight duration.

Calculate flight duration in minutes.

Handle overnight/cross-day flights correctly.

Validate booking-to-flight references.

Clean payment amounts and identify invalid values.

Create analytics-safe datasets by removing PII.

Generate cleaned datasets for Power BI reporting.

Build interactive dashboards for operational analysis.

📂 Source Dataset

The source dataset is an Excel workbook containing four sheets:

Flights

Bookings

Passengers

Payments

The raw data is ingested using Python and Pandas.

🛠️ Technologies Used

Technology	Purpose
Python	Data pipeline implementation
Pandas	Data ingestion, cleaning and transformation
NumPy	Data processing and validation
Jupyter Notebook	Pipeline documentation and execution
Power BI	Data visualization and reporting
Excel	Source data
🧹 Data Cleaning & Transformation

✈️ Flights

The flight data is processed to:

Standardize airline names using the flight ID prefix.

Convert inconsistent duration values into a consistent format.

Remove exact duplicate rows.

Identify duplicate flight IDs with conflicting information.

Detect invalid timestamps where arrival occurs before departure.

Move invalid flight records into a separate invalid_flights dataset.

Airline mapping:

AI → Air India
SJ → SpiceJet
UK → Vistara
6F → IndiGo
🎫 Bookings

The bookings data is processed to:

Fill missing booking statuses with UNKNOWN.

Validate whether each flight_id exists in the cleaned flights dataset.

Create a flight_reference_valid flag.

Create an analytics-safe booking dataset without sensitive information.

👤 Passengers

Passenger data is processed to:

Handle missing last names.

Check duplicate passenger IDs.

Create an analytics-safe passenger dataset.

Remove personally identifiable information from reporting datasets.

💳 Payments

Payment data is processed to:

Convert payment amounts to numeric values.

Identify missing and invalid amounts.

Create an amount_quality column.

Validate booking references.

Ensure only valid payment amounts are used for revenue analysis.

⏱️ Flight Duration Calculation

Flight duration is calculated using:

Duration = Arrival Time − Departure Time
The calculated duration is converted into minutes and stored in:

duration_minutes
The calculated value is compared against the original duration with a small tolerance.

🌙 Overnight Flight Handling

Flights crossing midnight are handled using complete datetime values.

For example:

Departure: 23:38
Arrival:   02:32 next day
Because the dates are included in the timestamps, normal datetime subtraction produces the correct positive duration.

Records where arrival occurs before departure are treated as invalid rather than artificially correcting the timestamp.

✅ Data Validation

The pipeline performs validation checks including:

Duplicate flight IDs

Invalid flight timestamps

Flight reference validation

Passenger reference validation

Payment-to-booking reference validation

Payment amount quality

Duration consistency

Invalid flight records are stored separately so that they are not silently discarded.

📊 Output Datasets

The pipeline generates the following datasets:

output/
│
├── cleaned_flights.csv
├── cleaned_bookings.csv
├── cleaned_payments.csv
├── analytics_passengers.csv
├── analytics_bookings.csv
└── invalid_flights.csv
Analytics-Safe Data

Personal information such as:

Passport numbers

Emergency contact names

Emergency contact phone numbers

Passenger names

is excluded from the analytics datasets used for reporting.

📈 Power BI Dashboard

The cleaned datasets are connected to Power BI to create interactive dashboards.

Key KPIs

Total Valid Flights

Total Airlines

Average Flight Duration

Total Routes

Total Bookings

Valid Flight References

Invalid Flight References

Cancellation Rate

Payment Revenue

Key Visualizations

Flights by Route

Flights by Airline

Flights by Departure Hub

Average Flight Duration by Airline

Average Flight Duration by Origin Hub

Flight Volume Over Time

Flight Status Distribution

Payment Method Breakdown

Airline Performance

Delay and Anomaly Analysis

Interactive Features

Airline slicer

Departure date range filter

Route analysis

Drill-down analysis

Interactive Power BI visuals

🏗️ Project Architecture

                  ┌─────────────────────┐
                  │   Excel Source Data │
                  │ Flights / Bookings  │
                  │ Passengers / Payments│
                  └──────────┬──────────┘
                             ↓
                  ┌─────────────────────┐
                  │   Python / Pandas   │
                  │     Ingestion       │
                  └──────────┬──────────┘
                             ↓
                  ┌─────────────────────┐
                  │ Data Cleaning &     │
                  │ Transformation      │
                  └──────────┬──────────┘
                             ↓
                  ┌─────────────────────┐
                  │ Data Validation     │
                  │ & Quality Checks    │
                  └──────────┬──────────┘
                             ↓
             ┌───────────────┴────────────────┐
             ↓                                ↓
    ┌──────────────────┐             ┌──────────────────┐
    │ Cleaned CSV Data │             │ Invalid Records  │
    └────────┬─────────┘             └──────────────────┘
             ↓
    ┌──────────────────┐
    │    Power BI      │
    │    Dashboard     │
    └──────────────────┘
📁 Repository Structure

ASG-Airlines-Data-Engineering/
│
├── README.md
│
├── data/
│   └── source/
│       └── airlines_data.xlsx
│
├── output/
│   ├── cleaned_flights.csv
│   ├── cleaned_bookings.csv
│   ├── cleaned_payments.csv
│   ├── analytics_passengers.csv
│   ├── analytics_bookings.csv
│   └── invalid_flights.csv
│
├── scripts/
│   └── airlines_data_cleaning.py
│
├── notebooks/
│   └── airlines_pipeline.ipynb
│
├── dashboard/
│   ├── airlines_dashboard.pbix
│   └── dashboard_screenshot.png
│
├── documentation/
│   └── Airlines_Data_Engineering_Documentation.docx
│
├── architecture/
│   ├── architecture_diagram.png
│   ├── data_flow_diagram.png
│   └── data_model.png
│
├── logs/
│   └── pipeline.log
│
└── requirements.txt
▶️ How to Run the Project

1. Clone the repository

git clone https://github.com/<your-username>/ASG-Airlines-Data-Engineering.git
cd ASG-Airlines-Data-Engineering
2. Install dependencies

pip install -r requirements.txt
3. Run the pipeline

python scripts/airlines_data_cleaning.py
The cleaned datasets will be generated inside the output/ folder.

4. Open the Power BI Report

Open:

dashboard/airlines_dashboard.pbix
and refresh the data if required.

📋 Requirements

The main Python libraries used are:

pandas
numpy
openpyxl
🔐 Data Privacy

The project separates analytics data from personally identifiable information.

Sensitive fields such as passport numbers, passenger names, and emergency contact details are excluded from analytics datasets used for reporting.

🚀 Future Improvements

The current pipeline runs locally using Python and Pandas.

Future improvements could include:

Azure Data Factory for automated ingestion

Azure Data Lake Storage for data storage

Azure Databricks for scalable processing

SQL/Azure SQL for structured storage

Automated pipeline scheduling

Additional data-quality checks

Automated Power BI refresh

👩‍💻 Project Deliverables

This repository contains:

✅ Complete data pipeline

✅ Python script

✅ Jupyter notebook

✅ Cleaned datasets

✅ Invalid records dataset

✅ Analytics-safe datasets

✅ Power BI report

✅ Dashboard screenshot

✅ Architecture diagram

✅ Data Flow Diagram

✅ Data Model

✅ Detailed project documentation

📌 Conclusion

This project demonstrates an end-to-end airline data engineering workflow, starting from raw Excel data and ending with analytics-ready datasets and Power BI dashboards.

The pipeline focuses on data quality, validation, transformation, privacy, and business reporting, enabling reliable analysis of flight operations, routes, bookings, payments, and airline performance.
