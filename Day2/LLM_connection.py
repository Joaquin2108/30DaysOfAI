import streamlit as st
from snowflake.snowpark.functions import ai_complete
import json

st.title(":material/smart_toy: Hello, Cortex!")

# Connecting to Snowflake
try:
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()

except Exception:
    from snowflake.snowpark import Session

    session = Session.builder.configs(
        st.secrets["connection"]["snowflake"]
    ).create()

# Model and prompt
model = "claude-3-7-sonnet"
prompt = st.text_input("Enter your prompt for the AI model")

# Run LLM inference
if prompt and st.button("Generate Response"):

    df = session.range(1).select(
        ai_complete(
            model=model,
            prompt=prompt
        ).alias("response")
    )

    response_raw = df.collect()[0][0]

    try:
        response = json.loads(response_raw)
        st.write(response)
    except:
        st.write(response_raw)

# Footer
st.divider()
st.caption("Day 2: Hello, Cortex! | 30 Days of AI")