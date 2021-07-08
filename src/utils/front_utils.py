import numpy as np
import pandas as pd
import pickle
import streamlit as st 
import webbrowser
import os
import pandas as pd


# cwd = os.getcwd()  # Get the current working directory (cwd)
# model = pickle.load(open(cwd+"/utils/bg_reg.pkl", "rb"))
#
# # To get exactly the same columns as the one used in the model
# data = pd.read_csv("https://raw.githubusercontent.com/SamuelD005/challenge-regression/development/Data8.csv", sep=",")
# X = data.drop(["Price", "Unnamed: 0", "PriceperMeter"], axis = 1)
# columns = X.columns


def side_bar(address):
    with st.sidebar:
        # LIST OF ADDRESS
        df = pd.read_csv("dataset/info_house.csv")
        df = df.dropna(subset=["property_location_number"])
        df["property_location_number"] = df["property_location_number"].astype(int)
        df["address"] = df["property_location_street"].astype(str) + " " + df["property_location_number"].astype(str) + ", " + df["property_location_postalCode"].astype(str) + " " + df["property_location_locality"].astype(str)
        
        df_address = df[df["address"] == address]
        
        # Type of property
        type_of_property = df_address["property_type"]
        st.header(f'Information about the {type_of_property.values[0].capitalize()}:')

        locality = df_address["property_location_postalCode"].values[0]

        # Number of rooms
        number_of_room = df_address["property_bedroomCount"].values[0]
        st.markdown('__Number of bedrooms:__')
        st.info(number_of_room)

        # Surface of the house
        area = int(df_address["property_netHabitableSurface"].values[0])
        st.markdown('__Habitable Surface:__')
        st.info(f'{area} m2')

        '''
        - State of the building - 
        we translate the wording from immoweb which is raw. 
        !should be deleted if working with clean db
        '''
        dic_state = {"AS_NEW":" new", "JUST_RENOVATED": "new", "TO_BE_DONE_UP" : "to renovate", "GOOD" : "good"} 
        # st.selectbox('What is the state of your house?', ["good", "medium", "to renovate", "new"])
        if isinstance(df_address["property_building_condition"].values[0], str):
            state_of_building = dic_state[df_address["property_building_condition"].values[0]]
            st.markdown('__Building condition:__')
            st.info(f'{state_of_building.capitalize()}')
        else:  
            state_of_building = "medium" #This is the default value for the model to run
        
        # Equipped Kitchen
        if isinstance(df_address["property_kitchen_type"].values[0], str):
            fully_equipped_kitchen = "Yes"
            st.markdown('__Equipped kitchen?__')
            st.info(f'{fully_equipped_kitchen.capitalize()}')
        else:
            fully_equipped_kitchen = "No"
            st.markdown('__Equipped kitchen?__')
            st.info(f'{fully_equipped_kitchen.capitalize()}')
                       
        # Furnished !!!WARNING!!! Must change the DATASET SAM JE YO NO FURNISHED OPTION
        furnished = "No" # set to default but influence the result of the model

        # Open Fire
        open_fire = df_address["property_fireplaceExists"].values[0]
        open_fire_display = "Yes" if open_fire == 1 else "No"
        st.markdown('__Fire place?__')
        st.info(f'{open_fire_display.capitalize()}')

        st.header('Outdoor informations:')
        
        # Terrace Area
        if isinstance(df_address["property_terraceSurface"].values[0], int):
            terrace_area = df_address["property_terraceSurface"].values[0]
        else:
            terrace_area = 0

        terrace_area_display = terrace_area if terrace_area > 0 else "No terrace"
        st.markdown('__Terrace area:__')
        if terrace_area_display == "No terrace":
            st.info(f'{terrace_area_display}')
        else:
            st.info(f'{terrace_area_display} m2')

        # Garden Area
        # garden_area = st.number_input("Enter the area of your garden", min_value= 0, max_value = 100000000) #not in dataset

        # number_of_facades = st.selectbox('What is the number of facades?', [2, 3, 4])
        # swimming_pool = st.selectbox('Do you have a swimming pool?', ["No","Yes"])
        # surface_of_the_land = area + terrace_area + garden_area


        fully_equipped_kitchen = 1 if fully_equipped_kitchen == "Yes" else 0
        furnished = 1 if furnished == "Yes" else 0
        
        # swimming_pool = 1 if swimming_pool == "Yes" else 0


        # A INTEGRER
        # df = pd.DataFrame([[locality,
        #                     type_of_property,
        #                     number_of_room,area, 
        #                     fully_equipped_kitchen, 
        #                     furnished, 
        #                     open_fire, 
        #                     terrace_area,
        #                     garden_area,
        #                     surface_of_the_land,
        #                     number_of_facades,
        #                     swimming_pool,
        #                     state_of_building,
        #                     province,
        #                     region]], 
        #                     columns= columns)
        if st.button("About"):
            st.text("Thanks for watching the presentation")
    ###################################################################FIN SIDEBAR
        return

