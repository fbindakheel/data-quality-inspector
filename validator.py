import pandas as pd
import csv

# with open("D:/python-practice/Data_quality_website/data/data_quality_inspector_10000.csv", "r", newline="", encoding="utf-8-sig") as file:
#     reader = csv.DictReader(file)
#     load_csv = []
#     for r in reader:
#         load_csv.append(r)
#     data = pd.DataFrame(load_csv)

def find_duplicates(data, columns):
    '''Return all duplicate rows'''
    data = pd.DataFrame(data)
    invalid_duplicate_data = data[data.duplicated(subset=columns, keep=False)]
    return invalid_duplicate_data

def find_missing_values(data):
    '''return all missing values'''

    data = pd.DataFrame(data)
    data = data.map(
        lambda x: x.strip() if isinstance(x, str) else x
        )
    data = data.replace(
    ["", "unknown", "Unknown", "UNKNOWN", "N/A", "n/a", "-"],
    pd.NA
    )
    
    missing_values = data[data.isna().any(axis=1)]

    return missing_values

def find_invalid_numeric_types(data, columns):
    '''return all invalid numeric data types'''

    data = pd.DataFrame(data)
    invalid_bool = pd.DataFrame(index=data.index)
    data = data.map(
        lambda x: x.strip() if isinstance(x, str) else x
        )
    data = data.replace(
    ["", "unknown", "Unknown", "UNKNOWN", "N/A", "n/a", "-"],
    pd.NA
    )
    
    for column in columns:
        converted = pd.to_numeric(data[column], errors="coerce")
    
        invalid_bool[column] = converted.isna() & data[column].notna()
    invalid_numeric_df = data[invalid_bool.any(axis=1)]
    return invalid_numeric_df, invalid_bool


def find_invalid_date_types(data, columns, date_format):
    '''return all invalid data types'''

    data = pd.DataFrame(data)
    invalid_dates_bool = pd.DataFrame(index=data.index)
    data = data.map(
        lambda x: x.strip() if isinstance(x, str) else x
          )
    
    data = data.replace(
    ["", "unknown", "Unknown", "UNKNOWN", "N/A", "n/a", "-"],
    pd.NA
    )
    for column in columns:
        converted_date = pd.to_datetime(data[column], errors="coerce", format=date_format)
        
        invalid_dates_bool[column] = converted_date.isna() & data[column].notna()
    invalid_dates_df = data[invalid_dates_bool.any(axis=1)]
    return invalid_dates_df, invalid_dates_bool


def find_invalid_business_rules(data, rules):
    '''return all invalid business rules'''

    data = pd.DataFrame(data)
    
    
    invalid_rules_bool = pd.DataFrame(index=data.index)
    
    for i, rule in enumerate(rules):
        column = rule["column"]
        operator = rule["operator"]
        value = rule["value"]
        
        
        series = data[column].map(lambda x: x.strip() if isinstance(x, str) else x)
        
        series = series.replace(["", "unknown", "Unknown", "UNKNOWN", "N/A", "n/a", "-"], pd.NA) 
        
        if operator == "min":
            numeric = pd.to_numeric(series, errors="coerce")
            invalid = numeric.notna() & (numeric < value)
        elif operator == "max":
            numeric = pd.to_numeric(series, errors="coerce")
            invalid = numeric.notna() & (numeric > value)
        elif operator == "in":
            
            invalid = series.notna() & ~series.isin(value)
        else:
            raise ValueError(f"Unsupported rule type: {operator}")
        invalid_rules_bool[f"rule_{i}_{column}_{operator}"] = invalid
    invalid_rules_df = data[invalid_rules_bool.any(axis=1)]
    
    return invalid_rules_df, invalid_rules_bool


def find_invalid_emails(data, columns):
    '''return all invalid emails'''
    data = pd.DataFrame(data)
    
    invalid_emails_bool = pd.DataFrame(index=data.index)
    data = data.map(lambda x: x.strip() if isinstance(x, str) else x)
    data = data.replace(
        ["", "unknown", "Unknown", "UNKNOWN", "N/A", "n/a", "-"],
        pd.NA
    )
    pattern = r'^[A-Za-z0-9._-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}$'
    for column in columns:
        invalid_emails_bool[column] = data[column].notna() & ~data[column].str.match(pattern, na=False)
        
    invalid_emails_df = data[invalid_emails_bool.any(axis=1)]
    return invalid_emails_df, invalid_emails_bool

