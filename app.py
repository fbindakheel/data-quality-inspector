import streamlit as st 
import pandas as pd
# from loader import csv_loader
from validator import (
    find_duplicates,
    find_missing_values, 
    find_invalid_numeric_types,
    find_invalid_date_types,
    find_invalid_business_rules,
    find_invalid_emails)
from reports import (
    duplicate_report,
    missing_values_report,
    invalid_numeric_type_report,
    invalid_date_type_report,
    business_rules_report,
    invalid_emails_report
)
from cleaner import (
    remove_duplicates,
    fill_missing_values,
    fix_invalid_date_types,
    fix_invalid_num_types
)

st.set_page_config(page_title="Data Quality Inspector", page_icon="🔎", layout="wide", initial_sidebar_state="collapsed")


def apply_streamlit_style():
    st.markdown("""
    <style>
    /* App canvas and typography */
    .stApp { background: linear-gradient(135deg, #f7f9fc 0%, #eef4f9 100%); color: #18283b; }
    .block-container { max-width: 1120px; padding-top: 2.4rem; padding-bottom: 4rem; }
    h1, h2, h3 { font-family: 'Segoe UI', Arial, sans-serif; letter-spacing: -.025em; color: #15324e; }
    h1 { font-weight: 780; font-size: clamp(2rem, 4vw, 3rem); padding-bottom: .35rem; }
    h2 { border-bottom: 1px solid #dbe5ed; padding-bottom: .55rem; margin-top: 1.3rem; }
    h3 { font-weight: 680; }
    p, label { font-family: 'Segoe UI', Arial, sans-serif; }

    /* Buttons: presentation only; original button keys and behavior stay intact */
    div.stButton > button { border-radius: 12px; border: 1px solid #c9d8e6;
        background: #ffffff; color: #173a59; padding: .6rem 1.2rem;
        font-weight: 650; box-shadow: 0 2px 8px rgba(20,52,80,.055);
        transition: background-color .15s, border-color .15s, transform .15s; }
    div.stButton > button:hover { background: #e8f2fc; border-color: #2c79ae; color: #10466c; transform: translateY(-1px); }
    div.stButton > button:focus-visible { outline: 3px solid #8bc6f3; outline-offset: 2px; }

    /* Upload box, inputs and tables */
    [data-testid="stFileUploader"] { background: #ffffff; border: 1px solid #dce6ef;
        border-radius: 16px; padding: 1rem 1.2rem; box-shadow: 0 5px 18px rgba(25,60,95,.045); }
    [data-testid="stFileUploaderDropzone"] { background: #f5f9fd; border-radius: 12px; }
    [data-testid="stSelectbox"], [data-testid="stMultiSelect"], [data-testid="stNumberInput"],
    [data-testid="stTextInput"] { margin-bottom: .45rem; }
    [data-testid="stDataFrame"] { border: 1px solid #dce6ef; border-radius: 12px; overflow: hidden; }

    /* Reporting metric cards */
    [data-testid="stMetric"] { background: #ffffff; border: 1px solid #dce6ef;
        border-radius: 14px; padding: 1rem 1.25rem; margin-bottom: .45rem;
        box-shadow: 0 3px 14px rgba(25,60,95,.04); }
    [data-testid="stMetricLabel"] { color: #59728a; font-weight: 600; }
    [data-testid="stMetricValue"] { color: #153d5c; font-weight: 760; }

    /* Preserve readability in dark-mode browser preferences */
    @media (prefers-color-scheme: dark) {
        .stApp { background: #101b29; color: #e9f1f8; }
        h1, h2, h3 { color: #e9f1f8; }
        div.stButton > button, [data-testid="stMetric"], [data-testid="stFileUploader"] {
            background: #192b3c; color: #e9f1f8; border-color: #35516b; }
        [data-testid="stMetricLabel"] { color: #b7cce0; }
        [data-testid="stMetricValue"] { color: #f0f7ff; }
        [data-testid="stFileUploaderDropzone"] { background: #21374b; }
    }
    </style>
    """, unsafe_allow_html=True)


