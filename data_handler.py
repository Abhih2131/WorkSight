import pandas as pd
import os
from datetime import datetime, date

def load_employee_data(file_path):
    """Load and clean employee master data with safe column handling."""
    print(f"🔍 Loading Employee Data from: {os.path.abspath(file_path)}")
    if not os.path.exists(file_path):
        print(f"❌ Employee Data File Not Found: {file_path}")
        return pd.DataFrame()

    try:
        df = pd.read_excel(file_path)
        df.columns = df.columns.str.strip().str.lower()
        df.fillna("", inplace=True)
        print("✅ Employee Data Loaded Successfully")
        return df
    except Exception as e:
        print(f"❌ Error Loading Employee Data: {e}")
        return pd.DataFrame()

def load_leave_data(file_path):
    """Load HRMS leave data."""
    print(f"🔍 Loading Leave Data from: {os.path.abspath(file_path)}")
    if not os.path.exists(file_path):
        print(f"❌ Leave Data File Not Found: {file_path}")
        return pd.DataFrame()

    try:
        df = pd.read_excel(file_path)
        df.columns = df.columns.str.strip().str.lower()
        df.fillna("", inplace=True)
        print("✅ Leave Data Loaded Successfully")
        return df
    except Exception as e:
        print(f"❌ Error Loading Leave Data: {e}")
        return pd.DataFrame()

def load_sales_data(file_path):
    """Load sales INR data."""
    print(f"🔍 Loading Sales Data from: {os.path.abspath(file_path)}")
    if not os.path.exists(file_path):
        print(f"❌ Sales Data File Not Found: {file_path}")
        return pd.DataFrame()

    try:
        df = pd.read_excel(file_path)
        df.columns = df.columns.str.strip().str.lower()
        df.fillna("", inplace=True)
        print("✅ Sales Data Loaded Successfully")
        return df
    except Exception as e:
        print(f"❌ Error Loading Sales Data: {e}")
        return pd.DataFrame()

def load_all_data(folder_path="data"):
    """Load all key datasets into a dictionary with deep debugging."""
    try:
        base_path = os.path.abspath(folder_path)
        print(f"🔍 Base Path: {base_path}")

        print("🔍 Loading Employee Data...")
        employee_data = load_employee_data(os.path.join(base_path, "employee_master.xlsx"))

        print("🔍 Loading Leave Data...")
        leave_data = load_leave_data(os.path.join(base_path, "HRMS_Leave.xlsx"))

        print("🔍 Loading Sales Data...")
        sales_data = load_sales_data(os.path.join(base_path, "Sales_INR.xlsx"))

        data = {
            "employee": employee_data,
            "leave": leave_data,
            "sales": sales_data
        }
        print("✅ All Data Loaded Successfully")
        return data

    except Exception as e:
        print(f"❌ Unexpected Error in load_all_data: {e}")
        raise RuntimeError(f"Data loading failed: {str(e)}")
