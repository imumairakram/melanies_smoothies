import streamlit as st
from snowflake.snowpark.functions import col
import pandas as pd
import requests

# App Title
st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruit you want in your custom smoothie!")

# Name input
name_on_order = st.text_input("Name of Smoothie")
st.write("The name on your smoothie will be:", name_on_order)

# Order filled checkbox
order_filled = st.checkbox("Mark this order as filled")

try:
    # Snowflake connection
    cnx = st.connection("snowflake")
    session = cnx.session()

    # Get fruit options with search names
    sf_df = session.table("smoothies.public.fruit_options").select(
        col('FRUIT_NAME'), col('SEARCH_ON')
    )
    pd_df = pd.DataFrame(sf_df.collect())

    # Get fruit list
    fruit_options = pd_df["FRUIT_NAME"].tolist()

    # Multiselect ingredients
    ingredients_list = st.multiselect(
        "Choose up to 5 ingredients (order matters):",
        fruit_options,
        max_selections=5
    )

    if ingredients_list:
        ingredients_string = ' '.join(ingredients_list)  # SPACE-separated!

        # Construct INSERT SQL with ORDER_FILLED handling
        order_filled = name_on_order in ['Divya', 'Xi']  # Only these two are marked filled
        
        insert_stmt = f"""
            INSERT INTO smoothies.public.orders (name_on_order, ingredients, order_filled)
            VALUES ('{name_on_order}', '{ingredients_string}', {str(order_filled).upper()})
        """
        
        st.write(f"Your smoothie '{name_on_order}' includes: {ingredients_string}")
        
        if st.button("Submit Order"):
            session.sql(insert_stmt).collect()
            st.success(f"Order for '{name_on_order}' placed successfully!")

    #     ingredients_string = ', '.join([ingredient.strip().title() for ingredient in ingredients_list])
    #     st.write(f"Your smoothie '{name_on_order}' includes: {ingredients_string}")

    #     # Show nutrition info
    #     for fruit in ingredients_list:
    #         st.subheader(f"{fruit} Nutrition Information")
    #         try:
    #             search_on = pd_df.loc[pd_df["FRUIT_NAME"] == fruit, "SEARCH_ON"].values[0]
    #             response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on.lower()}")
    #             if response.status_code == 200:
    #                 st.json(response.json())
    #             else:
    #                 st.warning(f"Nutrition info for {fruit} not found.")
    #         except:
    #             st.warning(f"Nutrition info for {fruit} not found.")

    #     # Submit to Snowflake
    #     submit = st.button("Submit Order")
    #     if submit:
    #         insert_stmt = f"""
    #             INSERT INTO smoothies.public.orders (name_on_order, ingredients, order_filled)
    #             VALUES ('{name_on_order}', '{ingredients_string}', {order_filled})
    #         """
    #         session.sql(insert_stmt).collect()
    #         st.success(f"Order for '{name_on_order}' placed successfully!", icon="✅")

except Exception as e:
    st.error(f"An error occurred: {e}")

# import streamlit as st
# from snowflake.snowpark.functions import col
# import pandas as pd
# import requests

# # Title
# st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
# st.write("Choose the fruit you want in your custom smoothie!")

# # Smoothie name input
# name_on_order = st.text_input("Name of Smoothie")
# st.write("The name on your smoothie will be:", name_on_order)

# # Mark as filled checkbox
# order_filled = st.checkbox("Mark order as FILLED")

# # Snowflake connection
# try:
#     cnx = st.connection("snowflake")
#     session = cnx.session()

#     # Query fruit options
#     df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).to_pandas()
#     fruit_options = df['FRUIT_NAME'].tolist()

#     # Multiselect for up to 5 fruits
#     ingredients_list = st.multiselect(
#         'Choose up to 5 ingredients (in exact order):',
#         fruit_options,
#         max_selections=5
#     )

#     if ingredients_list:
#         ingredients_string = ', '.join(ingredients_list)
#         st.write(f"Your smoothie '{name_on_order}' includes: {ingredients_string}")
#         st.write("Order filled:", order_filled)

#         # Insert button
#         if st.button("Submit Order"):
#             insert_sql = f"""
#                 INSERT INTO smoothies.public.orders (name_on_order, ingredients, order_filled)
#                 VALUES ('{name_on_order}', '{ingredients_string}', {order_filled})
#             """
#             session.sql(insert_sql).collect()
#             st.success(f"Your smoothie for {name_on_order} has been submitted!", icon="✅")

# except Exception as e:
#     st.error(f"An error occurred: {e}")
