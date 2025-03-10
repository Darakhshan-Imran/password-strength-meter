
import streamlit as st
import pandas as pd
import time
from password_utils import check_password_strength, save_password_to_csv, clear_password_history, check_repeated_passwords, convert_csv_to_excel, get_password_history

# Load existing history
HISTORY_FILE = "password_history.csv"

st.title("🔐 Password Strength Meter")

# Sidebar - Show history and download option
st.sidebar.title("📜 Password History")

# Load and display CSV history
try:
    df = pd.read_csv(HISTORY_FILE)
    st.sidebar.dataframe(df)

    # Provide download option
    if not df.empty:
        excel_file = convert_csv_to_excel()
        with open(excel_file, "rb") as f:
            st.sidebar.download_button("📥 Download as Excel", f, file_name="password_history.xlsx")

except FileNotFoundError:
    st.sidebar.write("No password history found.")

# **Clear History Button**
if st.sidebar.button("🗑️ Clear History"):
    clear_password_history()
    st.sidebar.success("✅ Password history cleared successfully!")
    st.rerun()  # Refresh to update history
  

# Initialize session state for password saving and alert message
if 'password_saved' not in st.session_state:
    st.session_state['password_saved'] = False
if 'alert_message' not in st.session_state:
    st.session_state['alert_message'] = None

# Input field
password = st.text_input("Enter a password:", type="password")

# Clear alert message when a new password is entered
if password:
    st.session_state['alert_message'] = None
    st.session_state['password_saved'] = False

# Buttons
if st.button("🔍 Check Password Strength"):
    if password:
        strength, feedback = check_password_strength(password)
        st.success(f"Password Strength: {strength}")
        if feedback:
            st.write(f"{feedback}")
    else:
        st.error("⚠️ Please enter a password!")

#FIRST APPROACH- MODERATELY PREFERRED

if st.button("💾 Save Password to History"):
    if password:
        alert_message = check_repeated_passwords(password)  # Check password count
        
        if alert_message:  
            st.warning(alert_message)  # Show warning message in UI
            st.stop()  # Stop execution to prevent saving the password

        if not st.session_state['password_saved']:
            save_password_to_csv(password)
            st.success("✅ Password saved successfully!")
            st.session_state['password_saved'] = True  

            time.sleep(0.5)  # Delay for 2 seconds before refreshing
            st.rerun()  # Refresh the page to update history
        else:
            st.warning("⚠️ Password already saved!")
    else:
        st.error("⚠️ Please enter a password before saving!")




