import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import folium
from streamlit_folium import folium_static
import geopandas as gpd
import base64
from folium.plugins import MarkerCluster
import branca

def app():

    st.markdown(
        """
        <style>
        .container {
            display: flex;
        }
        .logo-text {
            font-weight:700 !important;
            font-size:50px !important;
            color: #f9a01b !important;
            padding-top: 75px !important;
        }
        .logo-img {
            float: left;
            position: relative;
            margin-top: 600px;
        }
        #logo {
        position: absolute;
           float: right;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    #title
    st.markdown('---')
    st.title("Mapping Climate Change News Sentiment")

    st.sidebar.header('Choose month to view:')
    # Declare zipcode list
    state = ["ALABAMA", "ALASKA", "ARIZONA", "ARKANSAS", "CALIFORNIA",
    "COLORADO", "CONNECTICUT", "DELAWARE", "FLORIDA", "GEORGIA",
    "HAWAII", "IDAHO", "ILLINOIS", "INDIANA", "IOWA",
    "KANSAS", "KENTUCKY", "LOUISIANA", "MAINE", "MARYLAND",
    "MASSACHUSETTS", "MICHIGAN", "MINNESOTA", "MISSISSIPPI", "MISSOURI",
    "MONTANA", "NEBRASKA", "NEVADA", "NEW HAMPSHIRE", "NEW JERSEY",
    "NEW MEXICO", "NEW YORK", "NORTH CAROLINA", "NORTH DAKOTA", "OHIO",
    "OKLAHOMA", "OREGON", "PENNSYLVANIA", "RHODE ISLAND", "SOUTH CAROLINA",
    "SOUTH DAKOTA", "TENNESSEE", "TEXAS", "UTAH", "VERMONT",
    "VIRGINIA", "WASHINGTON", "WEST VIRGINIA", "WISCONSIN", "WYOMING"]

    # Put client and date options in the sidebar
    selected_state = st.sidebar.selectbox(
        'Choose state:',
        state,
        key='CALIFORNIA'
    )

    st.markdown("""
    * The [Climate Risk Viewer](https://storymaps.arcgis.com/collections/87744e6b06c74e82916b9b11da218d28?item=1) is a tool built by the Forest Service to spacially identify climate-related risks.
    * This Streamlit-based application is a new take that maps climate risk based on climate change related news articles by location.
    * A heatmap shows the quantity of climate change related articles with a negative sentiment.
    * The articles were pulled via webscraping from BBC Climate news and NASA Earth Observatory and represent news from 2010-present.
    """)

    # area_stats = pd.read_csv('data/RPMSZips.csv', dtype={'zip':str})
    area_stats = pd.read_csv('data/bbc_and_nasa_negative_article_counts_by_state.csv', dtype={'zips':str})
    area_stats['state_name'] = area_stats['state_name'].str.upper()

    articles = pd.read_csv('data/bbc_and_nasa_articles_loc_coor_sent.csv')
    articles['state_name'] = articles['state_name'].str.upper()

    # #get name of month for sunburst chart
    # area_stats['date_time'] = pd.to_datetime(area_stats['date_time'])
    # area_stats['month'] = area_stats['date_time'].dt.strftime("%B")
    # area_stats_sub = area_stats[['zipcode','month','solar_prod_mwh','real_pred_demand_mwh','percentage_demand_covered']]
    # df_groupby_month = area_stats_sub.groupby(['zipcode','month']).mean()
    # df_groupby_month = df_groupby_month.reset_index()

    # # Display dataframe on website via st.dataframe or st.write methods
    # st.write("==  scrollable dataframe after the end user has uploaded her time series file:")
    # st.dataframe(df.style.highlight_max(axis=0))

    st.markdown('---')
    st.header('Heat map of climate change news sentiment by US city')
    # view neighborhood, city by income, different groups, stats

    # reading in the polygon shapefile
    us_states = gpd.read_file(r"data/States_shapefile-shp/States_shapefile.shp")
    print(us_states.head())
    x_map= 37.0902
    y_map= -95.7129

    mymap = folium.Map(location=[x_map, y_map], zoom_start=4,tiles=None)
    folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(mymap)

    us_states_merged = pd.merge(us_states, area_stats, left_on='State_Name', right_on='state_name')
    print(us_states_merged.head())
    # us_states_merged['percentage_demand_covered'] = florida_zips_merged['percentage_demand_covered'] * 100

    #st.subheader(f'{demo} population in %')

    # view_real_estate = st.checkbox('View Industrial Locations')

    choropleth = folium.Choropleth(
     geo_data=us_states_merged,
     name='Choropleth',
     data=us_states_merged,
     columns=['State_Name','count'],
     key_on="feature.properties.State_Name",
        fill_color='Reds',
        line_weight=1,
     legend_name=f'Count of Negative Articles by State',
     smooth_factor=0
    ).add_to(mymap)

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

    # add labels indicating the name of the community
    style_function = "font-size: 15px; font-weight: bold"
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['State_Name'], style=style_function, labels=False))


    # create a layer control
    folium.LayerControl().add_to(mymap)

    folium_static(mymap, width=750, height=850)

    st.markdown('---')

    state_mask = (articles['state_name'] == selected_state)
    df_state_masked = articles[['city','state_name','Article Title','Article Link','Article Description','Published','roBERTa Negative Score']].loc[state_mask]
    st.write('Articles Assoicated with State = ')
    st.write(df_state_masked)
