from DMI import dmi_vejr

latitude = 55.69167045976886
longitude = 12.554718594176451
api_key = ''

dmi = dmi_vejr(latitude, longitude, api_key)

wind_speed, total_precipitation, forecast_datetime = dmi.get_rain_wind()

print(f"Forecast datetime: {forecast_datetime} ")
print(f"Wind Speed: {wind_speed} m/s")
print(f"Total Precipitation: {total_precipitation} mm")


