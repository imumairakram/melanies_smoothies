# # Import python packages
# import streamlit as st
# from snowflake.snowpark.functions import col
# import pandas as pd
# import requests

# # Write directly to the app
# st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
# st.write("Choose the fruits you want in your custom Smoothie!")

# name_on_order = st.text_input('Name on Smoothie:')
# st.write('The name on your Smoothie will be:', name_on_order)

# try:
#     cnx = st.connection("snowflake")
#     session = cnx.session()
    
#     # Get fruit options from Snowflake
#     my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#     fruit_list = [row["FRUIT_NAME"] for row in my_dataframe.collect()]

#     # Multiselect from fruit list
#     ingredients_List = st.multiselect(
#         'Choose up to 5 ingredients:',
#         fruit_list,
#         max_selections=5
#     )

#     if ingredients_List:
#         ingredients_string = ' '

#         # for fruit_chosen in ingredients_List:
#         #     ingredients_string += fruit_chosen + ' '
#         #     st.subheader(f"{fruit_chosen} Nutrition Information")
#         #     # smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
#         #     # sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

#         for fruit_chosen in ingredients_List:
#             ingredients_string += fruit_chosen + ' '
#             st.subheader(f"{fruit_chosen} Nutrition Information")
        
#             try:
#                 smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{fruit_chosen.lower()}")
#                 if smoothiefroot_response.status_code == 200:
#                     fruit_data = smoothiefroot_response.json()
#                     st.dataframe(pd.DataFrame([fruit_data]))  # show the API data in a table
#                 else:
#                     st.warning(f"Could not fetch data for {fruit_chosen}.")
#             except Exception as e:
#                 st.error(f"Error fetching data for {fruit_chosen}: {e}")


#         # SQL Insert Statement
#         my_insert_stmt = f"""
#             INSERT INTO smoothies.public.orders(ingredients, name_on_order)
#             VALUES ('{ingredients_string.strip()}', '{name_on_order}')
#         """
#         st.write(my_insert_stmt)
#         # st.write(f"Your smoothie '{name_on_order}' includes: {ingredients_string}")

#         # Submit Button
#         time_to_insert = st.button('Submit Order')
#         if time_to_insert:
#             session.sql(my_insert_stmt).collect()
#             st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")

#     smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#     if smoothiefroot_response.status_code == 200:
#         st.write("Fruit API Response:", smoothiefroot_response.json())
#     else:
#         st.error("Failed to fetch data from the fruit API.")
# except Exception as e:
#     st.error(f"An error occurred: {e}")

# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import pandas as pd
import requests

# Title and description
st.title("My Parent's New Healthy Dinner")
st.write("Choose the fruit you want in your custom smoothie!")

# Text input for smoothie name
name_on_order = st.text_input("Name of Smoothie")
st.write("The name on your smoothie will be:", name_on_order)

# Snowflake connection
try:
    cnx = st.connection("snowflake")
    session = cnx.session()

    # Query fruit options
    snowflake_df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
    fruit_options = pd.DataFrame(snowflake_df.collect())['FRUIT_NAME'].tolist()

    # Multiselect for ingredients
    ingredients_list = st.multiselect(
        'Choose up to 5 ingredients:',
        fruit_options
    )

    if ingredients_list:
        # Combine ingredients into a single string
        ingredients_string = ', '.join(ingredients_list)

        # Parameterized SQL for safety
        my_insert_stmt = """
            INSERT INTO smoothies.public.orders (name, ingredients)
            VALUES (%s, %s)
        """

        # Show the SQL statement for debugging
        st.write(f"Your smoothie '{name_on_order}' includes: {ingredients_string}")

        # Button to submit order
        time_to_insert = st.button("Submit Order")
        if time_to_insert:
            session.sql(my_insert_stmt, (name_on_order, ingredients_string)).collect()
            st.success(f"Your Smoothie '{name_on_order}' is ordered!", icon="✅")

    # Optional: Fetching fruit data from external API
    smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
    if smoothiefroot_response.status_code == 200:
        st.write("Fruit API Response:", smoothiefroot_response.json())
    else:
        st.error("Failed to fetch data from the fruit API.")
except Exception as e:
    st.error(f"An error occurred: {e}")
