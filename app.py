
from pathlib import Path

import requests
import streamlit as st


# ---------- Page setup ----------
st.set_page_config(
    page_title="Sorta — Downloads Butler",
    page_icon="🪄",
    layout="wide",
)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:1b"

if "organization_plan" not in st.session_state:
    st.session_state.organization_plan = []

if "activity" not in st.session_state:
    st.session_state.activity = []


# ---------- Styling ----------
st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 8% 8%, #eee7ff 0, transparent 28%),
            radial-gradient(circle at 92% 12%, #e1f5ff 0, transparent 28%),
            #f8f7fc;
        color: #28233d;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1150px;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #25164f, #49318a);
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    .sorta-hero {
        padding: 30px;
        border-radius: 26px;
        background: linear-gradient(115deg, #7654e8, #a45bea, #e878b5);
        color: white;
        box-shadow: 0 14px 32px rgba(105, 73, 190, 0.18);
        margin-bottom: 24px;
    }

    .sorta-hero h1 {
        color: white !important;
        font-size: 2.45rem;
        margin: 0 0 10px 0;
    }

    .sorta-hero p {
        color: white !important;
        font-size: 1.05rem;
        margin: 0;
    }

    .feature-card {
        background: white;
        border: 1px solid #e9e2fb;
        border-radius: 20px;
        padding: 20px;
        min-height: 135px;
        box-shadow: 0 8px 24px rgba(48, 33, 90, 0.06);
    }

    .feature-card .emoji {
        font-size: 1.65rem;
    }

    .feature-card h3 {
        color: #49318a;
        font-size: 1.08rem;
        margin: 8px 0 5px 0;
    }

    .feature-card p {
        color: #746d89;
        font-size: 0.92rem;
        margin: 0;
    }

    [data-testid="stFileUploaderDropzone"] {
        background: white !important;
        border: 2px dashed #a18bea !important;
        border-radius: 20px !important;
        padding: 24px !important;
    }

    [data-testid="stFileUploaderDropzone"] * {
        color: #51466f !important;
    }

    [data-testid="stFileUploaderDropzone"] svg {
        color: #7654e8 !important;
        fill: #7654e8 !important;
    }

    [data-testid="stFileUploaderDropzone"] button {
        background: #7654e8 !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }

    [data-testid="stFileUploaderDropzone"] button * {
        color: white !important;
    }

    div.stButton > button {
        background: linear-gradient(100deg, #7654e8, #a45bea) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        min-height: 46px;
        font-weight: 700;
    }

    h2, h3 {
        color: #30264f;
    }

    .preview-note {
        background: #f0ebff;
        border: 1px solid #ded3ff;
        border-radius: 14px;
        padding: 13px 16px;
        color: #514275;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- Ollama / Gemma helper ----------
def ask_gemma(filename: str) -> str:
    prompt = f"""
You are a careful file organization assistant.

Choose exactly ONE folder from this list:
Images, Documents, Code, Installers, Audio & Video, Spreadsheets, Archives, Review.

Filename: {filename}

Reply with ONLY the exact folder name from the list.
Do not explain. Do not add punctuation.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0},
        },
        timeout=120,
    )
    response.raise_for_status()

    answer = response.json().get("response", "").strip()

    # Validate Gemma's answer so the UI only uses approved folder labels.
    allowed_folders = {
        "Images",
        "Documents",
        "Code",
        "Installers",
        "Audio & Video",
        "Spreadsheets",
        "Archives",
        "Review",
    }

    # Match case-insensitively and tolerate simple underscores.
    normalized = answer.replace("_", " ").strip().lower()

    for folder in allowed_folders:
        if normalized == folder.lower():
            return folder

    # If Gemma returns something unexpected, safely fall back to Review.
    return "Review"


# ---------- Sidebar navigation ----------
with st.sidebar:
    st.markdown("## 🪄 Sorta")
    st.caption("Your Downloads Butler")
    st.divider()

    page = st.radio(
        "Navigate",
        ["Dashboard", "My files", "Activity & undo"],
        label_visibility="collapsed",
    )

    st.divider()
    st.caption("Powered by local Gemma AI")


# ---------- My files page ----------
if page == "My files":
    st.title("📁 My files")
    st.write("Select files to inspect them in this demo.")

    my_files = st.file_uploader(
        "Upload files",
        accept_multiple_files=True,
        key="my_files_uploader",
    )

    if my_files:
        for file in my_files:
            st.write(f"📄 {file.name}")
    else:
        st.info("No files selected yet.")

    st.stop()


# ---------- Activity page ----------
if page == "Activity & undo":
    st.title("↶ Activity")

    if st.session_state.activity:
        for event in reversed(st.session_state.activity):
            st.write(f"• {event}")
    else:
        st.info("No activity yet. Create a preview on the Dashboard.")

    if st.session_state.organization_plan:
        st.subheader("Latest AI preview")
        for item in st.session_state.organization_plan:
            st.write(f"📄 **{item['name']}** → 📁 `{item['folder']}/`")

    st.warning("Sorta is preview-only right now. It has not changed your files.")
    st.stop()


# ---------- Dashboard ----------
st.markdown(
    """
    <div class="sorta-hero">
        <h1>✨ A calmer Downloads folder</h1>
        <p>Let local AI suggest where your files belong. You review everything first.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="emoji">📥</div>
            <h3>Upload</h3>
            <p>Choose files for your preview.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="emoji">🧠</div>
            <h3>Gemma AI</h3>
            <p>Get a folder suggestion from your local model.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="emoji">🛡️</div>
            <h3>Safe preview</h3>
            <p>No files are moved or deleted.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")
st.subheader("📂 Try Sorta")

files = st.file_uploader(
    "Drop files here, or click Browse files",
    accept_multiple_files=True,
    key="dashboard_uploader",
)

if files:
    st.success(f"Selected {len(files)} file(s).")

    with st.expander("View selected files"):
        for file in files:
            st.write(f"📄 {file.name} · {file.size:,} bytes")

    if st.button("✨ Create AI organization preview", use_container_width=True):
        suggestions = []

        progress = st.progress(0, text="Gemma is looking at your filenames…")

        try:
            for index, file in enumerate(files):
                folder = ask_gemma(file.name)
                suggestions.append(
                    {
                        "name": file.name,
                        "folder": folder,
                    }
                )
                progress.progress(
                    (index + 1) / len(files),
                    text=f"Analyzed {index + 1} of {len(files)} file(s)…",
                )

            st.session_state.organization_plan = suggestions
            st.session_state.activity.append(
                f"Gemma generated a preview for {len(files)} file(s)."
            )
            progress.empty()
            st.rerun()

        except requests.exceptions.ConnectionError:
            progress.empty()
            st.error(
                "Couldn't reach Ollama. Make sure the Ollama app is running "
                "and Gemma is installed (`ollama run gemma3:1b`)."
            )

        except requests.exceptions.Timeout:
            progress.empty()
            st.error("Gemma took too long to respond. Try fewer files or try again.")

        except requests.exceptions.RequestException as error:
            progress.empty()
            st.error(f"Ollama request failed: {error}")


# ---------- Results ----------
if st.session_state.organization_plan:
    st.divider()
    st.subheader("✨ Gemma's organization suggestions")

    for item in st.session_state.organization_plan:
        st.write(f"📄 **{item['name']}**  →  📁 `{item['folder']}/`")

    st.markdown(
        """
        <div class="preview-note">
        Suggestions are generated by local Gemma AI. This is only a preview:
        Sorta has not moved, renamed, or deleted anything.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Clear preview"):
        st.session_state.organization_plan = []
        st.rerun()
