import streamlit as st
import json
import os

# Define file path for saving counts
SAVE_FILE = "counts.json"

# GitHub Page URLs for sounds
click_sound_path = "https://ppadiernos.github.io/tally-sounds/click.wav"
reset_sound_path = "https://ppadiernos.github.io/tally-sounds/reset.wav"

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

# Initialize counts from file
if 'counts' not in st.session_state:
    st.session_state.counts = load_counts()

# Track the last clicked category for highlighting
if 'active_category' not in st.session_state:
    st.session_state.active_category = None

# Ensure play_sound exists in session state
if 'play_sound' not in st.session_state:
    st.session_state.play_sound = None

# ----- PAGE TITLE -----
st.title("Response Tally App")

# ----- BROWSER INSTRUCTIONS FOR AUTOPLAY -----
st.markdown(
    """
    **Note**: If you want to hear the button clicks and reset sound every time, you may need to enable audio autoplay in your browser.

    - **Google Chrome**:  
      1. In the address bar, click the lock icon (or "Not Secure" text).  
      2. Select "Site settings" from the dropdown.  
      3. Under "Permissions," find "Sound" or "Autoplay" and set it to "Allow."

    - **Safari**:  
      1. Go to the **Safari** menu → **Settings for This Website**.  
      2. Under "Auto-Play," select **"Allow All Auto-Play"**.  

    After enabling autoplay, refresh this page to ensure repeated sounds are allowed.
    """,
    unsafe_allow_html=True
)

# ----- BUTTON CLICK LOGIC -----
def update_count(category):
    st.session_state.counts[category] += 1
    st.session_state.active_category = category
    save_counts()  # Save to file
    st.session_state.play_sound = "click"  # Queue sound
    st.rerun()  # Force UI refresh

# Layout: Two columns for buttons
col1, col2 = st.columns(2)

# Create buttons dynamically
for index, category in enumerate(st.session_state.counts.keys()):
    if index % 2 == 0:
        with col1:
            if st.button(category, key=category):
                update_count(category)
    else:
        with col2:
            if st.button(category, key=category):
                update_count(category)

# Display current tallies with GREEN highlight for active category
st.subheader("Current Counts")
for category, count in st.session_state.counts.items():
    if category == st.session_state.active_category:
        st.markdown(
            f"<b style='color: green;'>▶ {category}: {count}</b>",
            unsafe_allow_html=True
        )
    else:
        st.write(f"{category}: {count}")

# Reset button
if st.button("Reset Counts"):
    for category in st.session_state.counts:
        st.session_state.counts[category] = 0
    st.session_state.active_category = None
    save_counts()  # Save reset state to file
    st.session_state.play_sound = "reset"  # Queue reset sound
    st.rerun()  # Force UI refresh

# Play sound AFTER the rerun completes
if 'play_sound' in st.session_state and st.session_state.play_sound:
    sound_path = click_sound_path if st.session_state.play_sound == "click" else reset_sound_path
    st.markdown(
        f"""
        <audio id="sound" autoplay>
            <source src="{sound_path}" type="audio/wav">
        </audio>
        <script>
            setTimeout(() => {{
                document.getElementById("sound").pause();
                document.getElementById("sound").currentTime = 0;
            }}, 2000);
        </script>
        """,
        unsafe_allow_html=True,
    )
    st.session_state.play_sound = None  # Clear sound **AFTER** playing
