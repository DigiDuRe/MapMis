import pandas as pd

def consolidate_individual_records(file_path):
    """
    Reads a CSV or Excel file with 6 columns per row, then consolidates rows for each individual.
    A new individual record is started when the first column is non-empty and does not start with "~".
    Continuation rows (empty first column or starting with "~") are appended to the previous record.
    
    Parameters:
        file_path (str): Path to the input CSV or Excel file.
        
    Returns:
        consolidated_df (DataFrame): A new DataFrame where each row contains all data for one individual.
    """
    # Read the file based on its extension.
    if file_path.lower().endswith('.csv'):
        df = pd.read_csv(file_path, header=None)
    elif file_path.lower().endswith(('.xls', '.xlsx')):
        df = pd.read_excel(file_path, header=None)
    else:
        raise ValueError("Unsupported file format. Please provide a CSV or Excel file.")

    records = []         # List to hold all individual records (each record is a list of rows).
    current_record = []  # List to accumulate rows for the current individual.
    
    # Process each row in the DataFrame.
    for index, row in df.iterrows():
        # Get the value of the first column as a string; use empty string if NaN.
        first_col = str(row[0]).strip() if pd.notnull(row[0]) else ""
        
        # New record: first column is non-empty and does not start with "~"
        if first_col and not first_col.startswith("~"):
            # If there's an existing record, append it to records before starting a new one.
            if current_record:
                records.append(current_record)
            current_record = [list(row)]
        else:
            # Continuation row: either first column is empty or starts with "~"
            # If current_record is empty (edge case), start a new record.
            if not current_record:
                current_record = [list(row)]
            else:
                current_record.append(list(row))
    
    # Append the last record if it exists.
    if current_record:
        records.append(current_record)
    
    # Consolidate each individual's multiple rows into a single row.
    consolidated_data = []
    for record in records:
        flat_row = []
        for r in record:
            flat_row.extend(r)
        consolidated_data.append(flat_row)
    
    # Create a new DataFrame with the consolidated data.
    consolidated_df = pd.DataFrame(consolidated_data)
    return consolidated_df

if __name__ == "__main__":
    # Set the input and output file paths.
    input_file = "/Volumes/Extreme SSD/Python_Projects/NIAA Project/data/data_unstructured.csv"       # Change to "input.xlsx" if using an Excel file.
    output_file = "/Volumes/Extreme SSD/Python_Projects/NIAA Project/data/data_all_one_row.csv"  # Change extension if saving as Excel.
    
    # Process the input file.
    df_consolidated = consolidate_individual_records(input_file)
    
    # Save the consolidated DataFrame to a CSV file.
    df_consolidated.to_csv(output_file, index=False, header=False)
    print(f"Consolidated data saved to {output_file}")