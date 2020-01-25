import pandas as pd
import plotly.express as px

# Opens mapbox public token .txt file and reads it

with open('D:\Documents\Python_Programs\interactive-maps\mapbox_tkn.txt', 'r') as f:
    mapbox_key = f.read().strip()

# reads the scraped data for popular Areas, Food/Drinks, Transportation, Lodging, and NAN

loc_df = pd.read_csv(
    'D:\Documents\Python_Programs\interactive-maps\loc_data.csv', index_col=0)
print(loc_df.head())

# Replaces Locations with NAN data types to Miscellaneous

loc_df.type.fillna('Misc', inplace=True)

# Displays Data types in different colors on a map that are opened in your browser or Juniper Notebook

fig = px.scatter_mapbox(
    loc_df, lat="lat", lon="lon", color="type", hover_name='location', hover_data=['type'], zoom=12)  # Passes entire dataframe through .scatter_mapbox func, specifies where the data resides, and zooms in
# Diplays using the open-street-map style and now uses Mapbox
fig.update_layout(mapbox_style="light", mapbox_accesstoken=mapbox_key)
fig.show()  # updates and layout
