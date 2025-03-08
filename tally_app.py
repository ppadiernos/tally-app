import streamlit as st
import json
import os

# Define file path for saving counts
SAVE_FILE = "counts.json"

# Function to load counts from file
def load_counts():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return {
        "Ontopic General": 0,
        "Ontopic Cultural": 0,
        "Ontopic Profane": 0,
        "Ontopic Hate Speech": 0,
        "Ontopic OMCA Feedback": 0,
        "Off Topic General": 0,
        "Off Topic Cultural": 0,
        "Off Topic Profane": 0,
        "Off Topic Hate Speech": 0,
        "Off Topic OMCA Feedback": 0,
    }

# Function to save counts to file
def save_counts():
    with open(SAVE_FILE, "w") as f:
        json.dump(st.session_state.counts, f)

# Initialize counts and other state variables
if "counts" not in st.session_state:
    st.session_state.counts = load_counts()
if "active_category" not in st.session_state:
    st.session_state.active_category = None
if "last_action" not in st.session_state:
    st.session_state.last_action = None
if "redo_action" not in st.session_state:
    st.session_state.redo_action = None
if "confirm_reset" not in st.session_state:
    st.session_state.confirm_reset = False

st.title("Talkback Counter")

# ----- BUTTON CLICK LOGIC -----
def update_count(category):
    st.session_state.counts[category] += 1
    st.session_state.active_category = category
    st.session_state.last_action = {"category": category, "delta": 1}
    st.session_state.redo_action = None
    save_counts()

def undo_last_action():
    action = st.session_state.last_action
    if action:
        cat = action["category"]
        st.session_state.counts[cat] = max(0, st.session_state.counts[cat] - action["delta"])
        st.session_state.redo_action = action
        st.session_state.last_action = None
        save_counts()

def redo_last_action():
    action = st.session_state.redo_action
    if action:
        cat = action["category"]
        st.session_state.counts[cat] += action["delta"]
        st.session_state.last_action = action
        st.session_state.redo_action = None
        save_counts()

def reset_counts():
    for category in st.session_state.counts:
        st.session_state.counts[category] = 0
    st.session_state.active_category = None
    save_counts()
    st.session_state.confirm_reset = False

# Remove sound functions and variables
# Also, we remove the blue hover effect by not injecting any custom hover CSS

# We'll keep a simple CSS for our count cells so they have white text and are centered.
st.markdown("""
<style>
.count-cell {
    color: white;
    text-align: center;
    padding: 5px;
}
</style>
""", unsafe_allow_html=True)

# Group categories into Ontopic and Off Topic
ontopic_categories = [cat for cat in st.session_state.counts if cat.startswith("Ontopic")]
offtopic_categories = [cat for cat in st.session_state.counts if cat.startswith("Off Topic")]

# Layout: Two columns for groups
cols = st.columns(2)

# --- Ontopic Group ---
with cols[0]:
    st.subheader("Ontopic")
    # Header row for this group
    header_cols = st.columns([3, 1])
    with header_cols[0]:
        st.markdown("<b>Category</b>", unsafe_allow_html=True)
    with header_cols[1]:
        st.markdown("<b>Count</b>", unsafe_allow_html=True)
    # For each Ontopic category, display a row with the button and count
    for cat in ontopic_categories:
        row = st.columns([3, 1])
        with row[0]:
            label = f"▶ {cat}" if cat == st.session_state.active_category else cat
            st.button(label, on_click=update_count, args=(cat,), key=f"ontopic_{cat}")
        with row[1]:
            count = st.session_state.counts[cat]
            if cat == st.session_state.active_category:
                st.markdown(f"<div class='count-cell'><span style='color: green; font-weight: bold;'>{count}</span></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='count-cell'>{count}</div>", unsafe_allow_html=True)

# --- Off Topic Group ---
with cols[1]:
    st.subheader("Off Topic")
    header_cols = st.columns([3, 1])
    with header_cols[0]:
        st.markdown("<b>Category</b>", unsafe_allow_html=True)
    with header_cols[1]:
        st.markdown("<b>Count</b>", unsafe_allow_html=True)
    for cat in offtopic_categories:
        row = st.columns([3, 1])
        with row[0]:
            label = f"▶ {cat}" if cat == st.session_state.active_category else cat
            st.button(label, on_click=update_count, args=(cat,), key=f"offtopic_{cat}")
        with row[1]:
            count = st.session_state.counts[cat]
            if cat == st.session_state.active_category:
                st.markdown(f"<div class='count-cell'><span style='color: green; font-weight: bold;'>{count}</span></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='count-cell'>{count}</div>", unsafe_allow_html=True)

# --- Undo/Redo Buttons (styled distinctly) ---
st.markdown("""
<style>
.undo-redo-container button {
    font-size: 1.2em;
    padding: 10px 20px;
    background-color: #e6e6fa;
    border: 2px solid #4CAF50;
    border-radius: 8px;
    margin: 5px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="undo-redo-container">', unsafe_allow_html=True)
undo_redo_cols = st.columns(2)
with undo_redo_cols[0]:
    if st.button("⏪ Undo Last Action", key="undo-button", disabled=st.session_state.last_action is None):
        undo_last_action()
with undo_redo_cols[1]:
    if st.button("⏩ Redo Last Action", key="redo-button", disabled=st.session_state.redo_action is None):
        redo_last_action()
st.markdown('</div>', unsafe_allow_html=True)

# --- Reset Button with Confirmation ---
if st.button("Reset Counts", key="reset"):
    st.session_state.confirm_reset = True

if st.session_state.confirm_reset:
    st.warning("Are you sure you want to reset counts? (Double click to confirm)")
    conf_cols = st.columns(2)
    with conf_cols[0]:
        if st.button("Confirm Reset"):
            reset_counts()
    with conf_cols[1]:
        if st.button("Cancel Reset"):
            st.session_state.confirm_reset = False
