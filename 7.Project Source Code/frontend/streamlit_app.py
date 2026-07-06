"""
Personalized Networking Assistant - Streamlit Frontend
Simplified version - no external component imports
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Page configuration
st.set_page_config(
    page_title="Personalized Networking Assistant",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ INITIALIZE SESSION STATE ============
if 'base_url' not in st.session_state:
    st.session_state.base_url = "http://127.0.0.1:8000"

if 'event_description' not in st.session_state:
    st.session_state.event_description = ""

if 'user_interests' not in st.session_state:
    st.session_state.user_interests = ""

if 'generated_suggestions' not in st.session_state:
    st.session_state.generated_suggestions = []

if 'extracted_themes' not in st.session_state:
    st.session_state.extracted_themes = []

if 'show_results' not in st.session_state:
    st.session_state.show_results = False

if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"

if 'feedback_submitted' not in st.session_state:
    st.session_state.feedback_submitted = {}

if 'fact_check_result' not in st.session_state:
    st.session_state.fact_check_result = None


# ============ CUSTOM CSS ============
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; font-weight: 700; color: #1f77b4; text-align: center; padding: 1rem 0; }
    .suggestion-card { background: #f8f9fa; border-radius: 10px; padding: 1.2rem; margin: 0.8rem 0; border-left: 4px solid #1f77b4; }
    .theme-tag { display: inline-block; background: #e9ecef; padding: 0.2rem 0.8rem; border-radius: 20px; margin: 0.2rem; font-size: 0.85rem; }
    .fact-verified { background: #d4edda; border: 1px solid #c3e6cb; color: #155724; padding: 1rem; border-radius: 8px; }
    .fact-disputed { background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; padding: 1rem; border-radius: 8px; }
    .fact-partial { background: #fff3cd; border: 1px solid #ffeaa7; color: #856404; padding: 1rem; border-radius: 8px; }
    .history-entry { background: white; border-radius: 8px; padding: 1rem; margin: 0.5rem 0; border: 1px solid #e9ecef; }
    .stat-card { background: white; border-radius: 10px; padding: 1.2rem; text-align: center; border: 1px solid #e9ecef; }
    .stat-number { font-size: 2.5rem; font-weight: 700; color: #1f77b4; }
    .stat-label { font-size: 0.9rem; color: #6c757d; }
    .section-divider { margin: 2rem 0; border-top: 2px solid #dee2e6; }
    .info-box { background: #e7f3ff; border-radius: 8px; padding: 1rem; margin: 0.5rem 0; border-left: 4px solid #1f77b4; }
</style>
""", unsafe_allow_html=True)


# ============ SIDEBAR ============
with st.sidebar:
    st.markdown("### 🤝 Networking Assistant")
    st.markdown("---")
    
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