apply_streamlit_style()


def buttons():
    
    st.title("Data Quality Inspector")
    button_home = st.button("Home", key="b_home")
    button_validator = st.button("Data Quality Validator", key="b_validator")
    button_reports = st.button("Reports", key="b_reports")
    button_cleaner = st.button("Data Cleaner", key="b_cleaner")
    return button_home, button_validator, button_reports, button_cleaner
    
def file_uploader():
    st.header("Upload a Dataset")
    upload_file = st.file_uploader(
        "Upload a CSV file",
        type=["csv"]
    )
    return upload_file
    
def display_file(upload_file):
    
    try:
        df = pd.read_csv(upload_file)
        if df.empty:
            st.warning("DATASET EMPTY")
            return None
        st.header("Dataset Preview")
        st.subheader("First 10 Rows")
        st.dataframe(df.head(10))
        return df
    except pd.errors.EmptyDataError as error:
        st.error(error)
        
    
#Sections
def dupes_section(df):
    
    st.subheader("Duplicate Detection")
    
    return st.multiselect("Choose columns", options=df.columns, key="dupes")

def missing_section(df):
    
    st.subheader("Missing Values Detection")
    

def invalid_numeric_section(df):
   
    st.subheader("Invalid Numeric Types Detection")
    return st.multiselect("Choose Columns", options=df.columns, key="numeric")
      
def invalid_date_section(df):
   
    date_formats = {
    "2026-10-13 (YYYY-MM-DD)": "%Y-%m-%d",
    "13-10-2026 (DD-MM-YYYY)": "%d-%m-%Y",
    "10-13-2026 (MM-DD-YYYY)": "%m-%d-%Y",
    "2026/10/13 (YYYY/MM/DD)": "%Y/%m/%d",
    "13/10/2026 (DD/MM/YYYY)": "%d/%m/%Y",
    "10/13/2026 (MM/DD/YYYY)": "%m/%d/%Y",
    "2026-10-13 15:30:00 (Date & Time)": "%Y-%m-%d %H:%M:%S",
    "13 Oct 2026": "%d %b %Y",
    "13 October 2026": "%d %B %Y",
    "20261013 (YYYYMMDD)": "%Y%m%d"
    }
    
    st.subheader("Invalid Date Types Detection")
    select_format = st.selectbox("Select Date Format", options=list(date_formats.keys()))
    date_format = date_formats[select_format]
    columns = st.multiselect("Choose Columns", options=df.columns, key="dates")
    return columns, date_format

def business_rules_section(df):
    st.subheader("Business Rules")
    column = st.selectbox("Column", options=df.columns, key="columns")
    operator = st.selectbox("Operator", options=["min", "max", "in"], key="rules")
    if operator in ["min", "max"]:
        value = st.number_input("Value", key="value-int")
        rules = [
                {
                    "column": column,
                    "operator": operator,
                    "value": value
                }
            ]
    elif operator == "in":
        text = st.text_input("Value", key="value-str").split(",")
        value = [item.strip() for item in text if item.strip()]
        rules = [
                {
                    "column": column,
                    "operator": operator,
                    "value": value
                }
            ]
    return rules
def invalid_emails_section(df):
    st.subheader("Invalid Emails Detection")
    return st.multiselect("Select Columns", options=df.columns, key="emails")



