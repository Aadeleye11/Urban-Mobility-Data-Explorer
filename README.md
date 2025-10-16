# Train Trips Analytics Dashboard

A full-stack dashboard for analyzing train trip KPIs, vendor performance, and passenger data.  
Features interactive charts, color-coded KPIs, and advanced date filtering.

---

## Project Overview

This dashboard provides analytics for train trip data, split by vendor, with a focus on usability and actionable insights.  
It supports vendor comparison, daily/hourly breakdowns, and flexible date filtering, all in a modern dark-themed UI.

---

## Features

- **Vendor KPIs:**  
  - Total trips, average distance, duration, and passengers, split by vendor and overall totals.
  - Color-coded values (Vendor 1: blue, Vendor 2: yellow).

- **Interactive Charts:**  
  - Trips by day (line chart).
  - Trips per hour by vendor (stacked bar chart).
  - Average speed per hour by vendor (stacked bar chart).
  - Trip share by vendor (pie chart).

- **Date Filtering:**  
  - Date pickers restrict selection to available data (2016-01-01 to 2016-06-30).
  - "Apply" button updates all analytics.
  - "Clear Date Filter" resets to full range.

- **UI/UX:**  
  - Responsive dark theme.
  - Charts update instantly with filters.

---

## Architecture

- **Backend:**  
  - Python Flask REST API.
  - Endpoints for KPIs, analytics, and date range.
  - SQLite database (schema and sample dump included).
  - Date filtering supported on all endpoints.

- **Frontend:**  
  - HTML, CSS, JavaScript (no frameworks).
  - Chart.js for visualizations.
  - Dynamic tables and filter controls.
  - All API calls routed to Flask backend.

**Architecture Diagram:**  
*(See documentation.pdf for diagram and technical details.)*

---

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip
- SQLite3

### Clone or Download Project
```
git clone https://github.com/Aadeleye11/Urban-Mobility-Data-Explorer.git
```

### Optional: Create a Virtual Environment in Python
**Windows:**
```
python -m venv yourenv
yourenv\Scripts\activate
```

**macOS/Linux:**
```
python3 venv yourenv
source yourenv/bin/activate
```

### Install Dependencies
```
pip install -r requirements.txt
```

### Data Cleaning

Navigate to the backend directory, run the cleaning file to clean the train.csv file
```
cd backend
python cleaning.py
```

The cleaned csv file is then accessed by db_setup.py that create the DB using sqlite3 connector and loads the cleaned csv file to the database file (train.db)
```
python db_setup.py
```

### Backend Setup
Load the DB file from the db_setup.py file and integrate into the flask app
```
cd backend
pip install -r requirements.txt
python app.py # Make sure db_setup.py is in the file
```

### Frontend Setup

```
cd frontend
python -m http.server 8080
```
After this run the html file 

## Usage

- Select a date range using the date pickers (restricted to 2016-01-01 to 2016-06-30).
- Click "Apply" to filter all KPIs, charts, and tables.
- Click "Clear Date Filter" to reset to the full dataset.

### Video Walkthrough
Watch the video walkthrough to see how to set it up
[Demo Video](https://youtu.be/YoKBXUAnNJk)


## Documentation

- See [documentation.pdf](documentation.pdf) for:
  - System overview and requirements
  - Architecture diagrams
  - API endpoint documentation
  - Feature list with screenshots
  - Technical explanations

