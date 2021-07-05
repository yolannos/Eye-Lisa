import numpy as np
import pandas as pd
import pickle
import streamlit as st 
import webbrowser
import os
import pathlib

#### IMPORT UTILS
path = pathlib.Path(__file__).parent.resolve()
import sys
# adding utils to the system path
sys.path.insert(0, f'{path}/utils')
from front_utils import side_bar
from visu_house.plot_house import plot_house
from visu_house.house import House
from visu_house.tiff_manipulation import substract_dtm_dsm, mask_chm

### A INTEGRER
# cwd = os.getcwd()  # Get the current working directory (cwd)
# model = pickle.load(open(cwd+"/bg_reg.pkl", "rb"))

# ###### Just to get exactly the same columns as the one used in the model
# data = pd.read_csv("https://raw.githubusercontent.com/SamuelD005/challenge-regression/development/Data8.csv", sep=",")
# X = data.drop(["Price","Unnamed: 0","PriceperMeter"] , axis = 1)
# columns = X.columns
# #######
def main():

    st.title("Eye Lisa - Demo")
    html_temp = """
    <h2 style="color:black;text-align:left;"> Your favorite App to estimate the price of your good </h2>
    """
    st.markdown(html_temp,unsafe_allow_html=True)

    ### LIST OF ADDRESSE ###
    df_addresss = pd.read_csv("address.csv")
    list_address = df_addresss["address"].to_list()
    selected_address = st.selectbox('Please select an address:',list_address)
    

    #### SUBMIT BUTTON
    if st.button("Estimate the Price"):
        # result= model.predict(df)
        # st.success(f'The output is 1000')
        try:
            house = House(selected_address)
            print(house.tif_names)
            # dtm = f"/home/yolann/Documents/becode/projects/Eye-Lisa/src/dataset/DTM/{house.tif_names}"
            # dsm = f"/home/yolann/Documents/becode/projects/Eye-Lisa/src/dataset/DSM/{house.tif_names}"
            dtm = "/home/yolann/Documents/becode/projects/Eye-Lisa/src/dataset/DTM/156000-238000.tif"
            dsm = "/home/yolann/Documents/becode/projects/Eye-Lisa/src/dataset/DSM/156000-238000.tif"
            substract_dtm_dsm(dtm, dsm)
            shapes = [feature for feature in house.bounding_box_coordinates]
            mask_chm(shapes)
            # chm = "masked_chm.tif"
            # fig = plot_house(chm, house.house_coordinates)

            # config={"displayModeBar": True}
            # st.plotly_chart(fig, use_container_width=False, config=config)
        
        #Just because we don't have all the necessary tiffs
        except Exception as r:

            print(r)
            input_adress = "Hemelrijk 49, 2910 Essen"
            house = House(input_adress) #This is the only thing changing
            dtm = "/home/yolann/Documents/becode/projects/Eye-Lisa/src/dataset/DTM/155000-240000.tif"
            dsm = "/home/yolann/Documents/becode/projects/Eye-Lisa/src/dataset/DSM/155000-240000.tif"
            substract_dtm_dsm(dtm, dsm)
            shapes = [feature for feature in house.bounding_box_coordinates]
            mask_chm(shapes)
            chm = "masked_chm.tif"
            fig = plot_house(chm, house.house_coordinates)
            config={"displayModeBar": False, "showTips": False}
            st.plotly_chart(fig, use_container_width=True, config=config)


        # st.plotly_chart(fig, use_container_width=True)
    # st.success(f'The output is {np.expm1(result[0])}')
    

        ##### SIDEBAR #########
        side_bar(selected_address)

if __name__=='__main__':
    main()