import streamlit as st
import random

# Initialize session state
if "score" not in st.session_state:
    st.session_state.score = 0
if "message" not in st.session_state:
    st.session_state.message = ""
if "cop_pos" not in st.session_state:
    st.session_state.cop_pos = [2, 1]  # [lane (0-4), x position (0-9)]
if "speeders" not in st.session_state:
    st.session_state.speeders = []  # List of [lane, x] for speeders
if "difficulty" not in st.session_state:
    st.session_state.difficulty = 1
if "moves" not in st.session_state:
    st.session_state.moves = 0

st.title("🚔 I-5 Speed Enforcement - Trooper Life")
st.markdown("**Move your patrol car (🚔) to pull over speeders (🚗) on the highway! Lt. Betts is watching...**")

# Lieutenant Betts yelling area with image
col1, col2 = st.columns([1, 3])
with col1:
    st.image("https://media.istockphoto.com/id/1385108467/vector/angry-army-bootcamp-drill-sergeant-cartoon.jpg?s=612x612&w=0&k=20&c=3fGMt7aLzLa0uRGSZREujosQhE77PNWVKPpH6849GFo=", width=150, caption="Lt. Betts")
with col2:
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
    # Yell more often as score rises
    if random.random() < (0.3 + st.session_state.score / 50):
        st.session_state.message = random.choice(betts_yells)
    st.info(st.session_state.message or "Waiting for your next stop...")

# Score and difficulty
st.metric("Cars Stopped", st.session_state.score)
if st.session_state.score > 10:
    st.warning(f"Traffic heating up! Difficulty: {st.session_state.difficulty:.1f}x")

# Highway grid (5 lanes, 10 positions wide)
def render_highway():
    grid = [["🛣️" for _ in range(10)] for _ in range(5)]  # Empty highway
    # Place speeders
    for lane, x in st.session_state.speeders:
        if 0 <= x < 10:
            grid[lane][x] = "🚗"
    # Place cop car
    lane, x = st.session_state.cop_pos
    grid[lane][x] = "🚔"
    # Render as text grid
    highway_str = "\n".join(" ".join(row) for row in grid)
    st.text_area("I-5 Highway (You are 🚔, Speeders are 🚗)", highway_str, height=150)

render_highway()

# Movement buttons
col_up, col_down, col_left, col_right = st.columns(4)
with col_up:
    if st.button("⬆️ Up"):
        st.session_state.cop_pos[0] = max(0, st.session_state.cop_pos[0] - 1)
        update_game()
with col_down:
    if st.button("⬇️ Down"):
        st.session_state.cop_pos[0] = min(4, st.session_state.cop_pos[0] + 1)
        update_game()
with col_left:
    if st.button("⬅️ Left"):
        st.session_state.cop_pos[1] = max(0, st.session_state.cop_pos[1] - 1)
        update_game()
with col_right:
    if st.button("➡️ Right"):
        st.session_state.cop_pos[1] = min(9, st.session_state.cop_pos[1] + 1)
        update_game()

# Pursuit button for extra action
if st.button("🚨 Activate Lights & Pursue!"):
    # Bonus stop chance
    if random.random() < 0.5:
        st.session_state.score += random.randint(1, 3)
        st.success("Big pursuit! Extra stops!")
        st.balloons()
    else:
        st.warning("They evaded... Keep trying!")
    update_game()

def update_game():
    st.session_state.moves += 1
    # Move speeders left (faster with difficulty)
    for s in st.session_state.speeders:
        s[1] -= int(st.session_state.difficulty)
    # Remove off-screen speeders
    st.session_state.speeders = [s for s in st.session_state.speeders if s[1] >= 0]
    # Check for pulls (adjacent to cop)
    cop_lane, cop_x = st.session_state.cop_pos
    pulled = []
    for i, (lane, x) in enumerate(st.session_state.speeders):
        if abs(lane - cop_lane) <= 1 and abs(x - cop_x) <= 1:
            pulled.append(i)
            st.session_state.score += 1
    for i in sorted(pulled, reverse=True):
        del st.session_state.speeders[i]
    if pulled:
        st.success(f"Pulled over {len(pulled)} speeder(s)!")
    # Spawn new speeders (more with difficulty)
    if random.random() < (0.2 * st.session_state.difficulty):
        new_lane = random.randint(0, 4)
        st.session_state.speeders.append([new_lane, 9])  # Start from right
    # Increase difficulty every 5 moves
    if st.session_state.moves % 5 == 0:
        st.session_state.difficulty += 0.1
    st.rerun()  # Refresh the app

st.markdown("---")
st.caption("Click movement buttons to chase speeders. They move left each turn — catch 'em quick! For even more real-time action, we could switch to Replit or pygbag.")
