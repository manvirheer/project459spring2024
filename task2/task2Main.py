import pandas as pd
from fuzzywuzzy import process

cases_df = pd.read_csv('../project_desc_files/csvs/cases_2021_train.csv')

# Drop addiontal information and source
# Drop latitude and longitude, remove date confirmation
cases_df = cases_df.drop(["latitude","longitude","date_confirmation","additional_information","source"], axis=1)
# Drop all columns with greater than 75% empty values
for series_name, series in cases_df.items():
    series_value_size = cases_df[cases_df[series_name].notna()].size
    series_value_percent = series_value_size/cases_df.size
    if series_value_percent <= 0.25:
        cases_df = cases_df.drop(series_name, axis=1)
# TODO: Replace all rows with an empty province

# Drop any rows with empty values
cases_df = cases_df.dropna()
# Clean outcome to fall within the 3 categories
custom_subset = ['Hospitalized', 'Recovered', 'Deceased']
# Function to perform fuzzy matching on the custom subset
def fuzzy_match(value, subset):
    match = process.extractOne(value, subset)
    return match[0] if match[1] >= 80 else value
outcome_subset = ['Hospitalized', 'Recovered', 'Deceased']
cases_df['outcome'] = cases_df['outcome'].apply(fuzzy_match, args=(outcome_subset,))
# Hard code mapping results?
outcome_mapping = {
    'Hospitalized': 'Hospitalized',
    'Recovered': 'Recovered',
    'Deceased': 'Deceased',
    'recovered': 'Recovered',
    'died': 'Deceased',
    'Under treatment': 'Hospitalized',
    'Receiving Treatment': 'Hospitalized',
    'Alive': 'Hospitalized',
    'discharge': 'Recovered',
    'stable': 'Hospitalized',
    'stable condition': 'Hospitalized',
    'discharged': 'Recovered',
    'death': 'Deceased',
    'Stable': 'Hospitalized',
    'Dead': 'Deceased',
    'Died': 'Deceased',
    'Death': 'Deceased',
    'Discharged from hospital': 'Recovered',
    'released from quarantine': 'Recovered',
    'Discharged': 'Recovered',
    'recovering at home 03.03.2020': 'Recovered',
    'critical condition': 'Hospitalized'
}
cases_df['outcome'] = cases_df['outcome'].map(outcome_mapping)
# 4 columns, total recovered hospitalized deceased
grouped_cases_df = cases_df.groupby(['province', 'country']).agg({
    'chronic_disease_binary': lambda x: x.value_counts().to_dict(),  
    'outcome': lambda x: x.value_counts().to_dict()
}).reset_index()
# Check for correct spellings in the countries and provinces 
# no country drop the value
# no province assign the capital province 
# Dataframe that has province and country as the primary keys with information
# Province, Country, Counts of different values
print(cases_df["outcome"].value_counts())
print(grouped_cases_df)
