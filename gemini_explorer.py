import vertexai
import streamlit as st
from vertexai.preview.generative_models import GenerationConfig, GenerativeModel, Part, Content, ChatSession

project = 'gold-hold-418319'
vertexai.init(project=project)

config = GenerationConfig(
    temperature = 0.4,
    top_k=10
)

# Load model with config defined
model = GenerativeModel(
    'gemini-pro',
    generation_config=config,
)

chat = model.start_chat()

# Helper function
def llm_function(chat: ChatSession, query: str) -> None:
    """
    Processes a user query and displays the response in the Streamlit app.

    Keyword arguments:
    chat -- ChatSession,
    query -- text containing message.
    """

    response = chat.send_message(query)
    output = response.candidates[0].content.parts[0].text
    # try:
    #     output = response.candidates[0].content.parts[0].text
    # except:
    #     output = "".join(part.text for part in response.candidates[0].content.parts)  # Join text from all parts

    with st.chat_message("model"):
        st.markdown(output)

    st.session_state.messages.append({
        'role': 'user',
        'content': output
    })

    st.session_state.messages.append({
        'role': 'model',
        'content': output
    })


# Setting up title
st.title('Gemini Explorer')

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display and load chat history
for index, message in enumerate(st.session_state.messages):

    content = Content(
        role=message['role'],
        parts=[ Part.from_text(message['content']) ]
    )

    if index != 0:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    chat.history.append(content)

# for initial message startup
if len(st.session_state.messages) == 0:
    initial_prompt = "Introduce yourself as ReX, an assistant powered by Google Gemini. You use emojis to be interactive"
    llm_function(chat, initial_prompt)

# To capture user input
query : str = st.chat_input('Gemini Explorer')

if query:
    with st.chat_message('user'):
        st.markdown(query)
    llm_function(chat=chat, query=query)
