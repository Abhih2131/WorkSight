import pandas as pd
import os
from datetime import datetime, date

def load_employee_data(file_path):
    """Load and clean employee master data with safe column handling."""
    print(f"🔍 Loading Employee Data from: {file_path}")
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip().str.lower()
    df.fillna("", inplace=True)

    # Convert dates if columns exist
    if 'date_of_birth' in df.columns:
        df['date_of_birth'] = pd.to_datetime(df['date_of_birth'], errors='coerce')
        df['age'] = df['date_of_birth'].apply(lambda dob: calculate_age(dob))
    if 'date_of_joining' in df.columns:
        df['date_of_joining'] = pd.to_datetime(df['date_of_joining'], errors='coerce')
        df['tenure'] = df['date_of_joining'].apply(lambda doj: calculate_tenure(doj))
    if 'date_of_exit' in df.columns:
        df['date_of_exit'] = pd.to_datetime(df['date_of_exit'], errors='coerce')

    print("✅ Employee Data Loaded Successfully")
    return df

def load_leave_data(file_path):
    """Load HRMS leave data."""
    print(f"🔍 Loading Leave Data from: {file_path}")
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip().str.lower()
    df.fillna("", inplace=True)
    print("✅ Leave Data Loaded Successfully")
    return df

def load_sales_data(file_path):
    """Load sales INR data."""
    print(f"🔍 Loading Sales Data from: {file_path}")
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip().str.lower()
    df.fillna("", inplace=True)
    print("✅ Sales Data Loaded Successfully")
    return df

def calculate_age(dob):
    if pd.isnull(dob): return None
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

def calculate_tenure(doj):
    if pd.isnull(doj): return None
    today = date.today()
    return round((pd.Timestamp(today) - doj).days / 365, 2)

def load_all_data(folder_path="data"):
    """Load all key datasets into a dictionary with deep debugging."""
    try:
        base_path = os.path.abspath(folder_path)
        print(f"🔍 Base Path: {base_path}")

        # Debugging each file load
        print("🔍 Loading Employee Data...")
        employee_data = load_employee_data(os.path.join(base_path, "employee_master.xlsx"))
        print("✅ Employee Data Loaded")

        print("🔍 Loading Leave Data...")
        leave_data = load_leave_data(os.path.join(base_path, "HRMS_Leave.xlsx"))
        print("✅ Leave Data Loaded")

        print("🔍 Loading Sales Data...")
        sales_data = load_sales_data(os.path.join(base_path, "Sales_INR.xlsx"))
        print("✅ Sales Data Loaded")

        data = {
            "employee": employee_data,
            "leave": leave_data,
            "sales": sales_data
        }
        print("✅ All Data Loaded Successfully")
        return data

    except FileNotFoundError as fe:
        print(f"❌ FileNotFoundError: {fe}")
        raise RuntimeError(f"Data loading failed - File not found: {str(fe)}")
    except pd.errors.EmptyDataError as ee:
        print(f"❌ EmptyDataError: {ee}")
        raise RuntimeError(f"Data loading failed - Empty file or invalid format: {str(ee)}")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        raise RuntimeError(f"Data loading failed: {str(e)}")
