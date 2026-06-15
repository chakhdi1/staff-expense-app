import streamlit as st
from datetime import datetime
import os
import pandas as pd

# App Page Setup
st.set_page_config(page_title="Staff Expense Tracker", page_icon="💰", layout="centered")

st.title("💰 Staff Expense Tracker")
st.write("Submit your daily business expenses here.")
st.markdown("---")

# Excel ફાઈલનું નામ (આ તમારા ડેસ્કટોપ પર જ સેવ થશે)
EXCEL_FILE = "Staff_Expense_Data.csv"

# 1. Staff Name Dropdown (તમારા ૧૦ સેલ્સમેનના નામ અહીં લખી શકો છો)
staff_members = [
    "Select Name...", 
    "KRUNAL SHUKLA", 
    "AJAY DANGAR", 
    "AJAY PARMAR", 
    "Salesman 4", 
    "Salesman 5", 
    "Salesman 6", 
    "Salesman 7", 
    "Salesman 8", 
    "Salesman 9", 
    "Salesman 10"
]
selected_name = st.selectbox("👤 Select Employee Name:", staff_members)

# 2. Expense Category Dropdown
categories = ["Tea & Snacks", "Stationery & Printing", "Fuel & Transport", "Shop Maintenance", "Repairs", "Miscellaneous"]
selected_category = st.selectbox("📂 Expense Category:", categories)

# 3. Expense Description
description = st.text_area("📝 Expense Description:", placeholder="e.g., Tea for customers, Xerox charges, etc.")

# 4. Amount Input (ફક્ત આંકડા લખાશે)
amount = st.number_input("💵 Amount (in ₹):", min_value=0.0, step=10.0, format="%.2f")

# 5. Payment Mode Dropdown
payment_modes = ["Paid from Own Pocket", "Cash from Shop Counter", "UPI / GPay"]
selected_mode = st.selectbox("💳 How was it paid?", payment_modes)

# 6. Camera / Multiple Image Upload
uploaded_files = st.file_uploader("📷 Upload Receipt / Bill Images (Multiple Allowed):", 
                                  type=["jpg", "jpeg", "png"], 
                                  accept_multiple_files=True)

# 7. Auto Date & Time
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

st.markdown("---")

# Submit Button Logic
if st.button("📤 Submit Expense", type="primary"):
    if selected_name == "Select Name...":
        st.error("❌ Please select your name before submitting!")
    elif amount <= 0:
        st.error("❌ Please enter a valid amount!")
    elif not description:
        st.error("❌ Please write a brief description of the expense!")
    else:
        # નવો ડેટા ગોઠવવો
        new_data = {
            "Date/Time": [current_time],
            "Employee Name": [selected_name],
            "Category": [selected_category],
            "Description": [description],
            "Amount": [amount],
            "Payment Mode": [selected_mode],
            "Images Uploaded": [f"{len(uploaded_files)} image(s)"],
            "Status": ["Pending"]
        }
        new_df = pd.DataFrame(new_data)
        
        # જો ફાઈલ પહેલાથી બનેલી હોય તો એમાં નવો ડેટા નીચે ઉમેરવો
        if os.path.exists(EXCEL_FILE):
            existing_df = pd.read_csv(EXCEL_FILE)
            updated_df = pd.concat([existing_df, new_df], ignore_index=True)
            updated_df.to_csv(EXCEL_FILE, index=False)
        else:
            # નવી ફાઈલ બનાવવી
            new_df.to_csv(EXCEL_FILE, index=False)
            
        st.success(f"✅ Thank you {selected_name}! Your expense has been saved successfully.")
        st.balloons()

# --- Admin View (ફક્ત તમારા જોવા માટે) ---
st.markdown("---")
if st.checkbox("👑 View Live Admin Report"):
    st.subheader("📋 Employee Expense Ledger")
    if os.path.exists(EXCEL_FILE):
        df = pd.read_csv(EXCEL_FILE)
        st.dataframe(df)
        
        # એક્સેલ ફાઈલ ડાઉનલોડ કરવાનું બટન
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Excel Sheet", data=csv, file_name="Final_Expense_Report.csv", mime="text/csv")
    else:
        st.info("No data submitted yet.")