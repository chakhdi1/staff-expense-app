import streamlit as st
from datetime import datetime
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# App Setup
st.set_page_config(page_title="Staff Expense Tracker", page_icon="💰", layout="centered")

st.title("💰 Staff Expense Tracker")
st.write("Submit your daily business expenses here. Data syncs directly with Google Sheets.")
st.markdown("---")

# Streamlit Secrets માંથી ઓટોમેટિક લિંક ઉપાડશે
if "public_gsheets_url" in st.secrets:
    GOOGLE_SHEET_URL = st.secrets["public_gsheets_url"]
else:
    GOOGLE_SHEET_URL = None

# સ્ટાફના નામ (તમારો સાચો સ્ટાફ)
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
    elif not GOOGLE_SHEET_URL:
        st.error("❌ Google Sheet link is missing in Secrets!")
    else:
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            # ગૂગલ શીટમાંથી ડેટા રીડ કરવો
            existing_data = conn.read(spreadsheet=GOOGLE_SHEET_URL, ttl=0)
            existing_data = existing_data.dropna(how="all")
            
            new_row = pd.DataFrame([{
                "Date/Time": current_time,
                "Employee Name": selected_name,
                "Category": selected_category,
                "Description": description,
                "Amount": amount,
                "Payment Mode": selected_mode,
                "Images Uploaded": f"{len(uploaded_files)} image(s)",
                "Status": "Pending"
            }])
            
            updated_df = pd.concat([existing_data, new_row], ignore_index=True)
            # ગૂગલ શીટમાં સેવ કરવો
            conn.update(spreadsheet=GOOGLE_SHEET_URL, data=updated_df)
            st.success(f"✅ Thank you {selected_name}! Expense of ₹{amount} saved to Google Sheets.")
            st.balloons()
        except Exception as e:
            st.error(f"Connection Error: {e}")

# Admin section to view records
st.markdown("---")
if st.checkbox("👑 View Live Admin Report"):
    st.subheader("📋 Employee Expense Ledger")
    if GOOGLE_SHEET_URL:
        try:
            conn = st.connection("gsheets", type=GSheetsConnection)
            df = conn.read(spreadsheet=GOOGLE_SHEET_URL, ttl=0)
            st.dataframe(df)
        except:
            st.info("No data found or sheet is empty.")
