import csv
import pandas as pd
import plotly.express as px


def open_file(file_path):
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            data = [row for row in reader]
            return data
    except FileNotFoundError:
        print('File not found')
        return None
    except Exception as e:
        print(e)
        return None


# create a hashmap to the store the different countries and their respective cases
def create_hashmap_training_data(data):
    if not data:
        return {}
    hashmap = {}
    for line in data[1:]:
        country = line[3]
        if country == "" and line[2] == "Taiwan":
            country = "Taiwan"
        cases = hashmap.get(country, 0) + 1
        hashmap[country] = cases
    return hashmap


def create_hashmap_countries_continent_mapping(data):
    if not data:
        return {}
    hashmap = {}
    for line in data[1:]:
        country = line[1]
        continent = line[0]
        hashmap[country] = continent
    return hashmap


def continent_cases(hashmap_countries, hashmap_cases):
    hashmap = {}
    for country in hashmap_cases:
        continent = hashmap_countries.get(country, "Unknown")
        if country == "Burkina Faso":
            continent = "Africa"
        if country == "Cabo Verde":
            continent = "Africa"
        if country == "Eswatini":
            continent = "Africa"
        if continent == "Unknown":
            print(f'Unknown continent for {country}')
        cases = hashmap.get(continent, 0) + hashmap_cases[country]
        hashmap[continent] = cases
    return hashmap


def print_hashmap(hashmap):
    for key in hashmap:
        print(f'{key}: {hashmap[key]}')


countries_hashmap = create_hashmap_countries_continent_mapping(
    open_file('../added_reference_files/countries_continent_mapping.csv'))
cases_hashmap = create_hashmap_training_data(open_file('../../project_desc_files/csvs/cases_2021_train.csv'))

continent_cases_hashmap = continent_cases(countries_hashmap, cases_hashmap)
print_hashmap(continent_cases_hashmap)

df = pd.DataFrame(list(continent_cases_hashmap.items()), columns=['Continent', 'Cases'])
df_sorted = df.sort_values('Cases')

fig = px.bar(df_sorted, x='Cases', y='Continent', color='Cases',
             labels={'Cases': 'Number of Cases', 'Continent': 'Continent'},
             orientation='h',
             hover_data=['Cases'],
             color_continuous_scale='Reds')

fig.update_layout(title_text='COVID-19 Cases by Continent',
                  xaxis_title='Number of Cases',
                  yaxis_title='')

fig.update_xaxes(type='log')

fig.show()
