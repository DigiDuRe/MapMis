import pandas as pd

def is_empty(x):
    """Helper function to determine if a cell is empty after stripping whitespace."""
    return pd.isnull(x) or str(x).strip() == ""

def filter_rows(df):
    """
    Removes rows where:
      - Only the first column 'a' and the last column 'id' have data (with columns b, c, and d empty), or 
      - Only the 'id' column has data.
      
    Parameters:
        df (DataFrame): DataFrame with columns a, b, c, d, id.
        
    Returns:
        filtered_df (DataFrame): DataFrame after removing the specified rows.
    """
    # We drop a row if the id column is non-empty and all of b, c, and d are empty.
    # This covers both cases:
    # 1. Rows with data in 'a' and 'id' only.
    # 2. Rows with data only in 'id'.
    condition_drop = (
        (~df['id'].apply(is_empty)) & 
        (df['b'].apply(is_empty) & df['c'].apply(is_empty) & df['d'].apply(is_empty))
    )
    
    # Keep only rows that do NOT meet the condition to drop.
    filtered_df = df[~condition_drop].copy()
    return filtered_df

if __name__ == "__main__":
    # Read the new parsed data; assumes the file has headers: a, b, c, d, id.
    input_file = "/Volumes/Extreme SSD/Python_Projects/NIAA Project/FINAL_PARSED_DATA/events_data.csv"
    df = pd.read_csv(input_file)
    
    # Filter out rows as specified.
    filtered_df = filter_rows(df)
    
    # Save the filtered DataFrame to a new CSV file.
    output_file = "/Volumes/Extreme SSD/Python_Projects/NIAA Project/FINAL_PARSED_DATA/events_data.csv"
    filtered_df.to_csv(output_file, index=False)
    
    print(f"Filtered data saved to {output_file}")