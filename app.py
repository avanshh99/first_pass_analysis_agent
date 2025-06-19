import streamlit as st
import requests
import time
import os

# Configuration
BACKEND_URL = "http://localhost:5000"

st.set_page_config(page_title="Pitch Deck Analyst", layout="wide")
st.title("🚀 Pitch Deck Analyst")

uploaded_file = st.file_uploader("Upload a PDF pitch deck", type="pdf", accept_multiple_files=False)

if st.button("Analyze", key="analyze_button"):
    if uploaded_file is not None:
        try:
            # Verify file type
            if uploaded_file.type != "application/pdf":
                st.error("Invalid file type. Please upload a PDF file.")
                st.stop()
            
            # Check file size
            if uploaded_file.size > 200 * 1024 * 1024:  # 200MB limit
                st.error("File too large. Maximum size is 200MB.")
                st.stop()
                
            with st.spinner("Processing document..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                upload_response = requests.post(
                    f"{BACKEND_URL}/upload", 
                    files=files
                )
                
                if upload_response.status_code != 200:
                    error_msg = upload_response.json().get('error', 'Unknown error occurred')
                    st.error(f"Upload failed: {error_msg}")
                    st.stop()
            
            # ============= ANALYSIS SECTION =============
            with st.spinner("Analyzing content..."):
                # Get analysis from backend
                analysis_response = requests.get(f"{BACKEND_URL}/analyze")
                
                if analysis_response.status_code == 200:
                    analysis = analysis_response.json()
                    
                    # Display results in expandable sections
                    st.success("Analysis complete!")
                    
                    with st.expander("📌 Business Summary", expanded=True):
                        st.write(analysis.get("summary", "No summary available"))
                    
                    with st.expander("👥 Team Analysis", expanded=True):
                        st.write(analysis.get("team_analysis", "No team information found"))
                    
                    # Optional: Add download button
                    st.download_button(
                        label="Download Analysis",
                        data=str(analysis),
                        file_name="pitch_deck_analysis.txt",
                        mime="text/plain"
                    )
                else:
                    error_msg = analysis_response.json().get('error', 'Analysis failed')
                    st.error(f"Analysis error: {error_msg}")
            # ============= END ANALYSIS SECTION =============
            
        except requests.exceptions.ConnectionError:
            st.error("Backend service unavailable. Please ensure the Flask server is running.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
    else:
        st.warning("Please upload a PDF file first")

# Optional: Add instructions section
with st.expander("ℹ️ How to use this tool"):
    st.markdown("""
    **Instructions:**
    1. Upload a startup pitch deck in PDF format
    2. Click the 'Analyze' button
    3. View the automatic analysis of:
       - Business concept summary
       - Founding team information
    4. Download the results if needed
    
    **Note:** Works best with text-based PDFs (not scanned documents)
    """)