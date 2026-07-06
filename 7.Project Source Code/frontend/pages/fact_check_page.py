"""
Fact Check Page - Independent fact verification
Following the Fact-Checking Section pattern
"""

import streamlit as st
import requests


def render():
    """Render the fact check page"""
    
    st.markdown('<p class="main-header">🔍 Fact Check</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        Verify information about any topic using Wikipedia.
        Enter a statement or topic and get verification results.
    </div>
    """, unsafe_allow_html=True)
    
    # Input
    query = st.text_area(
        "What would you like to fact-check?",
        placeholder="Enter a statement or topic to verify...",
        height=80
    )
    
    # Check button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        check_button = st.button("🔎 Check Fact", use_container_width=True, type="primary")
    
    # ============ FACT CHECK RESULT ============
    if check_button and query:
        with st.spinner("🔍 Searching Wikipedia..."):
            try:
                response = requests.post(
                    f"{st.session_state.base_url}/fact-check",
                    json={"query": query},
                    timeout=10
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.fact_check_result = result
                    
                    # Display result
                    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
                    st.subheader("📝 Verification Result")
                    
                    # Color-coded result based on verification status
                    if result.get("verified", False):
                        st.markdown(f"""
                        <div class="fact-verified">
                            ✅ <strong>VERIFIED</strong>
                            <p style="margin-top: 0.5rem;">{result.get('summary', 'No summary available.')}</p>
                            <a href="{result.get('source_url', '#')}" target="_blank">🔗 Source</a>
                        </div>
                        """, unsafe_allow_html=True)
                    elif result.get("summary", "").startswith("No relevant"):
                        st.markdown(f"""
                        <div class="fact-disputed">
                            ❌ <strong>NOT FOUND</strong>
                            <p style="margin-top: 0.5rem;">{result.get('summary', 'No information found.')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="fact-partial">
                            ⚠️ <strong>PARTIAL MATCH</strong>
                            <p style="margin-top: 0.5rem;">{result.get('summary', 'No summary available.')}</p>
                            <a href="{result.get('source_url', '#')}" target="_blank">🔗 Source</a>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Show full response details
                    with st.expander("📄 Show Full Response"):
                        st.json(result)
                    
                else:
                    st.error(f"Error: {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend. Make sure the server is running.")
            except requests.exceptions.Timeout:
                st.error("⏰ Request timed out. Please try again.")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    elif check_button and not query:
        st.warning("Please enter a statement to fact-check.")
    
    # ============ SUGGESTED QUERIES ============
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
    
    st.subheader("💡 Suggested Queries")
    
    suggested_queries = [
        "Artificial Intelligence was first introduced in 1956",
        "Python is a high-level programming language",
        "The Eiffel Tower is located in London",
        "Machine Learning is a subset of Artificial Intelligence",
        "The Earth is flat"
    ]
    
    cols = st.columns(3)
    for i, query_text in enumerate(suggested_queries):
        with cols[i % 3]:
            if st.button(query_text, use_container_width=True):
                # Set the query and trigger check
                st.session_state.fact_check_query = query_text
                # Rerun to display the result
                st.rerun()
    
    # If we have a query from button click, check it
    if 'fact_check_query' in st.session_state:
        query = st.session_state.fact_check_query
        st.session_state.fact_check_query = None
        # Re-run the check
        with st.spinner("🔍 Searching Wikipedia..."):
            try:
                response = requests.post(
                    f"{st.session_state.base_url}/fact-check",
                    json={"query": query},
                    timeout=10
                )
                if response.status_code == 200:
                    result = response.json()
                    st.session_state.fact_check_result = result
                    st.rerun()
            except:
                pass
    
    # Show previous result if exists and no new query
    if st.session_state.fact_check_result and not check_button:
        result = st.session_state.fact_check_result
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.subheader("📝 Last Result")
        
        if result.get("verified", False):
            st.markdown(f"""
            <div class="fact-verified">
                ✅ <strong>VERIFIED</strong>
                <p style="margin-top: 0.5rem;">{result.get('summary', 'No summary available.')}</p>
                <a href="{result.get('source_url', '#')}" target="_blank">🔗 Source</a>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="fact-disputed">
                ❌ <strong>NOT VERIFIED</strong>
                <p style="margin-top: 0.5rem;">{result.get('summary', 'No information found.')}</p>
            </div>
            """, unsafe_allow_html=True)