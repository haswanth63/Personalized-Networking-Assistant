"""
Manual Testing Script
For verifying the UI works correctly
"""

import streamlit as st
import requests
import json
from datetime import datetime

st.set_page_config(
    page_title="Manual Testing - Networking Assistant",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 Manual Testing Dashboard")
st.markdown("---")

# Backend status
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔌 Backend Status")
    try:
        response = requests.get("http://127.0.0.1:8000/health", timeout=2)
        if response.status_code == 200:
            st.success("✅ Backend is running")
        else:
            st.warning("⚠️ Backend is unhealthy")
    except:
        st.error("❌ Backend is not running")
        st.info("Start backend: uvicorn app.main:app --reload --port 8000")

with col2:
    st.subheader("🌐 Frontend Status")
    st.success("✅ Frontend is running")
    st.caption(f"Updated: {datetime.now().strftime('%H:%M:%S')}")

st.markdown("---")

# Quick test sections
st.subheader("🧪 Quick Tests")

test_col1, test_col2 = st.columns(2)

with test_col1:
    if st.button("1. Test Event Analysis", use_container_width=True):
        try:
            payload = {"description": "AI and Machine Learning Conference"}
            response = requests.post("http://127.0.0.1:8000/analyze-event", json=payload)
            if response.status_code == 200:
                st.success("✅ Event analysis successful!")
                st.json(response.json())
            else:
                st.error(f"❌ Error: {response.text}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

with test_col2:
    if st.button("2. Test Fact Check", use_container_width=True):
        try:
            payload = {"query": "Artificial Intelligence"}
            response = requests.post("http://127.0.0.1:8000/fact-check", json=payload)
            if response.status_code == 200:
                st.success("✅ Fact check successful!")
                st.json(response.json())
            else:
                st.error(f"❌ Error: {response.text}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

col3, col4 = st.columns(2)

with col3:
    if st.button("3. Test Generate Conversation", use_container_width=True):
        try:
            payload = {
                "event_description": "Tech Networking Event",
                "user_interests": ["AI", "Data Science"],
                "max_suggestions": 3
            }
            response = requests.post("http://127.0.0.1:8000/generate-conversation", json=payload)
            if response.status_code == 200:
                st.success("✅ Generation successful!")
                data = response.json()
                st.json(data)
                if data.get("suggestions"):
                    st.info("Suggestions:")
                    for s in data["suggestions"]:
                        st.write(f"• {s}")
            else:
                st.error(f"❌ Error: {response.text}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

with col4:
    if st.button("4. Test History", use_container_width=True):
        try:
            response = requests.get("http://127.0.0.1:8000/history")
            if response.status_code == 200:
                st.success("✅ History loaded!")
                data = response.json()
                st.metric("Total Conversations", data.get("total", 0))
                if data.get("entries"):
                    st.write("Latest:")
                    for entry in data["entries"][:3]:
                        st.write(f"• {entry.get('event_description', 'N/A')[:50]}...")
            else:
                st.error(f"❌ Error: {response.text}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

st.markdown("---")

# All tests button
st.subheader("🚀 Run All Tests")

if st.button("Run All Tests", type="primary", use_container_width=True):
    results = []
    
    tests = [
        ("Health Check", lambda: requests.get("http://127.0.0.1:8000/health")),
        ("Analyze Event", lambda: requests.post("http://127.0.0.1:8000/analyze-event", json={"description": "Test"})),
        ("Fact Check", lambda: requests.post("http://127.0.0.1:8000/fact-check", json={"query": "Test"})),
    ]
    
    for name, test_func in tests:
        try:
            response = test_func()
            if response.status_code == 200:
                results.append(f"✅ {name}: Passed")
            else:
                results.append(f"❌ {name}: Failed ({response.status_code})")
        except Exception as e:
            results.append(f"❌ {name}: Error ({str(e)})")
    
    for result in results:
        if "✅" in result:
            st.success(result)
        else:
            st.error(result)