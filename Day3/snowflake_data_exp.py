import streamlit as st
import pandas as pd
import plotly.express as px


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Snowflake Data Explorer",
    page_icon="❄️",
    layout="wide"
)


# --------------------------------------------------
# Snowflake connection
# --------------------------------------------------

@st.cache_resource
def create_connection():

    try:
        # Used when running inside Snowflake
        from snowflake.snowpark.context import get_active_session

        return get_active_session()

    except Exception:
        # Used when running locally
        from snowflake.snowpark import Session

        return Session.builder.configs(
            st.secrets["connection"]["snowflake"]
        ).create()


# --------------------------------------------------
# Get Snowflake session
# --------------------------------------------------

session = create_connection()


# --------------------------------------------------
# Helper function
# --------------------------------------------------

def run_query(query):
    return session.sql(query).to_pandas()


# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("❄️ Snowflake Data Explorer")

st.markdown(
    """
    Explore data stored in Snowflake without writing SQL.
    """
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.header("Data Selection")

database = st.sidebar.text_input(
    "Database",
    value="SNOWFLAKE_SAMPLE_DATA"
)

schema = st.sidebar.text_input(
    "Schema",
    value="TPCH_SF1"
)


# --------------------------------------------------
# Get available tables
# --------------------------------------------------

tables_query = f"""
SHOW TABLES IN {database}.{schema}
"""

try:

    tables = run_query(tables_query)

except Exception as e:

    st.error("Could not retrieve tables from Snowflake.")
    st.exception(e)
    st.stop()


# --------------------------------------------------
# Table selection
# --------------------------------------------------

table_names = tables["name"].tolist()

if not table_names:

    st.warning("No tables were found.")
    st.stop()

selected_table = st.sidebar.selectbox(
    "Select table",
    table_names
)


# --------------------------------------------------
# Load selected table
# --------------------------------------------------

query = f"""
SELECT *
FROM {database}.{schema}.{selected_table}
LIMIT 10000
"""

try:

    df = run_query(query)

except Exception as e:

    st.error("Could not load the selected table.")
    st.exception(e)
    st.stop()


# --------------------------------------------------
# Dataset overview
# --------------------------------------------------

st.header(f"📊 {selected_table}")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Rows Loaded",
        f"{len(df):,}"
    )

with col2:
    st.metric(
        "Columns",
        len(df.columns)
    )

with col3:
    st.metric(
        "Missing Values",
        f"{df.isna().sum().sum():,}"
    )

with col4:
    st.metric(
        "Duplicate Rows",
        f"{df.duplicated().sum():,}"
    )


# --------------------------------------------------
# Data preview
# --------------------------------------------------

st.subheader("Data Preview")

st.dataframe(
    df,
    use_container_width=True
)


# --------------------------------------------------
# Column information
# --------------------------------------------------

st.subheader("Column Information")

column_info = pd.DataFrame({
    "Column": df.columns,
    "Data Type": df.dtypes.astype(str),
    "Missing Values": df.isna().sum().values,
    "Unique Values": df.nunique().values
})

st.dataframe(
    column_info,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# Numerical analysis
# --------------------------------------------------

st.subheader("Numerical Analysis")

numeric_columns = df.select_dtypes(
    include="number"
).columns.tolist()

if numeric_columns:

    selected_numeric = st.selectbox(
        "Select a numerical column",
        numeric_columns
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Mean",
            f"{df[selected_numeric].mean():,.2f}"
        )

    with col2:
        st.metric(
            "Median",
            f"{df[selected_numeric].median():,.2f}"
        )

    with col3:
        st.metric(
            "Minimum",
            f"{df[selected_numeric].min():,.2f}"
        )

    with col4:
        st.metric(
            "Maximum",
            f"{df[selected_numeric].max():,.2f}"
        )

    # Distribution

    fig = px.histogram(
        df,
        x=selected_numeric,
        title=f"Distribution of {selected_numeric}",
        marginal="box"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info("No numerical columns found.")


# --------------------------------------------------
# Categorical analysis
# --------------------------------------------------

st.subheader("Categorical Analysis")

categorical_columns = df.select_dtypes(
    include=["object", "category"]
).columns.tolist()

if categorical_columns:

    selected_categorical = st.selectbox(
        "Select a categorical column",
        categorical_columns
    )

    value_counts = (
        df[selected_categorical]
        .value_counts()
        .reset_index()
    )

    value_counts.columns = [
        selected_categorical,
        "Count"
    ]

    fig = px.bar(
        value_counts.head(20),
        x=selected_categorical,
        y="Count",
        title=f"Distribution of {selected_categorical}"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info("No categorical columns found.")


# --------------------------------------------------
# SQL Query
# --------------------------------------------------

with st.expander("🔍 View SQL"):

    st.code(
        query,
        language="sql"
    )