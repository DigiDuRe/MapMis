import pandas as pd

def extract_spouse_info(consolidated_df):
    """
    Extracts spouse information from a consolidated DataFrame that has 43 columns.
    The first 42 columns are arranged in blocks of 6 columns (7 blocks), each representing 
    an original row from the old dataset. The 43rd column (last column) contains the individual's id.
    
    For each 6-column block, if the first column starts with "~", the value (spouse information)
    is extracted along with the id from the 43rd column. The spouse cell is then cleared.
    
    Parameters:
        consolidated_df (DataFrame): The DataFrame with 43 columns.
        
    Returns:
        updated_consolidated_df (DataFrame): The modified DataFrame with spouse info cleared.
        spouse_df (DataFrame): A new DataFrame with two columns: 'spouse' and 'id'.
    """
    spouse_records = []  # To store extracted spouse information.
    # There are 43 columns; the last column holds the id.
    id_col_index = consolidated_df.shape[1] - 1  # Column index for id.
    num_blocks = (consolidated_df.shape[1] - 1) // 6  # Number of 6-column blocks.
    
    # Process each row in the consolidated DataFrame.
    for row_idx in consolidated_df.index:
        # Retrieve and clean up the id value.
        id_val = consolidated_df.at[row_idx, id_col_index]
        if pd.isnull(id_val):
            id_val = ""
        else:
            id_val = str(id_val).strip()
        
        # Iterate over each 6-column block.
        for block in range(num_blocks):
            start_col = block * 6  # First column of the block.
            spouse_info = consolidated_df.at[row_idx, start_col]
            if pd.isnull(spouse_info):
                spouse_info = ""
            else:
                spouse_info = str(spouse_info).strip()
                
            # Check if the cell contains spouse info (starts with "~")
            if spouse_info.startswith("~"):
                spouse_records.append({'spouse': spouse_info, 'id': id_val})
                # Clear the spouse info from the consolidated DataFrame.
                consolidated_df.at[row_idx, start_col] = ""
                
    spouse_df = pd.DataFrame(spouse_records)
    return consolidated_df, spouse_df

if __name__ == "__main__":
    # Load the consolidated data.
    # This CSV should have 43 columns: 42 for data blocks (7 blocks of 6 columns)
    # and the 43rd column for the individual's id.
    input_file = "/Volumes/Extreme SSD/Python_Projects/NIAA Project/data/data_all_one_row.csv"
    consolidated_df = pd.read_csv(input_file, header=None)
    
    # Extract spouse info and update the consolidated DataFrame.
    updated_consolidated_df, spouse_df = extract_spouse_info(consolidated_df)
    
    # Save the updated DataFrame and the spouse DataFrame.
    updated_consolidated_df.to_csv("/Volumes/Extreme SSD/Python_Projects/NIAA Project/data/data_in_one_row_without_spouses.csv", index=False, header=False)
    spouse_df.to_csv("/Volumes/Extreme SSD/Python_Projects/NIAA Project/FINAL_PARSED_DATA/spouse_data.csv", index=False)
    
    print("Spouse extraction complete. Files 'updated_consolidated_data.csv' and 'spouse_data.csv' have been saved.")