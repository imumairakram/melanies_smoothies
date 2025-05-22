# import streamlit as st
# from snowflake.snowpark.functions import col
# import pandas as pd
# import requests

# # Title and description
# st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
# st.write("Choose the fruit you want in your custom smoothie!")

# # Text input for smoothie name
# name_on_order = st.text_input("Name of Smoothie")
# st.write("The name on your smoothie will be:", name_on_order)

# # Snowflake connection
# try:
#     cnx = st.connection("snowflake")
#     session = cnx.session()

#     # Query fruit options from Snowflake
#     snowflake_df = session.table("smoothies.public.fruit_options").select(
#         col("FRUIT_NAME"), col("SEARCH_ON")
#     )
#     pd_df = pd.DataFrame(snowflake_df.collect())

#     # Create a map from FRUIT_NAME to SEARCH_ON
#     fruit_map = dict(zip(pd_df["FRUIT_NAME"], pd_df["SEARCH_ON"]))
#     fruit_options = list(fruit_map.keys())

#     # Multiselect for ingredients
#     ingredients_list = st.multiselect(
#         'Choose up to 5 ingredients:',
#         fruit_options,
#         max_selections=5
#     )

#     if ingredients_list:
#         # Combine ingredients into a single string
#         ingredients_string = ', '.join(ingredients_list)
#         st.write(f"Your smoothie '{name_on_order}' includes: {ingredients_string}")

#         # Show nutrition info using SEARCH_ON for each selected fruit
#         for fruit_chosen in ingredients_list:
#             search_on = fruit_map.get(fruit_chosen)

#             st.subheader(f"{fruit_chosen} Nutrition Information")

#             # Call API using SEARCH_ON value
#             fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{search_on}")
#             if fruityvice_response.status_code == 200:
#                 fruity_data = fruityvice_response.json()
#                 st.json(fruity_data)
#             else:
#                 st.warning(f"Nutrition info for {fruit_chosen} not found.")

#         # Insert into Snowflake orders table
#         insert_stmt = f"""
#             INSERT INTO smoothies.public.orders (name, ingredients)
#             VALUES ('{name_on_order}', '{ingredients_string}')
#         """

#         # Submit button
#         if st.button("Submit Order"):
#             session.sql(insert_stmt).collect()
#             st.success(f"Your Smoothie '{name_on_order}' is ordered!", icon="✅")

#     # Optional extra API preview (can be removed)
#     smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#     if smoothiefroot_response.status_code == 200:
#         st.write("Fruit API Response:", smoothiefroot_response.json())
#     else:
#         st.error("Failed to fetch data from the fruit API.")

# except Exception as e:
#     st.error(f"An error occurred: {e}")

import streamlit as st
from snowflake.snowpark.functions import col
import pandas as pd
import requests

# Title
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruit you want in your custom smoothie!")

# Smoothie name input
name_on_order = st.text_input("Name of Smoothie")
st.write("The name on your smoothie will be:", name_on_order)

# Mark as filled checkbox
order_filled = st.checkbox("Mark order as FILLED")

# Snowflake connection
try:
    cnx = st.connection("snowflake")
    session = cnx.session()

    # Query fruit options
    df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).to_pandas()
    fruit_options = df['FRUIT_NAME'].tolist()

    # Multiselect for up to 5 fruits
    ingredients_list = st.multiselect(
        'Choose up to 5 ingredients (in exact order):',
        fruit_options,
        max_selections=5
    )

    if ingredients_list:
        ingredients_string = ', '.join(ingredients_list)
        st.write(f"Your smoothie '{name_on_order}' includes: {ingredients_string}")
        st.write("Order filled:", order_filled)

        # Insert button
        if st.button("Submit Order"):
            insert_sql = f"""
                INSERT INTO smoothies.public.orders (name_on_order, ingredients, order_filled)
                VALUES ('{name_on_order}', '{ingredients_string}', {order_filled})
            """
            session.sql(insert_sql).collect()
            st.success(f"Your smoothie for {name_on_order} has been submitted!", icon="✅")

except Exception as e:
    st.error(f"An error occurred: {e}")
