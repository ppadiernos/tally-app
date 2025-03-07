import streamlit as st

# Initialize counts for 10 categories in session state
if 'counts' not in st.session_state:
    st.session_state.counts = {
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

st.title("Response Tally App")

# Layout: Two columns for buttons
col1, col2 = st.columns(2)

# Create buttons dynamically
for index, category in enumerate(st.session_state.counts.keys()):
    if index % 2 == 0:
        with col1:
            if st.button(category):
                st.session_state.counts[category] += 1
    else:
        with col2:
            if st.button(category):
                st.session_state.counts[category] += 1

# Display current tallies
st.subheader("Current Counts")
for category, count in st.session_state.counts.items():
    st.write(f"**{category}:** {count}")

# Reset button
if st.button("Reset Counts"):
    for category in st.session_state.counts:
        st.session_state.counts[category] = 0
    st.experimental_rerun()
