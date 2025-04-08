import cartopy.crs as ccrs
import geopandas as gpd
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pandas as pd
import geopandas as gpd
import folium

# ---------------------------------------------------------------------------------------------------------------------
# in this section, write the script to load the data and complete the main part of the analysis.
# try to print the results to the screen using the format method demonstrated in the workbook

# load the necessary data here and transform to a UTM projection
roads = gpd.read_file('data_files/NI_roads.shp')
counties = gpd.read_file('data_files/Counties.shp')
wards = gpd.read_file('data_files/NI_Wards.shp')
transport = gpd.read_file('data_files/transport_data.csv')
counties = counties.to_crs(epsg=2157)
wards = wards.to_crs(epsg=2157)
tran
# your analysis goes here...
def ward_area(gdf):   #calculate area of each ward and add to dataframe
    gdf['area'] = gdf['geometry'].area
ward_area(wards)

def ward_density(gdf): # function to calculate population density
    gdf['density'] = gdf['Population']/gdf['area']
ward_density(wards)

merged = wards.merge(transport, left_on='Ward Code', right_on='Ward Code') # test code to merge transport data
merged.head()
merged['NumBus'] = merged['NumBus'].astype('int64') # convert column into integer type

def NumBus_per_capita(gdf): # function to calculate bus stops per capita
    gdf['Bus_Per_Capita'] = gdf['Population']/gdf['NumBus']
NumBus_per_capita(merged)
merged.head()
join = gpd.sjoin(counties, wards, how='inner', lsuffix='left', rsuffix='right')  #spatial join

group_wards_by_counties = join.groupby(['CountyName'])
sum_population = group_wards_by_counties['Population'].sum()
print(sum_population)
# ---------------------------------------------------------------------------------------------------------------------
# below here, you may need to modify the script somewhat to create your map.
# create a crs using ccrs.UTM() that corresponds to our CRS
ni_utm = ccrs.UTM(29)

# create a figure of size 10x10 (representing the page size in inches)
fig, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw=dict(projection=ni_utm))

# add gridlines below
gridlines = ax.gridlines(draw_labels=True,
                         xlocs=[-8, -7.5, -7, -6.5, -6, -5.5],
                         ylocs=[54, 54.5, 55, 55.5])
gridlines.right_labels = False
gridlines.bottom_labels = False

# to make a nice colorbar that stays in line with our map, use these lines:
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1, axes_class=plt.Axes)

# plot the ward data into our axis, using gdf.plot()
ward_plot = wards.plot(column='Population', ax=ax, vmin=1000, vmax=8000, cmap='viridis',
                       legend=True, cax=cax, legend_kwds={'label': 'Resident Population'})

# add county outlines in red using ShapelyFeature
county_outlines = ShapelyFeature(counties['geometry'], ni_utm, edgecolor='r', facecolor='none')
ax.add_feature(county_outlines)

def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)  # get the length of the color list
    handles = []  # create an empty list
    for ii in range(
            len(labels)):  # for each label and color pair that we're given, make an empty box to pass to our legend
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[ii % lc], edgecolor=edge, alpha=alpha))
    return handles

county_handles = generate_handles([''], ['none'], edge='r')

# add a legend in the upper left-hand corner
ax.legend(county_handles, ['County Boundaries'], fontsize=12, loc='upper left', framealpha=1)

# save the figure
fig.savefig('sample_map.png', dpi=300, bbox_inches='tight')


wards_county = join.groupby('Ward')['CountyName'].nunique() #assess how many times wards appear in multiple counties
print(wards_county) # print result
wards_notUnique = wards_county[wards_county > 1]
print(wards_notUnique)
population_notUnique = wards[wards['Ward'].isin(wards_notUnique.index)]
sum_population_notUnique = population_notUnique['Population'].sum()
print(f'population of wards that are not unique is: {sum_population_notUnique}')


max_pop = (wards['Population'].max()) #find ward with max population
max_pop_ward = wards[wards['Population'] == max_pop]
print(f"the ward with the maximum population is: {max_pop_ward['Ward']}")

min_pop = (wards['Population'].min())
min_pop_ward = wards[wards['Population'] == min_pop]
print(f'the ward with the minimum population is: {min_pop_ward['Ward']}')

NumBus_wards = wards.merge(transport, left_on='Ward Code', right_on='Ward Code')
NumBus_wards.head()