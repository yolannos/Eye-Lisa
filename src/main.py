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
from front_utils import side_bar_void
from visu_house.plot_house import plot_house
from visu_house.house import House
from visu_house.tiff_manipulation import substract_dtm_dsm, mask_chm


def main():

    st.set_page_config(layout="wide",page_title='Eye Lisa', page_icon=":house:")

    col1, col2 = st.beta_columns(2)
    # col2.subheader("A webapp by Yolann Sabaux")
    html_title = html_subtitle = """
    <h1 style="color:rgb(32,32,32);text-align:left;"> Eye Lisa - Demo @<a href="https://en.wikipedia.org/wiki/Essen">Essen</a></h1>
    """
    col1.markdown(html_title,unsafe_allow_html=True)
    
    html_subtitle = """
    <h2 style="color:rgb(32,32,32);text-align:left;"> Take a look at your house!</h2>
    """
    col1.markdown(html_subtitle,unsafe_allow_html=True)


    # LIST OF ADDRESS
    df = pd.read_csv("dataset/essen_address.csv")   

    postal_code = 2910
    city_name = "Essen"
    col1.markdown('__Locality__')
    col1.info(f"{postal_code} - {city_name.upper()}")
    street_choice = df["streetname_nl"].sort_values().unique()
    selected_street = col1.selectbox('Please select an address:', street_choice)

    nb_choice = df[df["streetname_nl"] == "Albert Yssackersstraat"].sort_values(by=["house_number"])
    nb_choice = df[df["streetname_nl"] == selected_street].sort_values(by=["house_number"])
    nb_choice = nb_choice["house_number"].astype(int, errors="ignore").sort_values().to_list()
    selected_number = col1.selectbox('Please select a number:',nb_choice)

    selected_address = f"{selected_street} {selected_number}, 2910 Essen"
    # SUBMIT BUTTON
    # SIDEBAR
    df = side_bar_void(postal_code)
    if col1.button("Look at it!"):
        
        try:
            house = House(selected_address)
            dtm = f"dataset/DTM/{house.tif_names}"
            dsm = f"dataset/DSM/{house.tif_names}"
            substract_dtm_dsm(dtm, dsm)
            shapes = [feature for feature in house.bounding_box_coordinates]     
            mask_chm(shapes)
            chm = "dataset/masked_chm.tif"
            fig = plot_house(chm, house.house_coordinates)

            config={"displayModeBar": False,
                    'displaylogo': False,}
            col2.plotly_chart(fig, use_container_width=True, config=config)
            print("Everything's ok")

            html_line = '''
            <style type="text/css">
            hr {width: 85%;height: 20px;background-color: rgb(32,32,32);margin-right: auto;margin-left: auto;margin-top: 5px;margin-bottom: 5px;
            border-width: 2px;border-color: rgb(32,32,32);}
            </style>
            <hr>
            '''
            col1.markdown(html_line,unsafe_allow_html=True)

            html_subtitle_price = """
            <h2 style="color:rgb(32,32,32);text-align:left;"> Get an estimated price!</h2>
            """
            col1.markdown(html_subtitle_price,unsafe_allow_html=True)
            with col1.beta_expander(label='Expand me!'):
                cwd = os.getcwd()  # Get the current working directory (cwd)
                model = pickle.load(open(cwd+"/utils/bg_reg.pkl", "rb"))
                result = model.predict(df)
                result = round((np.expm1(result[0])//10000*10000))
                f"The price estimated is {result} euros."
        except Exception as r:
            col1.header("It looks like there was an error. Please retry or contact the administrator of the website.")
            print(f"There was the following error:{r}")

    # col1.success(f'The output is {np.expm1(result[0])}')


if __name__ == '__main__':

    main()