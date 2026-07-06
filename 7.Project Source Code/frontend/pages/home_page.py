"""
Home Page - Landing page for the application
Shows overview, stats, and quick start guide
"""

import streamlit as st
import requests
from datetime import datetime


def render():
    """Render the home page"""
    
    st.markdown('<p class="main-header">🤝 Personalized Networking Assistant</p>', unsafe_allow_html=True)
    
    # Stats row
    col1, col2, col3, col4 = st.columns(4)
    
    try:
        # Get stats from backend
        response = requests.get(f"{st.session_state.base_url}/admin/stats")
        if response.status_code == 200:
            stats = response.json()
            
            with col1:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{stats.get('total_conversations', 0)}</div>
                    <div class="stat-label">Conversations</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{stats.get('total_feedback', 0)}</div>
                    <div class="stat-label">Feedback Items</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                feedback_stats = stats.get('feedback_stats', {})
                like_rate = feedback_stats.get('like_rate', 0) * 100
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{like_rate:.0f}%</div>
                    <div class="stat-label">Like Rate</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{stats.get('total_feedback', 0)}</div>
                    <div class="stat-label">Total</div>
                </div>
                """, unsafe_allow_html=True)
    except:
        # Show placeholder stats
        with col1:
            st.markdown("""
            <div class="stat-card">
                <div class="stat-number">0</div>
                <div class="stat-label">Conversations</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class="stat-card">
                <div class="stat-number">0</div>
                <div class="stat-label">Feedback Items</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class="stat-card">
                <div class="stat-number">0%</div>
                <div class="stat-label">Like Rate</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown("""
            <div class="stat-card">
                <div class="stat-number">0</div>
                <div class="stat-label">Total</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Features
    st.subheader("🚀 What You Can Do")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 💬 Generate Starters
        Enter an event description and your interests to get personalized conversation starters.
        
        **How it works:**
        1. Describe your networking event
        2. List your interests
        3. Get 3 AI-generated conversation starters
        
        👉 [Go to Generate →](/Generate)
        """)
    
    with col2:
        st.markdown("""
        ### 🔍 Fact Check
        Verify information about any topic using Wikipedia.
        
        **How it works:**
        1. Enter a statement or topic
        2. Get verification results
        3. See source links
        
        👉 [Go to Fact Check →](/Fact_Check)
        """)
    
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    # Quick Start
    st.subheader("📖 Quick Start Guide")
    
    with st.expander("Step 1: Start the Backend Server"):
        st.code("""
        cd D:\\Personalized-Networking-Assistant
        venv\\Scripts\\activate
        uvicorn app.main:app --reload --port 8000
        """, language="bash")
        st.info("Wait for: ✅ Application startup complete")
    
    with st.expander("Step 2: Open this Frontend"):
        st.info("You're already here! 🎉")
        st.caption("If you need to restart: streamlit run frontend/streamlit_app.py")
    
    with st.expander("Step 3: Generate Your First Conversation"):
        st.markdown("""
        1. Navigate to **Generate** page
        2. Enter an event description (e.g., "AI and Machine Learning Conference")
        3. Enter your interests (e.g., "AI, Data Science, Python")
        4. Click **Generate Conversation Starters**
        5. See your personalized suggestions!
        """)
    
    with st.expander("Step 4: Provide Feedback"):
        st.markdown("""
        1. After generating suggestions, click 👍 or 👎 on each
        2. Your feedback helps improve future suggestions
        3. View all feedback in the **Feedback** page
        """)
    
    # Status
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    st.markdown("### 📊 System Status")
    col1, col2 = st.columns(2)
    
    with col1:
        try:
            response = requests.get(f"{st.session_state.base_url}/health", timeout=2)
            if response.status_code == 200:
                st.success("✅ Backend API: Running")
            else:
                st.warning("⚠️ Backend API: Unhealthy")
        except:
            st.error("❌ Backend API: Not reachable")
            st.info("Make sure to start the backend: `uvicorn app.main:app --reload`")
    
    with col2:
        st.success("✅ Frontend: Running")
        st.caption(f"Updated: {datetime.now().strftime('%H:%M:%S')}")