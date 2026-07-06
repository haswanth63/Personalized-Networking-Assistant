"""
Feedback Page - View feedback history
Following the Feedback History View pattern
"""

import streamlit as st
import requests
from datetime import datetime


def render():
    """Render the feedback page"""
    
    st.markdown('<p class="main-header">📊 Feedback History</p>', unsafe_allow_html=True)
    
    # ============ LOAD FEEDBACK ============
    try:
        # Get feedback stats
        stats_response = requests.get(f"{st.session_state.base_url}/feedback/stats")
        
        if stats_response.status_code == 200:
            stats = stats_response.json()
            
            # Stats cards
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Feedback", stats.get("total", 0))
            with col2:
                st.metric("👍 Likes", stats.get("likes", 0))
            with col3:
                st.metric("👎 Dislikes", stats.get("dislikes", 0))
            with col4:
                like_rate = stats.get("like_rate", 0) * 100
                st.metric("Like Rate", f"{like_rate:.0f}%")
        
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        
        # ============ FEEDBACK LIST ============
        st.subheader("📋 Recent Feedback")
        
        # Show feedback directly from file (following documentation pattern)
        import json
        from pathlib import Path
        
        feedback_path = Path("data") / "feedback.json"
        
        if st.button("📊 Show Feedback", use_container_width=True):
            if feedback_path.exists():
                with open(feedback_path, "r", encoding="utf-8") as f:
                    feedback_data = json.load(f)
                
                if feedback_data:
                    # Show latest 10 (following documentation)
                    recent_feedback = list(reversed(feedback_data[-10:]))
                    
                    for item in recent_feedback:
                        # Ternary expression for icon
                        icon = "👍" if item.get("feedback") == "like" else "👎"
                        suggestion = item.get("suggestion", "No suggestion")
                        timestamp = item.get("timestamp", "Unknown time")
                        
                        # Format timestamp
                        try:
                            dt = datetime.fromisoformat(timestamp)
                            formatted_time = dt.strftime("%Y-%m-%d %H:%M")
                        except:
                            formatted_time = timestamp[:16]
                        
                        st.markdown(f"""
                        <div class="history-entry">
                            <div style="display: flex; align-items: center; gap: 0.5rem;">
                                <span style="font-size: 1.5rem;">{icon}</span>
                                <span><strong>{suggestion}</strong></span>
                            </div>
                            <div style="margin-top: 0.3rem;">
                                <span style="color: #6c757d; font-size: 0.85rem;">
                                    🕐 {formatted_time}
                                </span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("---")
                else:
                    st.info("No feedback submitted yet.")
            else:
                st.info("No feedback file found. Submit some feedback to see it here!")
        
        # Alternative: Show from API
        st.caption("Or view from API:")
        if st.button("🔄 Refresh from API", use_container_width=True):
            try:
                response = requests.get(f"{st.session_state.base_url}/history")
                if response.status_code == 200:
                    data = response.json()
                    entries = data.get("entries", [])
                    
                    if entries:
                        st.success(f"Found {len(entries)} entries")
                        for entry in entries[:5]:
                            suggestions = entry.get("suggestions", [])
                            for s in suggestions:
                                st.info(f"💬 {s}")
                    else:
                        st.info("No entries found")
            except:
                st.error("Failed to fetch from API")
        
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend. Make sure the server is running.")
    except Exception as e:
        st.error(f"Error: {str(e)}")