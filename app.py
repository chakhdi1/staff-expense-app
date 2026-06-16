import streamlit as st
from datetime import datetime
import os
import pandas as pd

# App Page Setup
st.set_page_config(page_title="Staff Expense Tracker", page_icon="💰", layout="centered")

st.title("💰 Staff Expense Tracker")
st.write("Submit your daily business expenses here.")
st.markdown("---")

# ગૂગલ શીટ વગર સીધો ગિટહબ પર ડેટા સેવ થશે
DATA_FILE = "expenses.csv"

# Staff Names
staff_members = ["Select Name...", "KRUNAL SHUKLA", "AJAY DANGAR", "AJAY PARMAR", "Salesman 4", "Salesman 5"]
selected_name = st.selectbox("👤 Select Employee Name:", staff_members)

categories = ["STATIONARY", "TRANSPORT", "TEA & SNACKS", "SHOP MAINTENANCE", "OTHER"]
selected_category = st.selectbox("📂 Expense Category:", categories)

description = st.text_area("📝 Expense Description:")
amount = st.number_input("💵 Amount (in ₹):", min_value=0.0, step=10.0, format="%.2f")

payment_modes = ["Paid from Own Pocket", "Cash from Shop Counter", "UPI / GPay"]
selected_mode = st.selectbox("💳 How was it paid?", payment_modes)

uploaded_files = st.file_uploader("📷 Upload Receipt / Bill Images:", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

st.markdown("---")

if st.button("📤 Submit Expense", type="primary"):
    if selected_name == "Select Name...":
        st.error("❌ Please select your name!")
    elif amount <= 0:
        st.error("❌ Please enter a valid amount!")
    else:
        # નવો ડેટા
        new_row = pd.DataFrame([{
            "Date/Time": current_time,
            "Employee Name": selected_name,
            "Category": selected_category,
            "Description": description,
            "Amount": amount,
            "Payment Mode": selected_mode,
            "Images": f"{len(uploaded_files)} image(s)"
        }])
        
        # ક્લાઉડ ફાઈલ અપડેટ કરવી
        if os.path.exists(DATA_FILE):
            df = pd.read_csv(DATA_FILE)
            df = pd.concat([df, new_row], ignore_index=True)
        else:
            df = new_row
            
        df.to_csv(DATA_FILE, index=False)
        st.success(f"✅ Thank you {selected_name}! Expense saved successfully.")
        st.balloons()

# Admin Report Section
st.markdown("---")
if st.checkbox("👑 View Live Admin Report"):
    st.subheader("📋 Employee Expense Ledger")
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        st.dataframe(df)
        
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Full Excel Sheet", data=csv_data, file_name="Expense_Report.csv", mime="text/csv")
    else:
        st.info("No data submitted yet.")
