import numpy as np
import pandas as pd
import pickle
import streamlit as st 
import webbrowser
import os

def side_bar(address):
    with st.sidebar:
        ### LIST OF ADDRESSE ###
        df = pd.read_csv("info_house.csv")
        df = df.dropna(subset=["property_location_number"])
        df["property_location_number"] = df["property_location_number"].astype(int)
        df["address"] = df["property_location_street"].astype(str) + " " + df["property_location_number"].astype(str) + ", " + df["property_location_postalCode"].astype(str) + " " + df["property_location_locality"].astype(str)
        
        df_address = df[df["address"] == address]
        
        #Type of property
        type_of_property = df_address["property_type"]
        st.header(f'Information about the {type_of_property.values[0].capitalize()}:')

        locality = df_address["property_location_postalCode"].values[0]

        #Number of rooms
        number_of_room = df_address["property_bedroomCount"].values[0]
        st.markdown('__Number of bedrooms:__')
        st.info(number_of_room)

        #Surface of the house
        area = int(df_address["property_netHabitableSurface"].values[0])
        st.markdown('__Habitable Surface:__')
        st.info(f'{area} m2')

        #State of the building - we translate the wording from immoweb which is raw. !should be deleted if working with clean db
        dic_state = {"AS_NEW":" new", "JUST_RENOVATED": "new", "TO_BE_DONE_UP" : "to renovate", "GOOD" : "good"} 
        # st.selectbox('What is the state of your house?', ["good", "medium", "to renovate", "new"])
        if isinstance(df_address["property_building_condition"].values[0], str):
            state_of_building = dic_state[df_address["property_building_condition"].values[0]]
            st.markdown('__Building condition:__')
            st.info(f'{state_of_building.capitalize()}')
        else:  
            state_of_building = "medium" #This is the default value for the model to run
        
        #Equipped Kitchen
        if isinstance(df_address["property_kitchen_type"].values[0], str):
            fully_equipped_kitchen = "Yes"
            st.markdown('__Equipped kitchen?__')
            st.info(f'{fully_equipped_kitchen.capitalize()}')
        else:
            fully_equipped_kitchen = "No"
            st.markdown('__Equipped kitchen?__')
            st.info(f'{fully_equipped_kitchen.capitalize()}')
                       
        #Furnished !!!WARNING!!! Must change the DATASET SAM JE YO NO FURNISHED OPTION
        furnished = "No" #set to default but influence the result of the model

        #Open Fire
        open_fire = df_address["property_fireplaceExists"].values[0]
        open_fire_display = "Yes" if open_fire == 1 else "No"
        st.markdown('__Fire place?__')
        st.info(f'{open_fire_display.capitalize()}')

        st.header('Outdoor informations:')
        
        #Terrace Area
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

        #Garden Area
        # garden_area = st.number_input("Enter the area of your garden", min_value= 0, max_value = 100000000) #not in dataset

        # number_of_facades = st.selectbox('What is the number of facades?', [2, 3, 4])
        # swimming_pool = st.selectbox('Do you have a swimming pool?', ["No","Yes"])
        # surface_of_the_land = area + terrace_area + garden_area


        fully_equipped_kitchen = 1 if fully_equipped_kitchen == "Yes" else 0
        furnished = 1 if furnished == "Yes" else 0
        
        # swimming_pool = 1 if swimming_pool == "Yes" else 0


        ## A INTEGRER
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