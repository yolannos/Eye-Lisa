# from plot_house import plot_house
# from house import House
# from tiff_manipulation import substract_dtm_dsm, mask_chm
# import pandas as pd
# from rich.traceback import install
# install()

# import streamlit as st
# from rasterio.plot import show
# import rasterio
# import rasterio.mask
# import rasterio.merge


# # input_adress = "Nollekensstraat 18, 2910 Essen"

# # house = House(input_adress)
# # print(house.tif_names)

# # dtm = f"/home/yolann/Documents/becode/projects/Eye-Lisa/src/dataset/DTM/{house.tif_names}"
# # dsm = f"/home/yolann/Documents/becode/projects/Eye-Lisa/src/dataset/DSM/{house.tif_names}"
# # # dtm = "/home/yolann/Documents/becode/projects/Eye-Lisa/src/dataset/DTM/155000-240000.tif"
# # # dsm = "/home/yolann/Documents/becode/projects/Eye-Lisa/src/dataset/DSM/155000-240000.tif"

# # print(dtm)
# # print(dsm)
# # substract_dtm_dsm(dtm, dsm)

# # shapes = [feature for feature in house.bounding_box_coordinates]
# # mask_chm(shapes)

# # chm = "lidar_chm.tif"
# # fig = plot_house(chm, house.house_coordinates)

# # fig.show()
# # st.plotly_chart(fig, use_container_width=True)



# liste_tif = ["/home/yolann/Documents/becode/projects/Eye-Lisa/src/dataset/DSM/145000-239000.tif", "/home/yolann/Documents/becode/projects/Eye-Lisa/src/dataset/DSM/145000-240000.tif"]

# rasterio.merge.merge(liste_tif, dst_path= "/home/yolann/Documents/becode/projects/Eye-Lisa/src/dataset/DSM/merged.tif")
# # rasterio.merge.merge(liste_tif, dst_path= "/home/yolann/Documents/becode/projects/Eye-Lisa/src/dataset/DSM/merged.tif")

# dtm = f"/home/yolann/Documents/becode/projects/Eye-Lisa/src/dataset/DTM/merged.tif"
# # dtm = "/home/yolann/Documents/becode/projects/Eye-Lisa/src/dataset/DTM/155000-240000.tif"
# src = rasterio.open(dtm)
# print(src.bounds)
# show(src)

# dsm = f"/home/yolann/Documents/becode/projects/Eye-Lisa/src/dataset/DSM/merged.tif"
# # dtm = "/home/yolann/Documents/becode/projects/Eye-Lisa/src/dataset/DTM/155000-240000.tif"
# src = rasterio.open(dsm)
# print(src.bounds)
# show(src)

# chm = f"/home/yolann/Documents/becode/projects/Eye-Lisa/src/utils/visu_house/chm.tif"
# src = rasterio.open(chm)
# print(src.bounds)
# show(src)




# # ## GET TIFFS
# # df_addresss = pd.read_csv("../../address.csv")
# # list_address = df_addresss["address"].to_list()


# # liste_jerem = []
# # for address in list_address:
# #     house = House(address)
# #     liste_jerem.append(house.tif_names)
# # print(liste_jerem)