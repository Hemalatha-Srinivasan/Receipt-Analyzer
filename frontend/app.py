import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from backend.parser import extract_text_from_image, extract_fields
from backend.db import init_db, insert_receipt, fetch_all_receipts, delete_receipt
from backend.utils import linear_search, sort_by_amount
import pandas as pd
import json
from frontend.charts import plot_vendor_chart

# --- Application Initialization ---

# Initialize the database and create the required table if it does not exist
init_db()

st.title("🧾 Receipt Analyzer")

# --- File Upload Section ---

# Provide uploader for JPG and PNG receipts
uploaded_file = st.file_uploader("Upload a bill/receipt (JPG or PNG)", type=['jpg', 'png'])

if uploaded_file:
    # Ensure 'data' directory exists to store uploaded files
    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", uploaded_file.name)

    # Save uploaded file to the data directory
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Display uploaded image to user
    st.image(file_path, caption="Uploaded Receipt", use_container_width=True)

    # --- OCR Language Selection ---
    # Allow user to select OCR language(s)
    lang_map = {
        "English": "eng",
        "Tamil": "tam",
        "Hindi": "hin",
        "English + Tamil + Hindi": "eng+tam+hin"
    }
    selected_lang = st.selectbox("Select OCR Language", list(lang_map.keys()))
    lang_code = lang_map[selected_lang]

    # --- OCR and Field Extraction ---
    # Extract raw text using OCR and parse out fields (vendor, date, amount, currency)
    text = extract_text_from_image(file_path, lang=lang_code)
    fields = extract_fields(text)

    # Allow user to edit and confirm extracted fields
    st.subheader("✏️ Edit Extracted Fields")
    vendor = st.text_input("Vendor", fields['vendor'])
    date = st.text_input("Date", fields['date'])
    amount = st.number_input("Amount", value=fields['amount'], step=1.0)
    currency = st.text_input("Currency", fields.get('currency', '₹'))

    # Save receipt information to the database on button click
    if st.button("💾 Save Receipt"):
        insert_receipt(vendor, date, amount)
        st.success("✅ Receipt saved to database.")
        st.rerun()

# --- Fetch and Prepare All Receipts ---

# Retrieve all receipts from the database and convert to DataFrame
data = fetch_all_receipts()
df = pd.DataFrame(data, columns=["DB_ID", "Vendor", "Date", "Amount"])
df["ID"] = range(1, len(df) + 1)

# --- Search Functionality ---

st.subheader("🔍 Search Receipts")
search_term = st.text_input("Enter vendor keyword to search")
if search_term:
    # Filter receipts by vendor keyword using a linear search
    filtered = linear_search(data, search_term)
    df = pd.DataFrame(filtered, columns=["DB_ID", "Vendor", "Date", "Amount"])
    df["ID"] = range(1, len(df) + 1)

# --- Sort Functionality ---

if st.checkbox("🔽 Sort by Amount (High to Low)"):
    # Sort receipts by amount in descending order
    original_columns = ["DB_ID", "Vendor", "Date", "Amount"]
    sorted_data = sort_by_amount(df[original_columns].to_numpy().tolist())
    df = pd.DataFrame(sorted_data, columns=original_columns)
    df["ID"] = range(1, len(df) + 1)  # Re-assign sequential ID

# --- Display All Receipts Table ---

st.subheader("📋 All Receipts")
st.dataframe(df[["ID", "Vendor", "Date", "Amount"]])

# --- Data Export Options ---

if not df.empty:
    # Allow download of receipts as CSV and JSON
    st.download_button("📤 Export as CSV", 
                       df[["Vendor", "Date", "Amount"]].to_csv(index=False), 
                       file_name="receipts.csv") 
    st.download_button("📤 Export as JSON", 
                        df[["Vendor", "Date", "Amount"]].to_json(orient="records").replace('\\/', '/'), 
                        file_name="receipts.json",
                        mime="application/json")

# # --- Receipt Deletion Section ---

st.subheader("🗑️ Delete a Receipt")
if not df.empty:
    # Allow user to select a receipt by sequential ID for deletion
    selected_id = st.selectbox("Select Receipt ID to delete", df["ID"])
    db_id_to_delete = int(df[df["ID"] == selected_id]["DB_ID"].values[0])

    if st.button("Delete Selected Receipt"):
        delete_receipt(db_id_to_delete)
        st.success(f"✅ Receipt ID {selected_id} deleted. Please refresh to see changes.")
        st.rerun()

# --- Vendor Spend Visualization ---

st.subheader("📊 Spend by Vendor")
if not df.empty:
    # Generate and display chart for spend per vendor
    fig = plot_vendor_chart(df)
    st.pyplot(fig)

# --- Aggregates Display ---

st.subheader("📈 Aggregates")
if not df.empty:
    # Calculate and display sum, mean, median, and mode of amounts
    st.markdown(f"**Total Spend:** ₹ {df['Amount'].sum():.2f}")
    st.markdown(f"**Average Spend:** ₹ {df['Amount'].mean():.2f}")
    st.markdown(f"**Median Spend:** ₹ {df['Amount'].median():.2f}")
    st.markdown(
        f"**Mode Spend:** ₹ {df['Amount'].mode().values[0] if not df['Amount'].mode().empty else 'N/A'}"
    )