def side_bar_void(postal_code):
    with st.sidebar:
        st.header("Please enter the informations needed to have an estimated price")
        st.subheader('General informations:')
        type_of_property = st.selectbox('Select', ["house", "apartment"])
        locality = postal_code
        number_of_room = st.number_input("Enter the number of rooms", min_value= 0, max_value = 10)
        area = st.number_input("Enter the area of your house", min_value= 0, max_value = 1000)
        state_of_building = st.selectbox('What is the state of your house?', ["good", "medium", "to renovate", "new"])

        st.subheader('Please enter indoor informations:')
        fully_equipped_kitchen = st.selectbox('Is your Kitchen fully equipped?', ["No","Yes"])
        furnished = st.selectbox('Is your house is sell furnished?', ["No","Yes"])
        open_fire = st.selectbox('Do you have an open fire?', ["No","Yes"])

        st.subheader('Please enter outdoor informations:')
        terrace_area = st.number_input("Enter the area of your terrace", min_value= 0, max_value = 1000)
        garden_area = st.number_input("Enter the area of your garden", min_value= 0, max_value = 100000000)
        number_of_facades = st.selectbox('What is the number of facades?', [2, 3, 4])
        swimming_pool = st.selectbox('Do you have a swimming pool?', ["No","Yes"])
        surface_of_the_land = area + terrace_area + garden_area


        # province = utils.change_to_province(locality)[:2][0]
        # region = utils.change_to_province(locality)[:2][1]

        fully_equipped_kitchen = 1 if fully_equipped_kitchen == "Yes" else 0
        furnished = 1 if furnished == "Yes" else 0
        open_fire = 1 if open_fire == "Yes" else 0
        swimming_pool = 1 if swimming_pool == "Yes" else 0

        # df = pd.DataFrame([[locality,
        #                     type_of_property,
        #                     number_of_room,area, 
        #                     fully_equipped_kitchen, 
        #                     furnished, 
        #                     open_fire, 
        #                     terrace_area,
        #                     garden_area,
        #                     surface_of_the_land,
        #                     number_of_facades,
        #                     swimming_pool,
        #                     state_of_building,
        #                     province,
        #                     region]], 
        #                     columns= columns)
        return

def change_to_province(postal_code):
    if postal_code >= 1000 and postal_code < 1300:
        return "Brussel","Brussel",1,1
    elif postal_code >= 1300 and postal_code < 1500:
        return "Brabant Wallon","Wallonia",2,2
    elif (postal_code >= 1500 and postal_code < 2000) or (postal_code >= 3000 and postal_code < 3500):
        return "Brabant Flamand","Flanders",3,3
    elif postal_code >= 2000 and postal_code < 3000:
        return "Anvers","Flanders",4,3
    elif postal_code >= 3500 and postal_code < 4000:
        return "Limbourg","Flanders",5,3
    elif postal_code >= 4000 and postal_code < 5000:
        return "Liège","Wallonia",6,2
    elif postal_code >= 5000 and postal_code < 6000:
        return "Namur","Wallonia",7,2
    elif (postal_code >= 6000 and postal_code < 6600) or (postal_code >= 7000 and postal_code < 8000):
        return "Hainaut","Wallonia",8,2
    elif postal_code >= 6600 and postal_code < 7000:
        return "Luxembourg","Wallonia",9,2
    elif postal_code >= 8000 and postal_code < 9000:
        return "Flandre Occidental","Flanders",10,3
    elif postal_code >= 9000:
        return "Flandre Oriental","Flanders",11,3