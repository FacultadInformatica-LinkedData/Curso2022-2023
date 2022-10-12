from flask import Flask, render_template, request
from model import graph_DAO
from model.graph_DAO import c_building_inf

import folium
import pathlib

app = Flask(__name__)
start_coords = (40.428285284058816, -3.7070024693800345)
base_path = pathlib.Path(__file__).parents[1].resolve().as_posix()

@app.route('/')
def index():

    buildings, building_types, neighborhoods, districts, years, months = load_query_params()

    build_init_map()
    
    return render_template('index.html', 
                building=buildings, 
                building_type=building_types, 
                district=districts, 
                neighborhood=neighborhoods, 
                year=years, 
                month=months
            )

@app.route('/templates/map')
def reload_map():
    return render_template('map.html')

@app.post('/process/query')
def receive_query():
    conditions = request.get_json()
    exec_filter(clean_conditions(conditions))

    return '',201

def load_query_params():

    buildings, building_type, neighborhood, district = graph_DAO.get_buildings_inf()
    years, months = graph_DAO.get_years_months()
    
    return buildings, building_type, neighborhood, district, years, months

def exec_filter(conditions):

    observations = graph_DAO.observation_lookup(conditions)
    folium_map = folium.Map(location=start_coords, zoom_start=12)

    for build_id, observation in observations.items():
        building_inf = c_building_inf[build_id]

        folium.Marker(building_inf["location"], icon=folium.Icon(color="green", icon='map-marker', prefix='fa'), popup=build_popup(building_inf, observation)).add_to(folium_map)
    
    folium_map.save(base_path + '/app/templates/map.html')

def clean_conditions(conditions):
    
    new_conditions = dict()
    for key, value in conditions.items():
        if value != "default":
            new_conditions[key] = value

    return new_conditions
def build_init_map():

    observations = graph_DAO.get_latest_observations()
    folium_map = folium.Map(location=start_coords, zoom_start=12)

    for build_id, observation in observations.items():
        building_inf = c_building_inf[build_id]

        folium.Marker(building_inf["location"], icon=folium.Icon(color="green", icon='map-marker', prefix='fa'), popup=build_popup(building_inf, observation)).add_to(folium_map)
    
    folium_map.save(base_path + '/app/templates/map.html')

def build_popup(building, observation):

    txt = f"""
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css"
        integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

        <center><h4><b>{building.get("name")}</h4></b></center>
        <br><b>Type of building</b>
        {building.get("type")}
        <br><b>Neighborhood</b>
        {building.get("neighborhood")}
        <br><b>District</b>
        {building.get("district")}
        <br><b>Date</b>
        {observation.get("year")}-{observation.get("month")}
        <br><b>Consumption</b>
        {observation.get("value")} {observation.get("units")}
        <br><b>Type of Energy</b>
        {observation.get('type')}
        <br><b>Group of Energy</b>
        {observation.get('group')}
        
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
        integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
        crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js"
        integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"
        crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js"
        integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
        crossorigin="anonymous"></script>
        """  
    iframe = folium.IFrame(txt)
    return folium.Popup(iframe, min_width=300, max_width=300)

if __name__ == '__main__':
    app.run(debug=True)