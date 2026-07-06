"""
Sidebar Component - Reusable sidebar navigation
"""

import streamlit as st


def render_sidebar():
    """Render the sidebar navigation"""
    with st.sidebar:
        st.markdown("### 🤝 Networking Assistant")
        st.markdown("---")
        
        # Page navigation
        pages = {
            "🏠 Home": "Home",
            "💬 Generate": "Generate",
            "🔍 Fact Check": "Fact Check",
            "📜 History": "History",
            "📊 Feedback": "Feedback"
        }
        
        for label, page in pages.items():
            if st.button(label, use_container_width=True,
                        type="primary" if st.session_state.current_page == page else "secondary"):
                st.session_state.current_page = page
                st.rerun()
        
        st.markdown("---")
        
        # Backend status
        st.markdown("### 🔗 Status")
        try:
            import requests
            response = requests.get(f"{st.session_state.base_url}/health", timeout=2)
            if response.status_code == 200:
                st.success("✅ Connected")
            else:
                st.warning("⚠️ Unhealthy")
        except:
            st.error("❌ Disconnected")
        
        st.markdown("---")
        st.caption("v1.0.0")