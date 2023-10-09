import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import folium
from streamlit_folium import folium_static
import geopandas as gpd
import plotly.express as px
import base64
from folium.plugins import MarkerCluster
import branca

def app():
    # LOGO_IMAGE_IBM = "apps/ibm.png"
    # LOGO_IMAGE_U_OF_F = "apps/u_of_f.svg.png"
    # LOGO_IMAGE_BRIGHTER = "apps/brighter_potential_logo.png"

    # st.markdown(
    #     """
    #     <style>
    #     .container {
    #         display: flex;
    #     }
    #     .logo-text {
    #         font-weight:700 !important;
    #         font-size:50px !important;
    #         color: #f9a01b !important;
    #         padding-top: 75px !important;
    #     }
    #     .logo-img {
    #         float: left;
    #         position: relative;
    #         margin-top: 600px;
    #     }
    #     #logo {
    #     position: absolute;
    #        float: right;
    #     }
    #     </style>
    #     """,
    #     unsafe_allow_html=True
    # )


    #title
    st.markdown('---')
    st.title("Visualizing Climate Change News on a Map")

    # st.sidebar.header('Choose month to view:')
    # # Declare zipcode list
    # month = ['January','February','March','April','May','June','July',
    #          'August','September','October','November','December']

    # # Put client and date options in the sidebar
    # selected_month = st.sidebar.selectbox(
    #     'Choose month:',
    #     month,
    #     key='month'
    # )

    # st.markdown("""
    # * Renewables currently account for roughly only 4% of energy production in Florida.
    # * Stakeholders need to know how solar energy sources can supplement the power grid.
    # * The map below shows the percentage of energy demand that could have been produced by rooftop solar energy.
    # * This projection for 2019 is based on predictive modeling that predicts the rooftop solar energy potential and the energy demand based on the weather.
    # """)

    # area_stats = pd.read_csv('data/RPMSZips.csv', dtype={'zip':str})
    area_stats = pd.read_csv('data/articles_loc_zip_sent.csv', dtype={'zips':str})
    #st.write(area_stats.head())

    st.markdown('---')
    st.header('Heat map of climate change news sentiment by US city')
    # view neighborhood, city by income, different groups, stats

    # reading in the polygon shapefile
    us_states = gpd.read_file(r"data/us_shape_files_by_state.shp")
    print(us_states.head())
    x_map= 27.6648 
    y_map= 95.7129 

    mymap = folium.Map(location=[x_map, y_map], zoom_start=7,tiles=None)
    folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(mymap)
    #folium_static(mymap)

    #st.write(change_details.str[:2])
    #st.write(change_details['zipcode'].head())
    # change_details.rename(columns = {'zipcode':'zip_code'}, inplace= True)
    us_states_merged = pd.merge(us_states, area_stats, left_on='NAME', right_on='state_name')
    print(us_states_merged.head())

    #st.subheader(f'{demo} population in %')

    # view_real_estate = st.checkbox('View Industrial Locations')

    choropleth = folium.Choropleth(
     geo_data=us_states_merged,
     name='Choropleth',
     data=us_states_merged,
     columns=['NAME','count'],
     key_on="feature.properties.NAME",
        fill_color='Reds',
        line_weight=1,
     legend_name=f'Count of Negative Articles by State',
     smooth_factor=0
    ).add_to(mymap)

    # # add points for industrial real estate sites greater than 750,000 sqft
    # cluster = MarkerCluster().add_to(mymap)
    # style_function = "font-size: 15px; font-weight: bold"
    # #folium.Marker(location=[41.980250,-87.675000], tooltip = "<h3>RPMS</h3>", popup = 'RPMS', style=style_function).add_to(cluster)

    # # add points for student locations
    # if view_real_estate:
    #     industrial_locations = pd.read_csv('apps/florida_industrial_lat_long.csv')

    #     #industrial_owners = pd.read_csv('apps/industrial_solar.csv')
    #     lat = industrial_locations['lat'].tolist()
    #     lon = industrial_locations['long'].tolist()
    #     name = industrial_locations['reported_owner'].tolist()
    #     pred = industrial_locations['solar_prod_mw'].tolist()

    #     #st.write(industrial_locations.columns)

    #     for lt,ln,nm,pr in zip(lat,lon,name,pred):
    #         test = folium.Html(f'<b>Owner: {nm}<br>Daily Solar Production: {pr}</b>', script=True)  # i'm assuming this bit runs fine
    #         iframe = branca.element.IFrame(html=test, width=200, height=90)
    #         popup = folium.Popup(iframe, parse_html=True)
    #         folium.Marker(location=[lt, ln], radius=6, color='grey', fill_color='yellow', popup=popup).add_to(mymap)

    # # add labels indicating the name of the community
    # style_function = "font-size: 15px; font-weight: bold"
    # choropleth.geojson.add_child(
    #     folium.features.GeoJsonTooltip(['zipcode'], style=style_function, labels=False))

    # create a layer control
    folium.LayerControl().add_to(mymap)

    folium_static(mymap, width=750, height=850)



