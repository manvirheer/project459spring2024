import pandas as pd

cases_df = pd.read_csv('../project_desc_files/csvs/cases_2021_train.csv')

cases_age_size = cases_df[cases_df['age'].notna()].size
cases_sex_size = cases_df[cases_df['sex'].notna()].size
cases_province_size = cases_df[cases_df['province'].notna()].size

# Drop all columns with greater than 75% empty values
# Drop any province data empty values
# Drop addiontal information and source
# Drop latitude and longitude, remove date confirmation
# Clean outcome to fall within the 3 categories
# 4 columns, total recovered hospitalized deceased
# Check for correct spellings in the countries and provinces 
# no country drop the value
# no province assign the capital province 
# Dataframe that has province and country as the primary keys with information
print(cases_age_size / cases_df.size)
print(cases_sex_size / cases_df.size)
print(cases_province_size / cases_df.size)
print(cases_df.size)
# for series_name, series in cases_df.items():
#    print(series.value_counts())