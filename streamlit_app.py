# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import pandas as pd
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

try:
    cnx = st.connection("snowflake")
    session = cnx.session()
    
    # Get fruit options from Snowflake
    my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
    fruit_list = [row["FRUIT_NAME"] for row in my_dataframe.collect()]

    # Multiselect from fruit list
    ingredients_List = st.multiselect(
        'Choose up to 5 ingredients:',
        fruit_list,
        max_selections=5
    )

    if ingredients_List:
        ingredients_string = ' '

        for fruit_chosen in ingredients_List:
        ingredients_string += fruit_chosen + ' '
        st.subheader(f"{fruit_chosen} Nutrition Information")
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

        # SQL Insert Statement
        my_insert_stmt = f"""
            INSERT INTO smoothies.public.orders(ingredients, name_on_order)
            VALUES ('{ingredients_string.strip()}', '{name_on_order}')
        """
        st.write(my_insert_stmt)
        # st.write(f"Your smoothie '{name_on_order}' includes: {ingredients_string}")

        # Submit Button
        time_to_insert = st.button('Submit Order')
        if time_to_insert:
            session.sql(my_insert_stmt).collect()
            st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")

except Exception as e:
    st.error(f"An error occurred: {e}")



smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True) 
