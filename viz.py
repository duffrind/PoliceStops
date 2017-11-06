import os
import folium
import json
from branca.colormap import linear

def generate(count_dict = {'Charlotte County': 100, 'Seminole County': 100}):
    colormap = linear.YlGn.scale(min(0, min(count_dict.values())), max(count_dict.values()))
    us_states = os.path.join('app/data', 'fl_counties.json')
    geo_json_data = json.load(open(us_states))
    m = folium.Map([27.6648, -83.5158], zoom_start=7)
    folium.GeoJson(
        geo_json_data,
        name='policestops',
        style_function=lambda feature: {
            'fillColor': colormap(count_dict.get(feature['properties']['name'], 0)),
            'color': 'black',
            'weight': 1,
            'dashArray': '5, 5',
            'fillOpacity': 0.9,
        }
    ).add_to(m)
    folium.LayerControl().add_to(m)
    m.save(os.path.join('app/templates', 'map.html'))
    #m
