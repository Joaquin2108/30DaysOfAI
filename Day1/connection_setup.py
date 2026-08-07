import streamlit as st

try:
    # import the active session if it exists
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()

#else create a new session if it doesn't exist
except:
    from snowflake.snowpark import Session
    #connection parameters are stored in the streamlit secrets manager
    session = Session.builder.configs(st.secrets["connection"]["snowflake"]).create()

#This pattern makes your code work in all three environments: Streamlit in Snowflake (production),
#local development, and Streamlit Community Cloud.

#Query and display the results of a simple query to verify the connection
version = session.sql("SELECT current_version()").collect()[0][0]

#Green checkmark to indicate a successful connection
st.success(f"Connected to Snowflake! Current version: {version}")