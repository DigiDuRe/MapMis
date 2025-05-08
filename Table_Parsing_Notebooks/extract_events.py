import pandas as pd

def parse_blocks_with_inherited_a(df):
    """
    Processes the consolidated DataFrame to extract a new DataFrame from each 6-column block.
    
    Each 6-column block (7 blocks per row) provides 4 columns: a, b, c, d.
    - a is taken from the third column of the block (i.e. block_start+2),
      and if empty, it is replaced with the value of a from the previous block for that individual.
    - b, c, and d are taken from the fourth, fifth, and sixth columns of the block.
    The individual's id is stored in the last column of the consolidated DataFrame and is included in every row.
    
    Parameters:
        df (DataFrame): Consolidated DataFrame with 43 columns (42 for data blocks and 1 for id).
    
    Returns:
        parsed_df (DataFrame): New DataFrame with columns: a, b, c, d, id.
    """
    new_records = []
    # Calculate number of blocks; last column is the id.
    num_blocks = (df.shape[1] - 1) // 6  
    id_col_index = df.shape[1] - 1  # The id column is the last column.
    
    # Iterate over each row in the consolidated DataFrame.
    for idx, row in df.iterrows():
        # Retrieve the individual's id from the last column.
        id_val = row[id_col_index]
        if pd.isnull(id_val):
            id_val = ""
        else:
            id_val = str(id_val).strip()
        
        previous_a = ""  # Will store the previous block's "a" value.
        # Process each 6-column block.
        for block in range(num_blocks):
            start_col = block * 6
            # Extract columns for the block:
            # "a" is from column index (start_col+2)
            a = row[start_col + 2]
            # Normalize a: if a is NaN or an empty string, inherit from previous block (if any)
            if pd.isnull(a) or (isinstance(a, str) and a.strip() == ""):
                a = previous_a  # previous_a may be blank if not set.
            else:
                a = str(a).strip()
                previous_a = a  # update for future blocks
            
            # Extract b, c, d from columns start_col+3, start_col+4, start_col+5.
            b = row[start_col + 3]
            c = row[start_col + 4]
            d = row[start_col + 5]
            
            # Normalize these values to strings (or blank if NaN)
            b = str(b).strip() if pd.notnull(b) else ""
            c = str(c).strip() if pd.notnull(c) else ""
            d = str(d).strip() if pd.notnull(d) else ""
            
            new_records.append({
                'a': a,
                'b': b,
                'c': c,
                'd': d,
                'id': id_val
            })
    
    parsed_df = pd.DataFrame(new_records, columns=['a', 'b', 'c', 'd', 'id'])
    return parsed_df

if __name__ == "__main__":
    # Load the updated consolidated data.
    input_file = "/Volumes/Extreme SSD/Python_Projects/NIAA Project/data/data_in_one_row_without_spouses.csv"  # Ensure this file has 43 columns.
    consolidated_df = pd.read_csv(input_file, header=None)
    
    # Process the data to extract the desired columns.
    new_df = parse_blocks_with_inherited_a(consolidated_df)
    
    # Save the new dataset.
    new_df.to_csv("/Volumes/Extreme SSD/Python_Projects/NIAA Project/FINAL_PARSED_DATA/events_data.csv", index=False)
    print("New parsed data saved as new_parsed_data.csv")