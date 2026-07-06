"""
Generate Page - Main conversation generation flow
Following Input Section and Main Generation Flow pattern
"""

import streamlit as st
import requests
import json
from datetime import datetime


def render():
    """Render the generate page"""
    
    st.markdown('<p class="main-header">💬 Generate Conversation Starters</p>', unsafe_allow_html=True)
    
    # ============ INPUT SECTION ============
    # Following the Input Section pattern from documentation
    
    st.subheader("📝 Input")
    
    # Event description
    event_description = st.text_area(
        "Event Description",
        placeholder="Describe the networking event you're attending...",
        height=100,
        value=st.session_state.event_description
    )
    st.session_state.event_description = event_description
    
    # User interests
    user_interests = st.text_input(
        "Your Interests (comma-separated)",
        placeholder="e.g., AI, Machine Learning, Data Science, Python",
        value=st.session_state.user_interests
    )
    st.session_state.user_interests = user_interests
    
    # Number of suggestions
    max_suggestions = st.slider(
        "Number of suggestions",
        min_value=1,
        max_value=5,
        value=3
    )
    
    # Generate button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_button = st.button(
            "🚀 Generate Conversation Starters",
            use_container_width=True,
            type="primary"
        )
    
    # ============ GENERATION LOGIC ============
    if generate_button and event_description and user_interests:
        # Parse interests
        interests_list = [i.strip() for i in user_interests.split(',') if i.strip()]
        
        if not interests_list:
            st.warning("Please enter at least one interest.")
            return
        
        # Set generating state
        st.session_state.generating = True
        
        # Show spinner
        with st.spinner("🤖 Generating conversation starters..."):
            try:
                # Call backend API
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
                    
                    # Store in session state
                    st.session_state.generated_suggestions = data.get("suggestions", [])
                    st.session_state.extracted_themes = data.get("extracted_themes", [])
                    st.session_state.session_id = data.get("history_id")
                    st.session_state.show_results = True
                    st.session_state.feedback_submitted = {}
                    
                    st.success(f"✅ Generated {len(st.session_state.generated_suggestions)} suggestions!")
                    st.rerun()
                else:
                    st.error(f"Error: {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend. Make sure the server is running.")
            except requests.exceptions.Timeout:
                st.error("⏰ Request timed out. Please try again.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        st.session_state.generating = False
    
    elif generate_button and not event_description:
        st.warning("Please enter an event description.")
    elif generate_button and not user_interests:
        st.warning("Please enter your interests.")
    
    # ============ RESULTS DISPLAY ============
    # Following the Results Display pattern from documentation
    
    if st.session_state.show_results and st.session_state.generated_suggestions:
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # Show extracted themes
        if st.session_state.extracted_themes:
            st.subheader("🎯 Extracted Themes")
            theme_html = "".join([
                f'<span class="theme-tag">#{theme}</span>'
                for theme in st.session_state.extracted_themes
            ])
            st.markdown(f"<div>{theme_html}</div>", unsafe_allow_html=True)
        
        # Show suggestions
        st.subheader("💡 Conversation Starters")
        st.caption(f"Session: {st.session_state.session_id or 'N/A'}")
        
        # Display each suggestion with feedback buttons
        for i, suggestion in enumerate(st.session_state.generated_suggestions):
            # Check if feedback already submitted for this suggestion
            fb_key = f"fb_{i}_{suggestion[:20]}"
            feedback_submitted = st.session_state.feedback_submitted.get(fb_key, False)
            
            # Suggestion card
            st.markdown(f"""
            <div class="suggestion-card">
                <strong>Suggestion {i+1}</strong>
                <p style="font-size: 1.05rem; margin-top: 0.3rem;">{suggestion}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Feedback buttons
            col1, col2, col3 = st.columns([1, 1, 5])
            
            with col1:
                # Like button
                if not feedback_submitted:
                    if st.button("👍", key=f"like_{i}"):
                        # Submit feedback
                        try:
                            feedback_data = {
                                "suggestion": suggestion,
                                "action": "like"
                            }
                            response = requests.post(
                                f"{st.session_state.base_url}/feedback",
                                json=feedback_data
                            )
                            if response.status_code == 200:
                                st.session_state.feedback_submitted[fb_key] = "like"
                                st.success("Thank you for your feedback! 👍")
                                st.rerun()
                            else:
                                st.error("Failed to submit feedback")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
            
            with col2:
                if not feedback_submitted:
                    if st.button("👎", key=f"dislike_{i}"):
                        try:
                            feedback_data = {
                                "suggestion": suggestion,
                                "action": "dislike"
                            }
                            response = requests.post(
                                f"{st.session_state.base_url}/feedback",
                                json=feedback_data
                            )
                            if response.status_code == 200:
                                st.session_state.feedback_submitted[fb_key] = "dislike"
                                st.success("Thank you for your feedback! 👎")
                                st.rerun()
                            else:
                                st.error("Failed to submit feedback")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
            
            with col3:
                if feedback_submitted:
                    status = st.session_state.feedback_submitted[fb_key]
                    if status == "like":
                        st.markdown("✅ Liked")
                    else:
                        st.markdown("✅ Disliked")
            
            st.markdown("---")
        
        # Regenerate option
        if st.button("🔄 Regenerate Suggestions", use_container_width=True):
            st.session_state.show_results = False
            st.session_state.generated_suggestions = []
            st.rerun()
    
    # ============ USAGE TIPS ============
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    with st.expander("💡 Tips for Better Results"):
        st.markdown("""
        **For Event Description:**
        - Be specific about the event theme
        - Mention the industry or field
        - Include keywords like "conference", "workshop", "meetup"
        
        **For Interests:**
        - List specific topics, not general ones
        - Include both professional and personal interests
        - Separate with commas (e.g., "AI, Python, Data Science")
        
        **Example:**
        - Event: "Tech Connect 2025 - A conference on AI and Machine Learning innovations"
        - Interests: "Artificial Intelligence, Python Programming, Deep Learning"
        """)