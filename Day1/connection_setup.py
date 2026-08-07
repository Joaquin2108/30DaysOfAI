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

# Streamlit UI elements. Text, headers, subheaders, captions, code blocks, and LaTeX can be displayed using Streamlit's built-in functions.
st.title("Testing a Snowflake Connection in Streamlit")
st.header("Day 1: Connection Setup")
st.markdown("This is a markdown text. You can use **bold**, *italic*, and [links](https://www.snowflake.com/) in markdown.")
st.subheader("This is the subheader.")
st.caption("This is the caption. It is usually used for small print or disclaimers. ")
st.code("x = 2021  \nprint(x)   # This is a code block. You can use it to display code snippets.")
st.latex(r''' a+a r^1+a r^2+a r^3 ''')
st.caption("Above is a LaTeX example. You can use LaTeX to display mathematical equations and symbols.")