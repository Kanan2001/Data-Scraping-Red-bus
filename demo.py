import pandas as pd
import mysql.connector
import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import seaborn as sns

# Function to load routes from a CSV file
def load_routes(filepath):
    df = pd.read_csv(filepath)  # Read CSV file into DataFrame
    return df['Routename'].tolist()  # Return a list of route names

# Function to fetch bus data from the MySQL database
def get_bus_data(route_name, min_price, max_price, is_above_2000):
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Pranavu2001",
            database="RED_BUS_PROJECT"
        )
        
        # SQL query based on whether the price filter is "above 2000" or within a range
        if is_above_2000:
            query = f'''
                SELECT * FROM bus_details
                WHERE price >= {min_price} AND Route_name="{route_name}"
                ORDER BY Price DESC
            '''
        else:
            query = f'''
                SELECT * FROM bus_details
                WHERE price BETWEEN {min_price} AND {max_price} AND Route_name="{route_name}"
                ORDER BY Price DESC
            '''
        
        # Execute the query and load the result into a DataFrame
        df = pd.read_sql(query, conn)
    except Exception as e:
        # Display an error message if there's an issue
        st.error(f"Error fetching data: {e}")
        return None
    finally:
        # Close the database connection
        conn.close()
    return df

# Load route data for different states from CSV files
list_routes = {
    "Kerala": load_routes("D:/.intel/.shared/Redbus/Bus route/df_Kerala.csv"),
    "Goa": load_routes("D:/.intel/.shared/Redbus/Bus route/df_KTCL.csv"),
    "Jammu & Kashmir": load_routes("D:/.intel/.shared/Redbus/Bus route/df_JKSRTC.csv"),
    "West Bengal": load_routes("D:/.intel/.shared/Redbus/Bus route/df_WBSTC.csv"),
    "Assam": load_routes("D:/.intel/.shared/Redbus/Bus route/df_KAAC.csv"),
    "Bihar": load_routes("D:/.intel/.shared/Redbus/Bus route/df_BSRTC.csv"),
    "North Bengal": load_routes("D:/.intel/.shared/Redbus/Bus route/df_NBSTC.csv"),
    "Punjab": load_routes("D:/.intel/.shared/Redbus/Bus route/df_PEPSU.csv"),
    "Chandigarh": load_routes("D:/.intel/.shared/Redbus/Bus route/df_CTU.csv"),
    "West Bengal 2": load_routes("D:/.intel/.shared/Redbus/Bus route/df_WBTC.csv")
}

# Streamlit page setup
st.set_page_config(layout="wide")

# Inject custom CSS to style the sidebar
st.markdown(
    """
    <style>
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f0f0f0; /* Change sidebar background color */
    }
    .css-1d391kg .css-1ie3i6z {
        color: #333; /* Change text color */
    }
    .css-1d391kg .css-1c1imd9 {
        color: #333; /* Change selected menu item color */
    }
    .css-1d391kg .css-1s6cx5t {
        color: #007BFF; /* Change icon color */
    }
    .css-1d391kg .css-14i3f7h {
        color: #007BFF; /* Change hover color */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar menu for navigation
with st.sidebar:
    web = option_menu(menu_title="Online Bus",
                      options=["Home", "States and Routes"],
                      icons=["house", "map"],
                      orientation="vertical")

# Main content based on selected menu item
if web == "Home":
    st.title("Welcome to Redbus Data Scraping using selenium with Streamlit")
    # Add the Redbus logo
    st.image("https://th.bing.com/th/id/OIP.IEcYZJUGVfxTTzksE8Wn8AHaDD?w=850&h=350&rs=1&pid=ImgDetMain", width=200)  # Update this path with the location of your logo
    
    st.subheader("Domain: Transportation")
    st.subheader("Objective")
    
    # Provide a description of the project
    st.markdown("""
    The 'Redbus data scraping and filtering with Streamlit application' aims to revolutionize the transportation industry by providing a comprehensive solution. 
    - **Selenium**: A tool for automating web browsers and web scraping.
    - **Pandas**: A powerful library for data manipulation and analysis.
    - **MySQL**: For database connection and storage.
    - **Streamlit**: A framework for creating interactive web applications.
    """)

elif web == "States and Routes":
    st.title("Bus Route Information")
    st.sidebar.header("Filter Options")
    
    # Select state and route from sidebar
    state = st.sidebar.selectbox("Select State", list_routes.keys())
    route_list = list_routes[state]
    selected_route = st.sidebar.selectbox("Select Route", route_list)

    # Interactive price range slider
    min_price_slider, max_price_slider = st.sidebar.slider(
        "Select Price Range",
        min_value=0,
        max_value=5000,
        value=(0, 2000),
        step=100
    )

    # Checkbox to toggle "Above 2000" filter
    is_above_2000 = st.sidebar.checkbox("Show Prices Above 2000", value=False)
    min_price = min_price_slider
    max_price = max_price_slider if not is_above_2000 else float('inf')

    # Fetch and display bus data based on the selected criteria
    df = get_bus_data(selected_route, min_price, max_price, is_above_2000)
    if df is not None:
        st.dataframe(df)  # Display DataFrame in Streamlit
    else:
        st.info("No data available for the selected criteria.")
