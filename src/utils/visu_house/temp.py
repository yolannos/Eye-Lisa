from plot_house import plot_house
from house import House
from tiff_manipulation import substract_dtm_dsm, mask_chm

import streamlit as st

input_adress = "Hemelrijk 49, 2910 Essen"

house = House(input_adress)
print(house.address)

dtm = "/home/yolann/Documents/becode/projects/Eye-Lisa/src/dataset/DTM/155000-240000.tif"
dsm = "/home/yolann/Documents/becode/projects/Eye-Lisa/src/dataset/DSM/155000-240000.tif"

substract_dtm_dsm(dtm, dsm)

shapes = [feature for feature in house.bounding_box_coordinates]
mask_chm(shapes)

chm = "lidar_chm.tif"
fig = plot_house(chm, house.house_coordinates)

st.plotly_chart(fig, use_container_width=True)