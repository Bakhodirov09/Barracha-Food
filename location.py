from geopy import Nominatim

async def get_location_name(latitude, longitude, lang):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.reverse((latitude, longitude), language=lang)

    location_name = location.address
    return location_name.split(",")