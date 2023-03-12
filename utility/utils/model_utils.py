import math
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
import qrcode
from PIL import Image, ImageDraw
from decimal import Decimal


def generate_barcode(self, generated_bar_text):
    EAN = barcode.get_barcode_class('code128')
    ean = EAN(f"{generated_bar_text}", writer=ImageWriter())
    buffer = BytesIO()
    ean.write(buffer)
    self.barcode.save(f"{generated_bar_text}.png",
                      File(buffer), save=False)


def get_code(model_name, prefix="MB"):
    obj = model_name.objects.last()
    prev_id = 0 if obj is None else obj.id
    current_id = int(prev_id) + 1
    return f"{prefix}{str(current_id).zfill(6)}"


def generate_qrcode(self, text):
    qrcode_img = qrcode.make(text)
    canvas = Image.new('RGB', (290, 290), 'white')
    canvas.paste(qrcode_img)
    fname = f'qr_code-{text}.png'
    buffer = BytesIO()
    canvas.save(buffer, 'PNG')
    self.qr_code.save(fname, File(buffer), save=False)
    canvas.close()


def get_hv_queryset(lat, lon):
    from restaurant.models import Client
    model_name = Client
    # user = request.user

    # lat = self.request.query_params.get('lat', None)
    # lon = self.request.query_params.get('long', None)

    if lat and lon:
        lat = float(lat)
        lon = float(lon)

        # Haversine formula = https://en.wikipedia.org/wiki/Haversine_formula
        R = 6378.1  # earth radius
        bearing = 1.57  # 90 degrees bearing converted to radians.
        distance = 10  # distance in km

        lat1 = math.radians(lat)  # lat in radians
        long1 = math.radians(lon)  # long in radians

        lat2 = math.asin(math.sin(lat1)*math.cos(distance/R) +
                         math.cos(lat1)*math.sin(distance/R)*math.cos(bearing))

        long2 = long1 + math.atan2(math.sin(bearing)*math.sin(distance/R)*math.cos(lat1),
                                   math.cos(distance/R)-math.sin(lat1)*math.sin(lat2))

        lat2 = math.degrees(lat2)
        long2 = math.degrees(long2)

        print(lat1, long1, lat2, long2)

        queryset = model_name.objects.filter(latitude__gte=lat1, latitude__lte=lat2).filter(
            longitude__gte=long1, longitude__lte=long2)
        

import math

def haversine(lat1, lon1, lat2, lon2):

    # import logging
    # logger = logging.getLogger('django')
    
    # logger.error(f'-----------haversine logg------------------')
    # logger.error(f'lat1 {lat1} lon1 {lon1} lat2 {lat2} lon2 {lon2}')
    try:
        lat1 = float(lat1)
        lon1 = float(lon1)
        lat2 = float(lat2)
        lon2 = float(lon2)
    except:
        return 0
    # distance between latitudes
    # and longitudes
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0
 
    # convert to radians
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0
 
    # apply formulae
    a = (pow(math.sin(dLat / 2), 2) +
         pow(math.sin(dLon / 2), 2) *
             math.cos(lat1) * math.cos(lat2))
    rad = 6371
    c = 2 * math.asin(math.sqrt(a))
    return rad * c

import requests
def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]



def get_location():
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name"),
        "latitude": response.get("latitude"),
        "longitude": response.get("longitude"),
    }
    return location_data
