# from dotenv import load_dotenv
# from langchain.chat_models import init_chat_model
# from langchain_core.prompts import ChatPromptTemplate

# load_dotenv()

# model = init_chat_model(
#     "meta-llama/llama-4-scout-17b-16e-instruct",
#     model_provider="groq",
# )

# prompt = ChatPromptTemplate.from_messages([
#     (
#         "system",
#         """
# You are an expert Information Extraction Agent.

# Analyze the given paragraph and extract the most useful information.

# Please provide:

# 1. Entity Type (Movie, Book, Company, Person, Event, Product, etc.)
# 2. Title / Name
# 3. Important People
# 4. Genre / Category
# 5. Release Year / Date (if available)
# 6. Main Topic or Plot
# 7. Ratings or Scores (if available)
# 8. Important Keywords
# 9. Interesting Facts
# 10. A quick summary (2-3 lines)
#         """
#     ),
#     (
#         "human",
#         """
# Extract information from this paragraph:

# {paragraph}
#         """
#     )
# ])

# print("Paste your paragraph (type END on a new line when finished):")

# lines = []

# while True:
#     line = input()
#     if line == "END":
#         break
#     lines.append(line)

# para = "\n".join(lines)

# final_prompt = prompt.invoke(
#     {"paragraph": para}
# )

# response = model.invoke(final_prompt)

# print(response.content)


import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Info Extractor",
    page_icon="🔍",
    layout="centered",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #09090e;
    font-family: 'Inter', sans-serif;
}
[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { max-width: 740px !important; padding: 0 1.5rem 3rem !important; }

/* ── Title ── */
.page-title {
    text-align: center;
    padding: 2.4rem 0 2rem;
}
.page-title h1 {
    margin: 0 0 0.35rem;
    font-size: 1.75rem;
    font-weight: 700;
    color: #f0f0f6;
    letter-spacing: -0.03em;
}
.page-title p {
    margin: 0;
    font-size: 0.8rem;
    color: #3a3a52;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Section label ── */
.section-label {
    font-size: 0.74rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #3a3a52;
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 0.55rem;
}

/* ── Textarea override ── */
[data-testid="stTextArea"] textarea {
    background: #111118 !important;
    border: 1px solid #1c1c2c !important;
    border-radius: 12px !important;
    color: #c8c8de !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.91rem !important;
    line-height: 1.65 !important;
    resize: vertical !important;
    caret-color: #7c6fff;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: #7c6fff !important;
    box-shadow: 0 0 0 3px rgba(124,111,255,0.12) !important;
}
[data-testid="stTextArea"] textarea::placeholder { color: #2e2e48 !important; }

/* ── Button ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #7c6fff 0%, #a855f7 100%) !important;
    border: none !important;
    border-radius: 11px !important;
    color: #fff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.92rem !important;
    font-weight: 600 !important;
    padding: 0.65rem 1.2rem !important;
    letter-spacing: -0.01em;
    transition: opacity 0.18s !important;
    margin-top: 0.4rem;
}
.stButton > button:hover { opacity: 0.88 !important; }
.stButton > button:disabled { opacity: 0.35 !important; }

/* ── Divider ── */
.divider { border: none; border-top: 1px solid #13131e; margin: 1.8rem 0; }

/* ── Result card ── */
.result-card {
    background: #111118;
    border: 1px solid #1c1c2c;
    border-radius: 14px;
    padding: 1.5rem 1.6rem;
    color: #c8c8de;
    font-size: 0.91rem;
    line-height: 1.75;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Spinner ── */
[data-testid="stSpinner"] { color: #7c6fff !important; }
</style>
""", unsafe_allow_html=True)

# ── Model & prompt ────────────────────────────────────────────────────────────
@st.cache_resource
def get_model():
    return init_chat_model(
        "meta-llama/llama-4-scout-17b-16e-instruct",
        model_provider="groq",
    )

model = get_model()

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an expert Information Extraction Agent.

Analyze the given paragraph and extract the most useful information.

Please provide:

1. Entity Type (Movie, Book, Company, Person, Event, Product, etc.)
2. Title / Name
3. Important People
4. Genre / Category
5. Release Year / Date (if available)
6. Main Topic or Plot
7. Ratings or Scores (if available)
8. Important Keywords
9. Interesting Facts
10. A quick summary (2-3 lines)
        """
    ),
    (
        "human",
        """
Extract information from this paragraph:

{paragraph}
        """
    )
])

# ── UI ────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-title">
    <h1>🔍 Info Extractor</h1>
    <p>llama-4-scout · groq · paste a paragraph, get structured insights</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-label">Paste your paragraph</div>', unsafe_allow_html=True)

paragraph = st.text_area(
    label="paragraph",
    placeholder="Paste any paragraph here — about a movie, book, person, event, company, product…",
    height=200,
    label_visibility="collapsed",
)

extract_btn = st.button("Extract Information", disabled=not paragraph.strip())

# ── Result ────────────────────────────────────────────────────────────────────
if extract_btn and paragraph.strip():
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Extracted Information</div>', unsafe_allow_html=True)

    with st.spinner("Analysing paragraph…"):
        final_prompt = prompt.invoke({"paragraph": paragraph})
        response = model.invoke(final_prompt)

    st.markdown(
        f'<div class="result-card">{response.content}</div>',
        unsafe_allow_html=True,
    )
