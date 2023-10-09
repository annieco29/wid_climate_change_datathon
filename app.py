import streamlit as st
from multiapp import MultiApp
from apps import st_mapLayers # import your app modules here

app = MultiApp()

# Add all your application here
app.add_app("Choropleth Map of Negative Climate News by State", st_mapLayers.app)

# The main app
app.run()