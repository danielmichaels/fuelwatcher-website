from flask_googlemaps import Map

def mapping(resp):
    map_data = [data for data in resp]
    for data in map_data:
        region_map = Map(
            identifier="region",
            zoom=10,
            style="height:600px;width:100%;margin:0;",
            lat=data['latitude'],
            lng=data['longitude'],
            markers=[(data['latitude'], data['longitude'], data['title']) for data in
                     map_data],
            fit_markers_to_bounds=True # zooms in/out to fit all markers in box
        )
    return region_map