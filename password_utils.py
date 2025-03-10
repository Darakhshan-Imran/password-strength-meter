
import re
import csv
import os
import pandas as pd
from collections import Counter

# Define the password history file
PASSWORD_HISTORY_FILE = "password_history.csv"

def check_password_strength(password):
    """
    Analyze the password and return its strength and improvement suggestions.
    """
    score = 0
    feedback = []

    # Check length
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Increase password length to at least 8 characters.")

    # Check uppercase and lowercase letters
    if re.search(r'[A-Z]', password) and re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Use both uppercase and lowercase letters.")

    # Check digits
    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("Include at least one digit (0-9).")

    # Check special characters
    if re.search(r'[!@#$%^&*]', password):
        score += 1
    else:
        feedback.append("Include at least one special character (!@#$%^&*).")

    # Determine strength level using range
    if score in range(1, 3):  # Score 1-2
        strength = "Weak"
    elif score in range(3, 4):  # Score 3-4
        strength = "Moderate"
    else:  # Score 5
        strength = "Strong"

    return strength, feedback


# def save_password_to_csv(password):
#     """
#     Saves the password to a CSV file for tracking history.
#     Ensures the header is only added once.
#     """
#     file_exists = os.path.exists(PASSWORD_HISTORY_FILE)
    
#     with open(PASSWORD_HISTORY_FILE, "a", newline="") as file:
#         writer = csv.writer(file)
        
#         # Add a header only if the file does not exist
#         if not file_exists:
#             writer.writerow(["Password"])
        
#         writer.writerow([password])

def save_password_to_csv(password):
    """
    Saves the password to a CSV file for tracking history.
    Ensures the header is only added once.
    """
    file_exists = os.path.exists(PASSWORD_HISTORY_FILE)
    
    with open(PASSWORD_HISTORY_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        
        # Add a header only if the file does not exist
        if not file_exists:
            writer.writerow(["Password"])
        
        writer.writerow([password])

# def get_password_history():
#     """
#     Reads and returns password history from the CSV file.
#     """
#     if not os.path.exists(PASSWORD_HISTORY_FILE):
#         return []
    
#     with open(PASSWORD_HISTORY_FILE, "r") as file:
#         reader = csv.reader(file)
#         next(reader, None)  # Skip header if it exists
#         return [row[0] for row in reader]

def get_password_history():
    """
    Reads and returns password history from the CSV file.
    """
    if not os.path.exists(PASSWORD_HISTORY_FILE):
        return []
    
    with open(PASSWORD_HISTORY_FILE, "r") as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip header if it exists
        return [row[0] for row in reader]

# def check_repeated_passwords():
#     """
#     Checks if any password has been used more than 10 times and returns an alert message.
#     """
#     passwords = get_password_history()
#     # print(f"Password history: {passwords}")
#     password_counts = Counter(passwords)
#     # print(f"Password counts: {password_counts}")

#     for password, count in password_counts.items():
#         if count >=5:
#             return f"⚠ ALERT: The password '{password}' has been used {count} times! Consider changing it."
    
#     return None  # No repeated passwords above the limit

def check_repeated_passwords(password):
    """
    Checks if the provided password has been used more than 5 times.
    Returns an alert message if the limit is reached.
    """
    passwords = get_password_history()
    password_counts = Counter(passwords)

    if password_counts.get(password, 0) >= 5:
        return f"⚠ ALERT: The password '{password}' has been used {password_counts[password]} times! Please try a new password."

    return None  # No repeated passwords above the limit

def convert_csv_to_excel():
    """
    Converts the password history CSV file to an Excel file and returns its path.
    """
    if not os.path.exists(PASSWORD_HISTORY_FILE):
        return None
    
    df = pd.read_csv(PASSWORD_HISTORY_FILE, header=None, names=["Passwords"])
    excel_file = "password_history.xlsx"
    df.to_excel(excel_file, index=False)
    
    return excel_file

def clear_password_history():
    """
    Clears the password history CSV file.
    """
    if os.path.exists(PASSWORD_HISTORY_FILE):
        os.remove(PASSWORD_HISTORY_FILE)
