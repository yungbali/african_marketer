import streamlit as st
from utils.ai_agents import AfricanMusicAIAgent
import os

def init_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "ai_agent" not in st.session_state:
        try:
            # Try to get API key from secrets
            anthropic_key = st.secrets.get("anthropic", {}).get("api_key")
            if not anthropic_key:
                st.error("""
                ⚠️ Anthropic API key not found in secrets.
                
                Please add your API key in Streamlit Cloud:
                1. Go to your app settings
                2. Click on 'Secrets'
                3. Add the following configuration:
                ```toml
                [anthropic]
                api_key = "sk-ant-your-actual-key-here"
                ```
                """)
                st.stop()
            
            st.session_state.ai_agent = AfricanMusicAIAgent(anthropic_key)
        except Exception as e:
            st.error(f"Error initializing AI agent: {str(e)}")
            st.stop()

def render_chat():
    """Render the chat interface"""
    st.subheader("💬 African Music Marketing Advisor")
    
    # Add description
    st.markdown("""
    Ask me anything about:
    - EPK Development
    - Music Marketing Strategy
    - African Music Industry Trends
    - Artist Branding
    - Digital Marketing
    """)
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about African music marketing..."):
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.ai_agent.get_advice(prompt)
                if response["status"] == "success":
                    st.markdown(response["advice"])
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response["advice"]}
                    )
                else:
                    st.error(response["advice"])

    # Add clear conversation button
    if st.button("🔄 Clear Conversation"):
        result = st.session_state.ai_agent.clear_conversation()
        if result["status"] == "success":
            st.session_state.messages = []
            st.success("Conversation cleared!")
        else:
            st.error(result["message"])

def main():
    st.set_page_config(
        page_title="African Music Marketing Assistant",
        page_icon="🎵",
        layout="wide"
    )
    
    st.title("🎵 African Music Marketing Assistant")
    
    # Initialize session state
    init_session_state()
    
    # Create two columns
    col1, col2 = st.columns([3, 1])
    
    with col1:
        render_chat()
    
    with col2:
        with st.expander("✨ Tips for Better Results"):
            st.markdown("""
            - Be specific about your goals
            - Mention your target market
            - Include relevant context
            - Ask follow-up questions
            """)
        
        with st.expander("📚 Resources"):
            st.markdown("""
            - [Music Marketing Guide](https://example.com)
            - [EPK Templates](https://example.com)
            - [Industry Reports](https://example.com)
            """)

if __name__ == "__main__":
    main()