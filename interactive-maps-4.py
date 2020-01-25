import pandas as pd
import plotly.express as px
import os


# Opens mapbox public token .txt file and reads it
with open('D:\Documents\Python_Programs\interactive-maps\mapbox_tkn.txt', 'r') as f:
    mapbox_key = f.read().strip()


# reads the scraped data for popular Areas, Food/Drinks, Transportation, Lodging, and NAN
loc_df = pd.read_csv(
    'D:\Documents\Python_Programs\interactive-maps\loc_data.csv', index_col=0)
print(loc_df.head())


# Replaces Locations with NAN data types to Miscellaneous
loc_df.type.fillna('Misc', inplace=True)


# Compares location names to a list, including/omitting 'the' and apostrophe/quote symbol
def loc_in_list(loc, loc_list):

    loc_list = list(set([i.strip().lower()
                         for i in loc_list if len(i.strip().lower()) > 0]))
    loc_list += ['the ' + i for i in loc_list if i[:4] != 'the ']
    loc_list += [i[4:] for i in loc_list if i[:4] == 'the ']

    for t_char in ["'", "-"]:
        loc_list += [i.replace(t_char, "") for i in loc_list if t_char in i]
        loc_list += [i.replace(t_char, " ") for i in loc_list if t_char in i]

    loc = loc.replace("’", "'")
    loc = loc.strip().lower()

    loc_in_list_bool = (loc in loc_list) or (loc.replace("'", "") in loc_list)

    return loc_in_list_bool


# Count the number of times a location is mentioned in a blog and sort the resulting dataframe:
data_dir = 'data_csvs'
data_files = [i for i in os.listdir(data_dir) if i.endswith('.csv')]

for csv_file in data_files:
    with open(os.path.join(data_dir, csv_file), 'r') as f:
        locs_txt = f.read()
    temp_locs = locs_txt.split('\n')
    locs_bool = [loc_in_list(i, temp_locs) for i in list(loc_df['location'])]
    loc_df = loc_df.assign(**{csv_file: locs_bool})

loc_df = loc_df.assign(counts=loc_df[data_files].sum(axis=1))
loc_df.sort_values(by='counts', inplace=True, ascending=False)

# Fixes overlapping locations by placing the more popular locations on top
loc_df = loc_df.assign(dup_row=0)
loc_thresh = 0.0001
for i in range(len(loc_df)):
    src_ind = loc_df.iloc[i].name
    for j in range(i+1, len(loc_df)):
        tgt_ind = loc_df.iloc[j].name
        lat_dist = loc_df.loc[src_ind]['lat'] - loc_df.loc[tgt_ind]['lat']
        lon_dist = loc_df.loc[src_ind]['lon'] - loc_df.loc[tgt_ind]['lon']
        tot_dist = (lat_dist ** 2 + lon_dist ** 2) ** 0.5
        if tot_dist < loc_thresh:
            print(f'Found duplicate item "{loc_df.loc[tgt_ind]["location"]}", index {tgt_ind}')
            for csv_file in data_files:
                if loc_df.loc[tgt_ind, csv_file]:
                    loc_df.loc[src_ind, csv_file] = True
            if loc_df.loc[tgt_ind, 'location'] not in loc_df.loc[src_ind, 'location']:
                loc_df.loc[src_ind, 'location'] = loc_df.loc[src_ind, 'location'] + ' | ' + loc_df.loc[tgt_ind, 'location']
            loc_df.loc[tgt_ind, 'dup_row'] = 1

loc_df = loc_df[loc_df.dup_row == 0]
loc_df = loc_df.assign(counts=loc_df[data_files].sum(axis=1))
loc_df.sort_values(by='counts', inplace=True, ascending=False)


print(loc_df.head())


# Displays Data types in different colors on a map that are opened in your browser or Juniper Notebook
fig = px.scatter_mapbox(
    loc_df, lat="lat", lon="lon", color="type", size="counts",
    hover_name='location', hover_data=['type'], zoom=12, size_max=15)  # Passes entire dataframe through .scatter_mapbox func, specifies where the data resides, and zooms in
# Diplays using the open-street-map style, now uses Mapbox, and uses the light theme
fig.update_layout(mapbox_style="light", mapbox_accesstoken=mapbox_key)
# updates and layout
fig.show(
    config={
        'displayModeBar': False,
        'editable': False,
    },
) 
