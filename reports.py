import pandas as pd

def duplicate_report(df, duplicates):
    
    total_rows = len(df)
    count_duplicates = len(duplicates)
    
    if total_rows == 0:
        return (0, 0, 0.0)
    
    percent_of_dupes = (count_duplicates / total_rows) * 100
    
    return total_rows, count_duplicates, percent_of_dupes


def missing_values_report(df, missing_values):
    
    total_rows = len(df)
    affected_rows = len(missing_values)
    total_missing_cells = (missing_values.isna().sum()).sum()
    
    if total_rows == 0:
        return (0, 0, 0, 0.0)
    
    percent_of_missing = (affected_rows / total_rows) * 100
    
    return total_rows, affected_rows, total_missing_cells, percent_of_missing
    
def invalid_numeric_type_report(df, invalid_numeric, invalid_bool):
    total_rows = len(df)
    affected_rows = len(invalid_numeric)
    
    total_invalid_numeric_cells = (invalid_bool.sum()).sum()
    
    if total_rows == 0:
        return (0, 0, 0, 0.0)
    
    percent_of_invalid_numeric = (affected_rows / total_rows) * 100
    
    return total_rows, affected_rows, total_invalid_numeric_cells, percent_of_invalid_numeric
    
def invalid_date_type_report(df, invalid_date, invalid_dates_bool):
    total_rows = len(df)
    affected_rows = len(invalid_date)
    total_invalid_date_cells = (invalid_dates_bool.sum()).sum()
    
    if total_rows == 0:
        return (0, 0, 0, 0.0)
    
    percent_of_invalid_date = (affected_rows / total_rows) * 100
    
    return total_rows, affected_rows, total_invalid_date_cells, percent_of_invalid_date
    
    
def business_rules_report(df, rules_df, invalid_rules_bool):
    total_rows = len(df)
    affected_rows = len(rules_df)
    total_invalid_rules_cells = (invalid_rules_bool.sum()).sum()
    if total_rows == 0:
        return (0, 0, 0, 0.0)
    
    percent_of_violations = (affected_rows / total_rows) * 100
    
    return total_rows, affected_rows, total_invalid_rules_cells, percent_of_violations
    
def invalid_emails_report(df, invalid_emails, invalid_emails_bool):
    total_rows = len(df)
    affected_rows = len(invalid_emails)
    total_invalid_emails_cells = (invalid_emails_bool.sum()).sum()
    
    
    if total_rows == 0:
        return (0, 0, 0, 0.0)
    
    percent_of_invalid_emails = (affected_rows / total_rows) * 100
    
    return total_rows, affected_rows, total_invalid_emails_cells, percent_of_invalid_emails