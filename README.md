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

### Backend Setup
```
cd backend
pip install -r requirements.txt
sqlite3 ../db/sample.db < db_schema.sql
python app.py
```


### Frontend Setup
```
cd frontend
python -m http.server 8080
```








## Usage

- Select a date range using the date pickers (restricted to 2016-01-01 to 2016-06-30).
- Click "Apply" to filter all KPIs, charts, and tables.
- Click "Clear Date Filter" to reset to the full dataset.

## Video Walkthrough

- [Watch the 5-minute walkthrough](LINK_TO_VIDEO)
- *(Or embed a local video file:)*  
![Walkthrough Video](walkthrough.mp4)

---

## Documentation

- See [documentation.pdf](documentation.pdf) for:
  - System overview and requirements
  - Architecture diagrams
  - API endpoint documentation
  - Feature list with screenshots
  - Technical explanations

