import requests
from datetime import datetime, timedelta

class dmi_vejr:
    def __init__(self, coord_lat, coord_lon, dmi_api_key):
        self.coord_lat = coord_lat
        self.coord_lon = coord_lon
        self.dmi_api_key = dmi_api_key

    def get_rain_wind(self):
        if self.coord_lat and self.coord_lon is None:
            coordinates = 'POINT(55.69167045976886 12.554718594176451)' 
        else:
            coordinates = f'POINT({self.coord_lat} {self.coord_lon})'

        parameters = 'wind-speed-10m,total-precipitation' 

        now = datetime.now()
        now_datetime = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

        future = now + timedelta(hours=6)
        future_datetime = future.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

        url = f'https://dmigw.govcloud.dk/v1/forecastedr/collections/harmonie_nea_sf/position?coords={coordinates}&crs=crs84&parameter-name={parameters}&datetime={now_datetime}/{future_datetime}&api-key={self.dmi_api_key}'

        response = requests.get(url)

        if response.status_code == 200:
            vejr_data = response.json()
            wind_speed = vejr_data['ranges']['wind-speed-10m']['values'][-1]
            total_precipitation = vejr_data['ranges']['total-precipitation']['values'][-1]
            return wind_speed, total_precipitation, future
        else:
            return response.status_code
        




