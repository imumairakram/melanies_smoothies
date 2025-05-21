# # Import python packages
# import streamlit as st
# from snowflake.snowpark.functions import col
# import pandas as pd
# import requests

# # Title and description
# st.title("My Parent's New Healthy Dinner")
# st.write("Choose the fruit you want in your custom smoothie!")

# # Text input for smoothie name
# name_on_order = st.text_input("Name of Smoothie")
# st.write("The name on your smoothie will be:", name_on_order)

# # Snowflake connection
# try:
#     cnx = st.connection("snowflake")
#     session = cnx.session()

#     # Get both FRUIT_NAME (display) and SEARCH_ON (for API)
#     snowflake_df = session.table("smoothies.public.fruit_options").select(
#         col('FRUIT_NAME'), col('SEARCH_ON')
#     )
#     fruit_df = pd.DataFrame(snowflake_df.collect())

#     # Create a mapping: FRUIT_NAME => SEARCH_ON
#     fruit_map = dict(zip(fruit_df['FRUIT_NAME'], fruit_df['SEARCH_ON']))

#     # Use display names in the dropdown
#     fruit_options = list(fruit_map.keys())

#     # Multiselect for ingredients
#     ingredients_list = st.multiselect(
#         'Choose up to 5 ingredients:',
#         fruit_options,
#         max_selections=5
#     )

#     if ingredients_list:
#         # Display chosen ingredients
#         ingredients_string = ', '.join(ingredients_list)
#         st.write(f"Your smoothie '{name_on_order}' includes: {ingredients_string}")

#         # Show nutrition info for each ingredient using SEARCH_ON value
#         for fruit in ingredients_list:
#             api_fruit = fruit_map.get(fruit, fruit)
#             st.subheader(f"{fruit} Nutrition Info")

#             search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
#             st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
            
#             response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{api_fruit.lower()}")
#             if response.status_code == 200:
#                 st.json(response.json())
#             else:
#                 st.warning(f"Nutrition info for {fruit} not found.")

#         # Prepare SQL Insert (string format since Snowflake Streamlit doesn't support parameterized form yet)
#         insert_stmt = f"""
#             INSERT INTO smoothies.public.orders (name, ingredients)
#             VALUES ('{name_on_order}', '{ingredients_string}')
#         """

#         # Submit button
#         if st.button("Submit Order"):
#             session.sql(insert_stmt).collect()
#             st.success(f"Your Smoothie '{name_on_order}' is ordered!", icon="✅")

# except Exception as e:
#     st.error(f"An error occurred: {e}")


 # Import python packages
 import streamlit as st
 from snowflake.snowpark.functions import col
 import pandas as pd
 import requests

 # Title and description
 st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
 st.write("Choose the fruit you want in your custom smoothie!")

 # Text input for smoothie name
 name_on_order = st.text_input("Name of Smoothie")
 st.write("The name on your smoothie will be:", name_on_order)

 # Snowflake connection
 try:
     cnx = st.connection("snowflake")
     session = cnx.session()

     # Query fruit options
     my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON')
     # st.dataFrame(data = my_dataframe, use_container_width=True)
     # st.stop()

     # Multiselect for ingredients
     ingredients_list = st.multiselect(
         'Choose up to 5 ingredients:',
         fruit_options
     )

      if ingredients_list:
        # Display chosen ingredients
        ingredients_string = ', '.join(ingredients_list)
        st.write(f"Your smoothie '{name_on_order}' includes: {ingredients_string}")

        # Show nutrition info for each ingredient using SEARCH_ON value
        for fruit in ingredients_list:
            api_fruit = fruit_map.get(fruit, fruit)
            st.subheader(f"{fruit} Nutrition Info")

            search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
            # st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
            st.subheader(fruit_chosen + Nutrition Information') 
            fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on) 
            fv_df st.dataframe(data=fruityvice_response.json(), use_container_width=True) 
                    
            
            response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{api_fruit.lower()}")
            if response.status_code == 200:
                st.json(response.json())
            else:
                st.warning(f"Nutrition info for {fruit} not found.")
         
          
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