#from validator.py
def data_validator(df):
    choice = st.selectbox (
            "Select Validator", options=[
            "Duplicate Detection", 
            "Missing Values", 
            "Invalid Numeric Types", 
            "Invalid Date Type", 
            "Business Rules", 
            "Invalid Emails"])
    
    if choice == "Duplicate Detection":
        columns_dupes = dupes_section(df)
        if columns_dupes:
            dupes_df = find_duplicates(df, columns_dupes)
            st.dataframe(dupes_df)
        
    elif choice == "Missing Values":
            missing_section(df)
            st.dataframe(find_missing_values(df))
            
    elif choice == "Invalid Numeric Types":
        columns_invalid_num = invalid_numeric_section(df)
        if columns_invalid_num:
                numeric_df, numeric_mask = find_invalid_numeric_types(df, columns_invalid_num)
                st.dataframe(numeric_df)
                
    elif choice == "Invalid Date Type":
        columns_invalid_dates, date_format = invalid_date_section(df)
        if columns_invalid_dates:
                date_df, date_mask = find_invalid_date_types(df, columns_invalid_dates, date_format)
                st.dataframe(date_df)
                
    elif choice == "Business Rules":
        rules = business_rules_section(df)
        if rules != []:
            rules_df, rules_mask = find_invalid_business_rules(df, rules)
            st.dataframe(rules_df)
            
    elif choice == "Invalid Emails":
        columns_invalid_emails = invalid_emails_section(df)
        if columns_invalid_emails:
            emails_df, emails_mask = find_invalid_emails(df, columns_invalid_emails)
            st.dataframe(emails_df)



#from reports.py
def data_reports(df):
    choice = st.selectbox("Select Report:", 
                          options=["Duplicate Report",
                                   "Missing Report", 
                                   "Invalid Numeric Report",  
                                   "Invalid Dates Report", 
                                   "Business Rules Report", 
                                   "Invalid Emails Report"])
    
    
    if choice == "Duplicate Report":
        columns_dupes = dupes_section(df)
        if columns_dupes:
            dupes_df = find_duplicates(df, columns_dupes)
            total_rows_dupes, count_duplicates, percent_of_dupes = duplicate_report(df, dupes_df)
            st.metric("Total Rows", total_rows_dupes)
            st.metric("Duplicates", count_duplicates)
            st.metric("% of Duplicates", f"{round(percent_of_dupes, 2)}%")
            
            
    elif choice == "Missing Report":
        columns_missing = missing_section(df)
        missing_df = find_missing_values(df)
        total_rows_missing, affected_rows_missing, total_missing_cells, percent_of_missing = missing_values_report(df, missing_df)
        st.metric("Total Rows", total_rows_missing)
        st.metric("Affected Rows", affected_rows_missing)
        st.metric("Missing Values", total_missing_cells)
        st.metric("% of Missing Values", f"{round(percent_of_missing, 2)}%")
        
        
    elif choice == "Invalid Numeric Report":
        columns_numeric = invalid_numeric_section(df)
        if columns_numeric:
            numeric_df, numeric_mask = find_invalid_numeric_types(df, columns_numeric)
            total_rows_numeric, affected_rows_numeric, total_invalid_numeric_cells, percent_of_invalid_numeric = invalid_numeric_type_report(
                df,
                numeric_df, 
                numeric_mask)
            st.metric("Total Rows", total_rows_numeric)
            st.metric("Affected Rows", affected_rows_numeric)
            st.metric("Invalid Numeric Values", total_invalid_numeric_cells)
            st.metric("% of Invalid Numeric Values", f"{round(percent_of_invalid_numeric, 2)}%")
            
        
    elif choice == "Invalid Dates Report":
        columns_date, date_format = invalid_date_section(df)
        if columns_date:
            dates_df, dates_mask = find_invalid_date_types(df, columns_date, date_format)
            total_rows_dates, affected_rows_dates, total_invalid_date_cells, percent_of_invalid_date = invalid_date_type_report(
                df, 
                dates_df,   
                dates_mask)
            st.metric("Total Rows", total_rows_dates)
            st.metric("Affected Rows", affected_rows_dates)
            st.metric("Invalid Date Values", total_invalid_date_cells)
            st.metric("% of Invalid Date Values", f"{round(percent_of_invalid_date, 2)}%")
            
        
    elif choice == "Business Rules Report":
        columns_rules = business_rules_section(df)
        if columns_rules:
            rules_df, rules_mask = find_invalid_business_rules(df, columns_rules)
            total_rows_rules, affected_rows_rules, total_invalid_rules_cells, percent_of_violations = business_rules_report(
                df, 
                rules_df, 
                rules_mask)
            st.metric("Total Rows", total_rows_rules)
            st.metric("Affected Rows", affected_rows_rules)
            st.metric("Violations", total_invalid_rules_cells)
            st.metric("% of Violations", f"{round(percent_of_violations, 2)}%")
            
            
    elif choice == "Invalid Emails Report":
        columns_emails = invalid_emails_section(df)
        if columns_emails:
            emails_df, emails_mask = find_invalid_emails(df, columns_emails)
            total_rows_emails, affected_rows_emails, total_invalid_emails_cells, percent_of_invalid_emails = invalid_emails_report(
                df, 
                emails_df, 
                emails_mask)
            st.metric("Total Rows", total_rows_emails)
            st.metric("Affected Rows", affected_rows_emails)
            st.metric("Invalid Email Values", total_invalid_emails_cells)
            st.metric("% of Invalid Emails", f"{round(percent_of_invalid_emails, 2)}%")

