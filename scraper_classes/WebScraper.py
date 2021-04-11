import csv
import geopy
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

class WebScraper:
    def __init__(self, keywords):
        self.keywords = keywords
        self.csv_columns = ['name', 'search_term', 'service', 'location', 'phone', 'email', 'website', 'Latitude', 'Longitude','Distance(km)']
        self.business_list = []
        self.filename = "madagascar-business.csv"
        self.url_list = []
        self_coordinates = (-18.9100122, 47.5255809)

    def set_keywords(self, keywords):
        self.keywords = keywords

    def write_data_to_csv(self):
        try:
            with open(self.filename, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.csv_columns)
                writer.writeheader()
                for data in self.business_list:
                    writer.writerow(data)
        except IOError:
            print("I/O error")

    def append_data_to_csv(self):
        try:
            with open(self.filename, 'a') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.csv_columns)
                for data in self.business_list:
                    writer.writerow(data)
        except IOError:
            print("I/O error")

    def calc_lat_long_dist_in_csv(self):
        try:
            geolocator = Nominatim(user_agent="Thinking_Huts_webscraper")
            with open(self.filename) as csvfile:
            reader = csv.DictReader(csvfile)
            business_list = list(reader)
            for row in business_list:
                city = row['location']
                location = geolocator.geocode(city)
                try:
                    city_coordinates = (location.latitude, location.longitude)
                    dist = geodesic(self_coordinates, city_coordinates).km
                except:
                    city_coordinates = (0,0)
                    dist=0

                row['Latitude'] = location.latitude
                row['Longitude'] = location.longitude
                row['Distance(km)'] = dist

            with open(self.filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.csv_columns)
            writer.writeheader()
            for data in business_list:
                writer.writerow(data)

        except IOError:
            print("I/O error")
