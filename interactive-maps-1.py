import pandas as pd
import plotly.express as px

# Opens mapbox public token .txt file and reads it

with open('D:\Documents\Python_Programs\interactive-maps\mapbox_tkn.txt', 'r') as f:
    mapbox_key = f.read().strip()

# reads the scraped data for popular Areas, Food/Drinks, Transportation, Lodging, and NAN

loc_df = pd.read_csv('D:\Documents\Python_Programs\interactive-maps\loc_data.csv', index_col=0)
print(loc_df.head())

# Replaces Locations with NAN data types to Miscellaneous 

loc_df.type.fillna('Misc', inplace=True)

# Displays Data types in different colors on a map that are opened in your browser or Juniper Notebook

fig = px.scatter_mapbox(loc_df, lat='lat', lon='lon', color='type') # Passes entire dataframe through .scatter_mapbox func and specifies where the data resides
fig.update_layout(mapbox_style = 'open-street-map') # Diplays using the open-street-map style
fig.show() # updates and layout

