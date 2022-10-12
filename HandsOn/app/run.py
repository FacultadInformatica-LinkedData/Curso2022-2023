from flask import Flask, render_template, request
import folium

app = Flask(__name__)
start_coords = (40.428285284058816, -3.7070024693800345)

@app.route('/')
def index():
    folium_map = folium.Map(location=start_coords, zoom_start=10)
    folium_map.save('templates/map.html')
    
    building, building_type, district, neighborhood, year, month = load_query_params()
    
    return render_template('index.html', 
                building=building, 
                building_type=building_type, 
                district=district, 
                neighborhood=neighborhood, 
                year=year, 
                month=month
            )

@app.route('/templates/map')
def reload_map():
    return render_template('map.html')

@app.post('/process/query')
def thing():
    exec_query()
    mark_map()
    print(request.get_json())
    return '',201

def load_query_params():
    pass

def exec_query():
    pass

def mark_map():
    folium_map = folium.Map(location=start_coords, zoom_start=10)
    folium_map.save('templates/map.html')


if __name__ == '__main__':
    app.run(debug=True)