# ============ HOME PAGE ============
if st.session_state.current_page == "Home":
    st.markdown('<p class="main-header">🤝 Personalized Networking Assistant</p>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🚀 Welcome!
    This AI-powered assistant helps you generate personalized conversation starters for networking events.
    
    **How it works:**
    1. Create your profile with a bio
    2. Add an event description
    3. Generate AI-powered conversation starters
    4. Fact-check any information
    """)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💬 Generate Starters", use_container_width=True):
            st.session_state.current_page = "Generate"
            st.rerun()
    with col2:
        if st.button("🔍 Fact Check", use_container_width=True):
            st.session_state.current_page = "Fact Check"
            st.rerun()


# ============ GENERATE PAGE ============
elif st.session_state.current_page == "Generate":
    st.markdown('<p class="main-header">💬 Generate Conversation Starters</p>', unsafe_allow_html=True)
    
    event_description = st.text_area("Event Description", placeholder="Describe the networking event...", height=100)
    user_interests = st.text_input("Your Interests (comma-separated)", placeholder="AI, Data Science, Python")
    max_suggestions = st.slider("Number of suggestions", 1, 5, 3)
    
    if st.button("🚀 Generate Conversation Starters", type="primary", use_container_width=True):
        if event_description and user_interests:
            interests_list = [i.strip() for i in user_interests.split(',') if i.strip()]
            
            with st.spinner("🤖 Generating..."):
                try:
                    import requests
                    payload = {
                        "event_description": event_description,
                        "user_interests": interests_list,
                        "max_suggestions": max_suggestions
                    }
                    response = requests.post(
                        f"{st.session_state.base_url}/generate-conversation",
                        json=payload,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.generated_suggestions = data.get("suggestions", [])
                        st.session_state.extracted_themes = data.get("extracted_themes", [])
                        st.session_state.show_results = True
                        st.rerun()
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please fill in all fields")
    
    if st.session_state.show_results and st.session_state.generated_suggestions:
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        if st.session_state.extracted_themes:
            st.subheader("🎯 Extracted Themes")
            theme_html = "".join([f'<span class="theme-tag">#{theme}</span>' for theme in st.session_state.extracted_themes])
            st.markdown(theme_html, unsafe_allow_html=True)
        
        st.subheader("💡 Conversation Starters")
        for i, suggestion in enumerate(st.session_state.generated_suggestions):
            st.markdown(f"""
            <div class="suggestion-card">
                <strong>Suggestion {i+1}</strong>
                <p>{suggestion}</p>
            </div>
            """, unsafe_allow_html=True)
            
            fb_key = f"fb_{i}"
            if fb_key not in st.session_state.feedback_submitted:
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("👍 Like", key=f"like_{i}"):
                        st.session_state.feedback_submitted[fb_key] = "like"
                        st.rerun()
                with col2:
                    if st.button("👎 Dislike", key=f"dislike_{i}"):
                        st.session_state.feedback_submitted[fb_key] = "dislike"
                        st.rerun()
            else:
                status = st.session_state.feedback_submitted[fb_key]
                st.markdown(f"✅ {status.capitalize()}d!")


# ============ FACT CHECK PAGE ============
elif st.session_state.current_page == "Fact Check":
    st.markdown('<p class="main-header">🔍 Fact Check</p>', unsafe_allow_html=True)
    
    query = st.text_area("What would you like to fact-check?", placeholder="Enter a statement or topic...", height=80)
    
    if st.button("🔎 Check Fact", type="primary", use_container_width=True):
        if query:
            with st.spinner("🔍 Searching Wikipedia..."):
                try:
                    import requests
                    response = requests.post(
                        f"{st.session_state.base_url}/fact-check",
                        json={"query": query},
                        timeout=10
                    )
                    if response.status_code == 200:
                        result = response.json()
                        st.session_state.fact_check_result = result
                        st.rerun()
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter something to check")
    
    if st.session_state.fact_check_result:
        result = st.session_state.fact_check_result
        if result.get("verified", False):
            st.markdown(f"""
            <div class="fact-verified">
                ✅ <strong>VERIFIED</strong>
                <p>{result.get('summary', 'No summary available.')}</p>
                <a href="{result.get('source_url', '#')}" target="_blank">🔗 Source</a>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="fact-disputed">
                ❌ <strong>NOT VERIFIED</strong>
                <p>{result.get('summary', 'No information found.')}</p>
            </div>
            """, unsafe_allow_html=True)


# ============ HISTORY PAGE ============
elif st.session_state.current_page == "History":
    st.markdown('<p class="main-header">📜 Conversation History</p>', unsafe_allow_html=True)
    
    try:
        import requests
        response = requests.get(f"{st.session_state.base_url}/history")
        if response.status_code == 200:
            data = response.json()
            entries = data.get("entries", [])
            st.metric("Total Conversations", data.get("total", 0))
            
            if entries:
                for entry in entries:
                    with st.expander(f"📅 {entry.get('timestamp', 'Unknown time')[:16]}"):
                        st.write(f"**Event:** {entry.get('event_description', 'N/A')}")
                        themes = entry.get('themes', [])
                        if themes:
                            st.write(f"**Themes:** {', '.join(themes)}")
                        suggestions = entry.get('suggestions', [])
                        if suggestions:
                            st.write("**Suggestions:**")
                            for s in suggestions:
                                st.write(f"• {s}")
            else:
                st.info("No conversations yet. Generate some starters!")
        else:
            st.error("Failed to load history")
    except Exception as e:
        st.error(f"Error: {str(e)}")


# ============ FEEDBACK PAGE ============
else:
    st.markdown('<p class="main-header">📊 Feedback History</p>', unsafe_allow_html=True)
    
    try:
        import requests
        response = requests.get(f"{st.session_state.base_url}/feedback/stats")
        if response.status_code == 200:
            stats = response.json()
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total", stats.get("total", 0))
            with col2:
                st.metric("👍 Likes", stats.get("likes", 0))
            with col3:
                like_rate = stats.get("like_rate", 0) * 100
                st.metric("Like Rate", f"{like_rate:.0f}%")
    except:
        pass
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Show feedback from file
    import json
    feedback_path = Path("data") / "feedback.json"
    
    if st.button("📊 Show Feedback", use_container_width=True):
        if feedback_path.exists():
            with open(feedback_path, "r", encoding="utf-8") as f:
                feedback_data = json.load(f)
            
            if feedback_data:
                for item in reversed(feedback_data[-10:]):
                    icon = "👍" if item.get("feedback") == "like" else "👎"
                    st.markdown(f"""
                    <div class="history-entry">
                        <div>{icon} <strong>{item.get('suggestion', 'No suggestion')}</strong></div>
                        <div style="color: #6c757d; font-size: 0.85rem;">🕐 {item.get('timestamp', 'Unknown time')[:16]}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("---")
            else:
                st.info("No feedback submitted yet.")
        else:
            st.info("No feedback file found.")