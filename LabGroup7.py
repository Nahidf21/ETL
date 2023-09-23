# Import necessary libraries
import pandas as pd
import numpy as np

# Load the three datasets into pandas dataframes
dfinit= pd.read_csv("dfinit.csv")
dfup1= pd.read_csv("dfup1.csv")
dfup2= pd.read_csv("dfup2.csv")

# Split the dfup2 dataset based on the value of "form_field"
dfup2_1=dfup2[dfup2["form_field"]==1]
dfup2_2=dfup2[dfup2["form_field"]==2]

# Drop the "form_field" column and set "recordid" as the index for both split datasets
dfup2_1_drop=dfup2_1.drop(columns="form_field").set_index("recordid")
dfup2_2_drop=dfup2_2.drop(columns="form_field").set_index("recordid")

# Merge the two split datasets, with dfup2_1_drop taking precedence where overlaps occur
dfup2_merge= dfup2_1_drop.combine_first(dfup2_2_drop)

# Fill any NaN values with -1 in the merged dataset
dfup2=dfup2_merge.fillna(int(-1))

# Fill any NaN values with -1 in dfinit and dfup1, and set "recordid" as the index for both
dfinit=dfinit.fillna(-1).set_index("recordid")
dfup1=dfup1.fillna(-1).set_index("recordid")

# Load the mapping_file dataset
mapping_file= pd.read_csv("mapping_file.csv")

# Extract column names from dfinit and dfup1 datasets
dfint_col = dfinit.columns
dfup1_col = dfup1.columns

# Initialize lists to store the mapping of columns for each dataset
mapping_file_dfinit = []
mapping_file_dfup1 = []
mapping_file_dfup2 = []

# Populate the mapping lists with appropriate column names from the mapping_file dataset
for _, row in mapping_file.iterrows():
    mapping_file_dfinit.append(row["dfinit"])
    mapping_file_dfup1.append(row["dfup1"])
    mapping_file_dfup2.append(row["dfup2"])

# Rename the columns of dfup1 based on the mapping_file dataset
for col in dfup1_col:
    x = col.split("_")
    if x[0] in mapping_file_dfup1:
        index_mapping_file = mapping_file_dfup1.index(x[0])
        new_col_name = f"{mapping_file_dfup2[index_mapping_file]}_{x[1]}"
        dfup1.rename(columns={col: new_col_name}, inplace=True)

# Rename the columns of dfinit based on the mapping_file dataset
for col in dfint_col:
    x = col.split("_")
    if x[0] in mapping_file_dfinit:
        index_mapping_file = mapping_file_dfinit.index(x[0])
        new_col_name = f"{mapping_file_dfup2[index_mapping_file]}_{x[1]}"
        dfinit.rename(columns={col: new_col_name}, inplace=True)

# Load the field_index dataset
fild_index= pd.read_csv("field_index.csv")

# Filter rows in field_index where all datasets have the column set to 1, and drop the first row
fild_index = fild_index[(fild_index["dfinit"]==1) & (fild_index["dfup1"]==1) & (fild_index["dfup2"]==1)]
fild_index= fild_index.drop(0)

# Create a list of column names based on the "Code" column of the field_index dataset
fild_index_list=[]
for _, row in fild_index.iterrows():
    fild_index_list.append(row["Code"].upper())

# Filter the columns in dfinit, dfup1, and dfup2 based on the field_index_list
dfinit= dfinit[fild_index_list]
dfup1= dfup1[fild_index_list]
dfup2=dfup2[fild_index_list]

# Concatenate the three datasets into a final consolidated dataset
final_data=pd.concat([dfinit,dfup1,dfup2],ignore_index=False)
print(final_data)

# Save the final dataset to a CSV file
final_data.to_csv("labGroup7.csv",index=True)
