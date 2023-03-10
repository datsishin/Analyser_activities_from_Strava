import io
import statistics
from PIL import Image
import folium
import polyline


def get_picture(load_data: dict):
    my_polyline = load_data['map']['summary_polyline']

    export_polyline = polyline.decode(my_polyline, 5)

    latitude = []
    longitude = []
    for _ in range(0, len(export_polyline)):
        latitude.append(export_polyline[_][0])
        longitude.append(export_polyline[_][1])

    avg_latitude = statistics.mean(latitude)
    avg_longitude = statistics.mean(longitude)

    min_latitude = min(latitude)
    max_latitude = max(latitude)

    min_longitude = min(longitude)
    max_longitude = max(longitude)

    center_point = [avg_latitude, avg_longitude]

    m = folium.Map(location=center_point, width=1000, height=1000)

    trail_coordinates = export_polyline

    folium.PolyLine(trail_coordinates).add_to(m)

    delta = 0.00001

    m.fit_bounds([(min_latitude + delta, min_longitude + delta),
                  (max_latitude + delta, max_longitude + delta)])

    img_data = m._to_png(1)
    img = Image.open(io.BytesIO(img_data))
    img.save('media/map.png')