#from cleaner.py
def data_cleaner(df):
    choice = st.selectbox("Choose Method: ", options=([
        "Remove Duplicates",
        "Fill Missing Values",
        "Fix Invalid Num Types",
        "Fix Invalid Date Types"
    ]))
    
    if choice == "Remove Duplicates":
        columns_dupes = dupes_section(df)
        if columns_dupes:
            cleaned_df = remove_duplicates(df, columns_dupes)
            st.session_state["cleaned_df"] = cleaned_df
            st.dataframe(cleaned_df)
            
    elif choice == "Fill Missing Values":
        columns_missing = st.multiselect("Select Columns", options=df.columns, key="missing")
        fill_method = st.selectbox("Select your fill method: ", options=(["Mean", "Median", "Mode", "Constant"]), key="fill_method")
        selected_value = None
        if fill_method == "Constant":
            selected_value = st.text_input("Type the Value you want to be Filled: ")
        if columns_missing:
            cleaned_df = fill_missing_values(df, columns_missing, fill_method, selected_value)
            st.session_state["cleaned_df"] = cleaned_df
            st.dataframe(cleaned_df)
            
    elif choice == "Fix Invalid Num Types":
        columns_num = invalid_numeric_section(df)
        if columns_num:
            cleaned_df = fix_invalid_num_types(df, columns_num)
            st.session_state["cleaned_df"] = cleaned_df
            st.dataframe(cleaned_df)
            
    elif choice == "Fix Invalid Date Types":
        columns_date, date_format = invalid_date_section(df)
        if columns_date:
            cleaned_df = fix_invalid_date_types(df, columns_date, date_format)
            st.session_state["cleaned_df"] = cleaned_df
            st.dataframe(cleaned_df)
        
    
#UI
if "page" not in st.session_state:
    st.session_state["page"] = "home"
    
button_home, button_validator, button_reports, button_cleaner = buttons()

upload_file = file_uploader()
if not upload_file:
    st.info("Please Upload a File")

if button_validator:
    st.session_state["page"] = "validator"
if st.session_state["page"] == "validator":
    if upload_file:
        df = display_file(upload_file)
        
        if df is not None:
            st.header("Data Validator")
            data_validator(df)
            
if button_reports:
    st.session_state["page"] = "reports"
if st.session_state["page"] == "reports":
    if upload_file:
        df = display_file(upload_file)
        
        if df is not None:
            st.header("Reports")
            data_reports(df)
            
if button_cleaner: 
    st.session_state["page"] = "cleaner"
if st.session_state["page"] == "cleaner":
    if upload_file:
        df = display_file(upload_file)
        
        if df is not None:
            st.header("Data Cleaner")
            if "cleaned_df" not in st.session_state:
                st.session_state["cleaned_df"] = df.copy()
            data_cleaner(st.session_state["cleaned_df"])
            
            
                
    
        
    
    
    
    
