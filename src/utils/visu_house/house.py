import numpy as np
from pyproj import Transformer, CRS
from mapbox import Geocoder

class House():

    def __init__(self, address):

        self.address = address

        self.request_data()
        self.get_tiff_names()

    def bounding_box(self):

        l, b = np.min(self.bounding_box_coordinates[0]["coordinates"][0], axis=0)
        r, t = np.max(self.bounding_box_coordinates[0]["coordinates"][0], axis=0)
        
        return l, b, r, t

    def get_tiff_names(self):
        l, b, r, t =  self.bounding_box()
        self.tiff_names = []
        x_coordinates = [l,r]
        y_coordinates = [t,b]

        for x in x_coordinates:
            for y in y_coordinates:
                
                if str(int((y)//1000*1000)) + "-" + str(int((x+1000)//1000*1000)) + ".tif" in self.tiff_names:
                    pass
                else:
                    self.tiff_names.append(str(int((y)//1000*1000)) + "-" + str(int((x+1000)//1000*1000)) + ".tif")

    def request_data(self):
        geocoder = Geocoder(access_token="pk.eyJ1IjoieW9sYW5ub3MiLCJhIjoiY2txZ3pncmU1MDcybzJ2bnh2Y3ExOXdhYiJ9.LiIcIeNaGqeRZ4W_IUcl-g")
        response = geocoder.forward(self.address)
        data = response.geojson()

        house_coordinates = data["features"][0]["geometry"]["coordinates"]
        self.full_address = data["features"][0]["place_name"]

        ####### CONVERSION OF THE ADDRESS INTO ESPG 31370 #######
        #######       AND FORMATTING INTO A GEOJSON       #######
        crs_proj = CRS("EPSG:31370")
        wgs84= CRS("EPSG:4326") 

        transformer = Transformer.from_crs(wgs84, crs_proj)
        dic = dict()
        dic["type"] = "Polygon"
        coord = []

        liste = [-1, 1, 1, -1]
        sublist = [1, 1, -1, -1]
        self.span = 150
        for i, j in zip(liste, sublist):
            lb72 = transformer.transform(house_coordinates[1], house_coordinates[0])
            coord.append((lb72[0]+(i*self.span), lb72[1]+(j*self.span)))
        
        
        self.house_coordinates = (transformer.transform(house_coordinates[1], house_coordinates[0]))

        dic["coordinates"] = [coord]

        self.bounding_box_coordinates = [dic]