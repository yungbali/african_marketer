import streamlit as st
from utils.ai_agents import AfricanMusicAIAgent
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="African Music Marketing Assistant",
    page_icon="🎵",
    layout="wide"
)

def init_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "ai_agent" not in st.session_state:
        try:
            st.session_state.ai_agent = AfricanMusicAIAgent()
        except Exception as e:
            logger.error(f"Error initializing AI agent: {str(e)}")
            st.error("Failed to initialize AI assistant. Please try again later.")
            st.stop()

def main():
    st.title("🎵 African Music Marketing Assistant")
    
    # Initialize session state
    init_session_state()
    
    # Sidebar with context options
    with st.sidebar:
        st.header("Marketing Context")
        genre = st.selectbox("Music Genre", 
            ["Afrobeats", "Amapiano", "Highlife", "Bongo Flava", "Other"])
        target_market = st.multiselect("Target Markets",
            ["Nigeria", "South Africa", "Kenya", "Ghana", "Tanzania", "International"])
        budget = st.select_slider("Marketing Budget",
            options=["Low", "Medium", "High"])
        
        context = {
            "genre": genre,
            "target_markets": target_market,
            "budget": budget
        }

    # Chat interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about African music marketing..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.ai_agent.get_advice(prompt, context)
                if response["status"] == "success":
                    st.markdown(response["advice"])
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response["advice"]
                    })
                else:
                    st.error(response["advice"])

if __name__ == "__main__":
    main()