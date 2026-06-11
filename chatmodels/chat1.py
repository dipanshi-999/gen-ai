import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mood AI",
    page_icon="🎭",
    layout="centered",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f;
    font-family: 'Inter', sans-serif;
}
[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { max-width: 720px !important; padding: 0 1.5rem 2rem !important; }

.page-title {
    text-align: center;
    padding: 2.2rem 0 1.8rem;
}
.page-title h1 {
    margin: 0 0 0.3rem;
    font-size: 1.7rem;
    font-weight: 700;
    color: #f0f0f6;
    letter-spacing: -0.03em;
}
.page-title p {
    margin: 0;
    font-size: 0.82rem;
    color: #44445a;
    font-family: 'JetBrains Mono', monospace;
}

.mood-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: #44445a;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.7rem;
    font-family: 'JetBrains Mono', monospace;
}

[data-testid="stRadio"] > div {
    display: flex !important;
    flex-direction: row !important;
    gap: 12px !important;
}
[data-testid="stRadio"] label {
    flex: 1;
    display: flex !important;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 0.65rem 0.5rem !important;
    border-radius: 12px !important;
    border: 1px solid #1a1a28 !important;
    background: #111119 !important;
    color: #5a5a78 !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    cursor: pointer;
    transition: all 0.18s !important;
}
[data-testid="stRadio"] label:hover {
    border-color: #2a2a40 !important;
    color: #d0d0e8 !important;
}
[data-testid="stRadio"] input[type="radio"] { display: none !important; }

