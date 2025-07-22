# Receipt Analyzer – Python Full Stack Project

Analyze bills and receipts with OCR and generate visual spend insights.

## Features

-  Upload '.jpg' / '.png' receipts
-  OCR text extraction (supports **English**, **Tamil**, **Hindi**)
-  Auto-extract **Vendor**, **Date**, and **Amount**
-  Save data into **SQLite** local database
-  View parsed data, **filter/search**, and **sort**
-  Visualize spend trends by **vendor**
-  Delete receipts from database
-  Export data as **CSV** or **JSON**


## Technologies Used

-  Python 3.10
-  Streamlit – frontend dashboard
-  Tesseract OCR – for text extraction
-  SQLite – lightweight database
-  Pandas & Matplotlib – data handling & charts
-  Upload a receipt image (.jpg, .png)

##  Installation & Setup

## Clone the Repository

git clone https://github.com/Hemalatha-Srinivasan/receipt-analyzer.git
cd receipt-analyzer

## Install Required Packages

pip install -r requirements.txt

## Install Tesseract OCR Engine

Windows:
Download from  https://github.com/UB-Mannheim/tesseract/wiki

Add Tesseract path to System Environment Variables, e.g.:
C:\Program Files\Tesseract-OCR

## Run the App
streamlit run frontend/app.py

Then open your browser to http://localhost:8501

## Project Structure

receipt-analyzer/
│
├── backend/
│   ├── db.py           # Database functions (insert, fetch, delete)
│   ├── parser.py       # OCR + field extraction logic
│   ├── utils.py        # Search and sorting utilities
│
├── frontend/
│   ├── app.py          # Main Streamlit dashboard
│   ├── charts.py       # Spend chart visualization
│
├── data/               # Uploaded image storage
├── requirements.txt    # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # Project documentation

## User Journey

-  Upload a receipt image (.jpg, .png)
-  Choose OCR language
-  Extracted text is auto-parsed into structured fields
-  User can verify/edit vendor, date, amount
-  Save to SQLite

## View all receipts:
-  Search by vendor
-  Sort by amount
-  Visualize spend trends
-  Delete records if needed
-  Export as .csv or .json

## Design Choices

-  Streamlit – Fast UI development and interaction
-  Tesseract – Multilingual OCR (supports Indian scripts)
-  Rule-based parsing – Lightweight, easy to customize
-  SQLite – Serverless, local, and easy to maintain
- Modular architecture – Separate files for each functionality

## Limitations

-  OCR may fail on blurry/complex receipts
-  Rule-based parser may miss edge cases
-   No login/authentication (local only)
-   File & DB stored locally (not cloud-based)
-   Not intended for production use – internal/intern use only

## Assumptions

-  Tesseract is installed and properly configured
-  Python 3.9 or above is installed
-  Used on desktop environment
-  Receipts follow a general standard format

## Created By
Hemalatha S
Python Intern Assignment 
22-July-2025
GitHub: github.com/Hemalatha-Srinivasan
