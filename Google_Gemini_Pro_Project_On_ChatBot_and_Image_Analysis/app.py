import streamlit as st
import time
import textwrap
import google.generativeai as genai

from IPython.display import Markdown

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

## Function to load OpenAI model and get response
def get_gemini_response(api_key, question):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(question)
    return response

## Initialize our Streamlit app
st.set_page_config(
    page_title="Gemini Pro AI Chat Assistant",
    page_icon="🤖",
    layout="centered"
)
st.title("💬 Gemini Pro ChatBot")
st.caption("🚀 A dynamic conversational experience powered by the Google's Gemini Pro AI.")


# Sidebar for API key input
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter your Gemini API key: ", type="password", key="api_key")

# Initialize chat session in Streamlit if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role": "assistant", "content": "How can I help you?"}]

# Display chat history
for message in st.session_state.chat_history:
    role = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message["content"])

# Input field for user's message at the bottom of the page
input_text = st.chat_input("Ask your question here:")

if input_text:
    if api_key:
        # Add user's message to chat and display it
        st.session_state.chat_history.append({"role": "user", "content": input_text})
        st.chat_message("user").markdown(input_text)

        # Send user's message to Gemini AI and get a response
        start_time = time.time()
        response = get_gemini_response(api_key, input_text)
        end_time = time.time()

        assistant_response = response.text
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

        # Calculate evaluation metrics
        latency = end_time - start_time
        input_tokens = len(input_text.split())
        output_tokens = len(assistant_response.split())
        throughput = output_tokens / latency

        # Display Gemini AI's response
        with st.chat_message("assistant"):
            st.markdown(assistant_response)

        # Display metrics in the sidebar
        st.sidebar.subheader("Evaluation Metrics")
        st.sidebar.write(f"- **Throughput:** {throughput:.6f} tokens/second")
        st.sidebar.write(f"- **Latency:** {latency:.6f} seconds")
        st.sidebar.write(f"- **Input Tokens:** {input_tokens}")
        st.sidebar.write(f"- **Output Tokens:** {output_tokens}")
    else:
        st.sidebar.error("Please enter your API key to proceed.")
