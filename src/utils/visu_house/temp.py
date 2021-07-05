from plot_house import plot_house
from house import House
from tiff_manipulation import substract_dtm_dsm, mask_chm
import pandas as pd
from rich.traceback import install
install()

import streamlit as st
from rasterio.plot import show
import rasterio

# input_adress = "Hemelrijk 49, 2910 Essen"

# house = House(input_adress)
# print(house.tif_names)

# dtm = f"/home/yolann/Documents/becode/projects/Eye-Lisa/src/dataset/DTM/{house.tif_names}"
# dsm = f"/home/yolann/Documents/becode/projects/Eye-Lisa/src/dataset/DSM/{house.tif_names}"

# print(dtm)
# print(dsm)
# substract_dtm_dsm(dtm, dsm)

# shapes = [feature for feature in house.bounding_box_coordinates]
# mask_chm(shapes)

# chm = "lidar_chm.tif"
# fig = plot_house(chm, house.house_coordinates)

# fig.show()
# st.plotly_chart(fig, use_container_width=True)

# dtm = f"/home/yolann/Documents/becode/projects/Eye-Lisa/src/dataset/DTM/merged.tif"
# src = rasterio.open(dtm)
# show(dtm)



# ## GET TIFFS
df_addresss = pd.read_csv("../../address.csv")
list_address = df_addresss["address"].to_list()


liste_jerem = []
for address in list_address:
    house = House(address)
    liste_jerem.append(house.tif_names)
print(liste_jerem)