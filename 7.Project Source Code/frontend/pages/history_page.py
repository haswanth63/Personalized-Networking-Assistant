"""
History Page - View past conversations
Following the Conversation History View pattern
"""

import streamlit as st
import requests
from datetime import datetime


def render():
    """Render the history page"""
    
    st.markdown('<p class="main-header">📜 Conversation History</p>', unsafe_allow_html=True)
    
    # ============ LOAD HISTORY ============
    try:
        response = requests.get(f"{st.session_state.base_url}/history")
        
        if response.status_code == 200:
            data = response.json()
            entries = data.get("entries", [])
            total = data.get("total", 0)
            
            # Stats
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Conversations", total)
            with col2:
                st.metric("Showing", f"{min(len(entries), 10)}")
            
            if not entries:
                st.info("No conversations yet. Generate some starters to see them here!")
                
                # Quick link to generate
                if st.button("🚀 Go Generate Starters", use_container_width=True):
                    st.session_state.current_page = "Generate"
                    st.rerun()
                return
            
            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
            
            # Display each history entry
            st.subheader("📋 Recent Conversations")
            
            for entry in entries:
                with st.expander(f"📅 {entry.get('timestamp', 'Unknown time')[:16]}"):
                    # Event description
                    st.markdown(f"""
                    <div class="history-entry">
                        <strong>🎯 Event:</strong> {entry.get('event_description', 'N/A')}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Themes
                    themes = entry.get('themes', [])
                    if themes:
                        theme_html = "".join([
                            f'<span class="theme-tag">#{theme}</span>'
                            for theme in themes
                        ])
                        st.markdown(f"**Themes:** {theme_html}", unsafe_allow_html=True)
                    
                    # Suggestions
                    suggestions = entry.get('suggestions', [])
                    if suggestions:
                        st.markdown("**💡 Suggestions:**")
                        for i, suggestion in enumerate(suggestions, 1):
                            st.markdown(f"{i}. {suggestion}")
                    
                    # User interests
                    interests = entry.get('user_interests', [])
                    if interests:
                        st.markdown(f"**Interests:** {', '.join(interests)}")
                    
                    # ID
                    st.caption(f"ID: {entry.get('id', 'N/A')}")
            
        else:
            st.error("Failed to load history")
            
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend. Make sure the server is running.")
    except Exception as e:
        st.error(f"Error: {str(e)}")