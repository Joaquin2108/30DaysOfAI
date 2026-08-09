import streamlit as st
from openai import OpenAI

# Connecting to Snowflake and OpenAI API
conn = st.secrets["connection"]["snowflake"]
host = conn.get("host") or f"{conn['account']}.snowflakecomputing.com"
client = OpenAI(api_key=conn["password"], 
                base_url=f"https://{host}/api/v2/cortex/v1")

# Selecting model and prompt
llm_models = ["claude-3-5-sonnet", "mistral-large", "llama3.1-8b"]
model = st.selectbox("Select a model", llm_models)

example_prompt = "What is the capital of Mexico?"
prompt = st.text_area("Enter your prompt for the AI model", example_prompt)

# Selecting streaming method
streaming_method = st.radio(
    "Streaming method:",
    ["Direct", "Real Streaming"],
    help="Choose how you want the AI model to stream responses")

# Run LLM inference
if st.button("Generate Response"):
    messages = [{"role": "user", "content": prompt}]

    # Run inference based on the selected streaming method
    if streaming_method == "Direct":
        with st.spinner("Generating response with '{model}'"):
            response = client.chat.completions.create(
                model=model,
                messages = messages,
                stream=False)
            st.write(response.choices[0].message.content)

    # Run inference with real streaming
    else:
        with st.spinner("Generating response with '{model}'"):
            stream = client.chat.completions.create(
                model=model,
                messages = messages,
                stream=True)
        st.write_stream(stream)

# Footer
st.divider()
st.caption("Day 3: Hello, Cortex! | 30 Days of AI") 