import pandas as pd

def remove_duplicates(data, columns):
    df = pd.DataFrame(data).copy()
    df = df.drop_duplicates(subset=columns)
    return df

def fill_missing_values(data, columns, fill_method, selected_value):
    df = pd.DataFrame(data).copy()
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x) 
    df = df.replace(["", "unknown", "Unknown", "UNKNOWN", "N/A", "n/a", "-"], pd.NA)
    for column in columns:
        mode = df[column].mode()
        df_int = pd.DataFrame()
        df_int[column] = pd.to_numeric(df[column], errors="coerce")
        if fill_method == "Mean":
            avg = df_int[column].mean()
            df[column] = df_int[column].fillna(avg)
        elif fill_method == "Median":
            median = df_int[column].median()
            df[column] = df_int[column].fillna(median)
        elif fill_method == "Mode":
            if mode.empty:
                continue
            else:
                mode_value = mode.iloc[0]
            df[column] = df[column].fillna(mode_value)
        elif fill_method == "Constant":
            df[column] = df[column].fillna(selected_value)
            
        
    return df


def fix_invalid_num_types(data, columns):
    df = pd.DataFrame(data).copy()
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
    df = df.replace(["", "unknown", "Unknown", "UNKNOWN", "N/A", "n/a", "-"], pd.NA)
    for column in columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")
        
    return df            

def fix_invalid_date_types(data, columns, date_format):
    df = pd.DataFrame(data).copy()
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
    df = df.replace(["", "unknown", "Unknown", "UNKNOWN", "N/A", "n/a", "-"], pd.NA)
    for column in columns:
        df[column] = pd.to_datetime(df[column], format=date_format, errors="coerce")
    
    return df
