import streamlit as st
import random
import time

# Simple state to track game progress
if "score" not in st.session_state:
    st.session_state.score = 0
if "message" not in st.session_state:
    st.session_state.message = ""
if "game_active" not in st.session_state:
    st.session_state.game_active = False

st.title("🚔 I-5 Speed Enforcement - Trooper Life")
st.markdown("**You're a Washington State Trooper on I-5. Pull over speeders before Lt. Betts loses it!**")

# Lieutenant Betts yelling area
st.subheader("Lt. Betts on the radio:")
betts_yells = [
    "Trooper! Where are the tickets?! MOVE IT!",
    "You're letting them get away! STEP ON IT!",
    "I want FIVE more stops THIS HOUR!",
    "That's a 90 in a 70 — PULL HIM OVER NOW!",
    "Betts to unit — quit sightseeing and write some citations!",
    "My grandmother drives faster than you pull people over!",
    "Quota time is ticking, trooper!",
    "I see THREE speeders — why aren't they stopped yet?!"
]

# Display random yell every few interactions
if random.random() < 0.4:
    st.session_state.message = random.choice(betts_yells)

st.info(st.session_state.message or "Waiting for your next stop...")

# Score display
st.metric("Cars Stopped", st.session_state.score)

# Game controls (click to "patrol" and stop cars)
col1, col2 = st.columns(2)

with col1:
    if st.button("🚨 Patrol the highway & spot a speeder", use_container_width=True):
        st.session_state.game_active = True
        time.sleep(1.5)  # Fake "searching" delay
        if random.random() < 0.7:  # 70% chance of success
            st.session_state.score += 1
            st.success("🚨 Pulled over a speeder! Nice work, Trooper!")
            st.balloons()
        else:
            st.warning("Missed 'em... they got away this time.")

with col2:
    if st.button("🔵 Activate lights & pursue!", use_container_width=True, disabled=not st.session_state.game_active):
        st.session_state.game_active = False
        st.session_state.score += random.randint(1, 3)
        st.success(f"Big pursuit! Stopped {st.session_state.score - (st.session_state.score - random.randint(1,3))} more cars!")
        st.session_state.message = random.choice(betts_yells[:3])  # Angry praise

# Difficulty ramp-up simulation
if st.session_state.score > 10:
    st.warning("Traffic is getting heavier... Lt. Betts is watching!")

st.markdown("---")
st.caption("This is a simple web version — click buttons to simulate stops. For a full real-time game, we'd need a different platform like Replit or pygbag.")