.divider { border: none; border-top: 1px solid #14141e; margin: 1.5rem 0; }

.chat-bubble-row {
    display: flex;
    gap: 10px;
    margin-bottom: 1rem;
    align-items: flex-end;
}
.chat-bubble-row.user { flex-direction: row-reverse; }

.bubble-avatar {
    width: 32px; height: 32px;
    border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 15px; flex-shrink: 0;
}
.bubble-avatar.bot-angry  { background: #2a0a0a; }
.bubble-avatar.bot-happy  { background: #1f1a06; }
.bubble-avatar.bot-sad    { background: #0a1020; }
.bubble-avatar.user-av    { background: #141420; border: 1px solid #1e1e30; }

.bubble-text {
    max-width: 78%;
    padding: 0.68rem 0.95rem;
    border-radius: 14px;
    font-size: 0.91rem;
    line-height: 1.6;
}
.bubble-text.bot {
    background: #111119;
    color: #c8c8de;
    border: 1px solid #1a1a28;
    border-bottom-left-radius: 4px;
}
.bubble-text.user {
    background: #1e1e30;
    color: #e8e8f8;
    border: 1px solid #2a2a40;
    border-bottom-right-radius: 4px;
}
.bubble-text.bot.angry { border-color: #3a1010; }
.bubble-text.bot.happy { border-color: #2e2610; }
.bubble-text.bot.sad   { border-color: #0e1a30; }

.typing-indicator {
    display: flex; gap: 5px; align-items: center;
    padding: 0.68rem 0.95rem;
    background: #111119; border: 1px solid #1a1a28;
    border-radius: 14px; border-bottom-left-radius: 4px;
    width: fit-content;
}
.typing-indicator span {
    width: 6px; height: 6px;
    background: #44445a; border-radius: 50%;
    animation: tdot 1.2s infinite;
}
.typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
.typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
@keyframes tdot {
    0%,60%,100% { transform: translateY(0); background: #44445a; }
    30% { transform: translateY(-6px); background: var(--mood-color, #888); }
}

.empty-state {
    text-align: center; padding: 3rem 1rem; color: #2a2a3e;
}
.empty-state .big-emoji { font-size: 3rem; margin-bottom: 0.8rem; }
.empty-state p { font-size: 0.87rem; }

[data-testid="stChatInput"] {
    background: #111119 !important;
    border: 1px solid #1a1a28 !important;
    border-radius: 12px !important;
}
[data-testid="stChatInput"]:focus-within { border-color: #2e2e50 !important; }
[data-testid="stChatInput"] textarea {
    color: #d0d0e8 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.91rem !important;
}

.stButton > button {
    background: transparent !important;
    border: 1px solid #1a1a28 !important;
    color: #44445a !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.73rem !important;
    border-radius: 8px !important;
    padding: 0.28rem 0.8rem !important;
}
.stButton > button:hover {
    border-color: #3a3a58 !important;
    color: #8888aa !important;
}
</style>
""", unsafe_allow_html=True)


# ── Model ─────────────────────────────────────────────────────────────────────
@st.cache_resource
def get_model():
    return init_chat_model(
        "meta-llama/llama-4-scout-17b-16e-instruct",
        model_provider="groq",
        temperature=0.9,
    )

model = get_model()

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_mood" not in st.session_state:
    st.session_state.current_mood = None

# ── Page title ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-title">
    <h1>🎭 Mood AI</h1>
    <p>llama-4-scout · groq · pick a mood, start chatting</p>
</div>
""", unsafe_allow_html=True)

# ── Mood selector ─────────────────────────────────────────────────────────────
MOODS = {
    "😠  Angry": ("angry", "You are a very angry AI", "#ff4444"),
    "😄  Happy": ("happy", "You are a happy AI",      "#ffd84d"),
    "😢  Sad":   ("sad",   "You are a sad AI",         "#4d9fff"),
}

st.markdown('<div class="mood-label">Choose your AI agent</div>', unsafe_allow_html=True)
mood_choice = st.radio("mood", list(MOODS.keys()), horizontal=True, label_visibility="collapsed")

mood_key, system_prompt, mood_color = MOODS[mood_choice]

# Reset history when mood changes
if st.session_state.current_mood != mood_key:
    st.session_state.current_mood = mood_key
    st.session_state.messages = [SystemMessage(content=system_prompt)]

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Mood info bar ─────────────────────────────────────────────────────────────
mood_emoji = {"angry": "😠", "happy": "😄", "sad": "😢"}[mood_key]
col1, col2 = st.columns([5, 1])
with col1:
    st.markdown(
        f'<span style="font-size:0.78rem;font-family:JetBrains Mono,monospace;color:{mood_color};">'
        f'{mood_emoji} {mood_key.upper()} MODE ACTIVE</span>',
        unsafe_allow_html=True,
    )
with col2:
    if st.button("clear"):
        st.session_state.messages = [SystemMessage(content=system_prompt)]
        st.rerun()

# ── Chat history ──────────────────────────────────────────────────────────────
visible = [m for m in st.session_state.messages if not isinstance(m, SystemMessage)]

if not visible:
    st.markdown(f"""
    <div class="empty-state">
        <div class="big-emoji">{mood_emoji}</div>
        <p>Your {mood_key} AI is ready — say something!</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in visible:
        if isinstance(msg, HumanMessage):
            st.markdown(f"""
            <div class="chat-bubble-row user">
                <div class="bubble-avatar user-av">🧑</div>
                <div class="bubble-text user">{msg.content}</div>
            </div>
            """, unsafe_allow_html=True)
        elif isinstance(msg, AIMessage):
            st.markdown(f"""
            <div class="chat-bubble-row">
                <div class="bubble-avatar bot-{mood_key}">{mood_emoji}</div>
                <div class="bubble-text bot {mood_key}">{msg.content}</div>
            </div>
            """, unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Type a message…"):
    st.session_state.messages.append(HumanMessage(content=prompt))

    st.markdown(f"""
    <div class="chat-bubble-row user">
        <div class="bubble-avatar user-av">🧑</div>
        <div class="bubble-text user">{prompt}</div>
    </div>
    """, unsafe_allow_html=True)

    typing = st.empty()
    typing.markdown(f"""
    <div class="chat-bubble-row">
        <div class="bubble-avatar bot-{mood_key}">{mood_emoji}</div>
        <div class="typing-indicator" style="--mood-color:{mood_color}">
            <span></span><span></span><span></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    response = model.invoke(st.session_state.messages)
    st.session_state.messages.append(AIMessage(content=response.content))

    typing.empty()
    st.rerun()