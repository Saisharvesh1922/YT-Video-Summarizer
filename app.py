import streamlit as st
import os
from video_summarizer import process_video
from pdf_utils import create_pdf

# Page configuration
st.set_page_config(
    page_title="AI Video Summarizer Pro",
    page_icon="🎥",
    layout="centered"
)

# Custom CSS for a premium look
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    .summary-box {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
        margin-top: 20px;
        font-size: 1.1em;
        line-height: 1.6;
    }
    .metrics-container {
        display: flex;
        justify-content: space-between;
        margin-top: 10px;
        color: #888;
        font-size: 0.9em;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎥 AI YouTube Video Summarizer")
st.markdown("Paste a YouTube link below to get an AI-generated summary. We now use **Sentence-Aware Chunking** for better quality.")

# Input section
video_url = st.text_input("Enter YouTube URL", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Summarize Video"):
    if video_url:
        try:
            with st.spinner("🚀 Analyzing video... (Step: Download -> Transcribe -> Summarize)"):
                # Run the summarization logic
                transcript, summary = process_video(video_url)
                
                # Store in session state
                st.session_state['summary'] = summary
                st.session_state['transcript'] = transcript
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a valid YouTube URL.")

# Display results if summary exists in session state
if 'summary' in st.session_state:
    st.subheader("📌 AI Summary")
    st.markdown(f'<div class="summary-box">{st.session_state["summary"]}</div>', unsafe_allow_html=True)
    
    # Simple metrics
    word_count_orig = len(st.session_state["transcript"].split())
    word_count_summ = len(st.session_state["summary"].split())
    
    reduction_val = 100 - (word_count_summ / word_count_orig * 100) if word_count_orig > 0 else 0
    
    st.markdown(f"""
    <div class="metrics-container">
        <span>Original Words: {word_count_orig}</span>
        <span>Summary Words: {word_count_summ}</span>
        <span>Reduction: {reduction_val:.1f}%</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Transcript Expander
    with st.expander("📝 View Full Transcript"):
        st.write(st.session_state["transcript"])
    
    st.markdown("---")
    
    # PDF Download section
    pdf_filename = "video_summary.pdf"
    create_pdf(st.session_state['summary'], pdf_filename)
    
    with open(pdf_filename, "rb") as f:
        st.download_button(
            label="📄 Download Summary as PDF",
            data=f,
            file_name=pdf_filename,
            mime="application/pdf"
        )
    
    # Cleanup temp PDF file
    if os.path.exists(pdf_filename):
        os.remove(pdf_filename)

st.sidebar.title("Pro Features Active")
st.sidebar.success("✅ Sentence-Aware Chunking")
st.sidebar.success("✅ Variable Length Summaries")
st.sidebar.info(
    "Using higher-context windows (3000 chars) to ensure better flow and coherence in the summary."
)
st.sidebar.markdown("---")
st.sidebar.write("Developed with Antigravity 🚀")
