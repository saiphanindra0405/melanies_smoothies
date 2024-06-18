import streamlit as st
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write(
    """Choose the **FRUITS** you want in your custom Smoothie!"""
)

name_on_order = st.text_input('Name on Smoothie: ')
st.write('The name on your Smoothie will be: ', name_on_order)

# Debugging: Print secrets keys
st.write(st.secrets.keys())

if "connections" in st.secrets and "SnowparkConnection" in st.secrets["connections"]:
    conn_params = st.secrets["connections"]["SnowparkConnection"]
    session = Session.builder.configs(conn_params).create()

    # Retrieve available fruit options from Snowflake
    my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).to_pandas()

    ingredients_list = st.multiselect(
        'Choose up to 5 ingredients:',
        my_dataframe['FRUIT_NAME'].tolist(),
        max_selections=5
    )

    if ingredients_list:
        ingredients_string = ' '.join(ingredients_list)

        my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders (ingredients, name_on_order)
        VALUES ('{ingredients_string}', '{name_on_order}')
        """

        time_to_insert = st.button('Submit Order')
        if time_to_insert:
            session.sql(my_insert_stmt).collect()
            st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
else:
    st.error("SnowparkConnection details are missing in the secrets.")
