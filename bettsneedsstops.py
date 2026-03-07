import streamlit as st
import random
import time

st.set_page_config(page_title="I-5 Patrol Dash", layout="wide")

# CSS for game vibe
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bangers&display=swap');

    .betts-yell {
        background: #ff0000;
        color: #ffff00;
        font-family: 'Bangers', cursive;
        font-size: 48px;
        text-align: center;
        padding: 30px;
        border: 8px solid #000;
        border-radius: 15px;
        margin: 20px 0;
        text-shadow: 3px 3px 6px #000;
        box-shadow: 0 0 20px #ff4500;
    }

    .betts-face {
        display: block;
        margin: 0 auto 15px;
        border: 5px solid #ffd700;
        border-radius: 50%;
        box-shadow: 0 0 20px #ff4500;
    }

    .highway {
        background: linear-gradient(to bottom, #228B22 40%, #556B2F 100%);
        border: 5px dashed #FF8C00;
        border-radius: 20px;
        padding: 20px;
        margin: 20px 0;
        min-height: 400px;
    }
    </style>
""", unsafe_allow_html=True)

# Angry Betts
BETTS_IMG = "https://thumbs.dreamstime.com/b/angry-army-bootcamp-drill-sergeant-soldier-shouting-cartoon-209860607.jpg"

st.title("🚔 I-5 Patrol Dash – Flappy Style!")

st.image(BETTS_IMG, width=280, caption="Lt. Scott Betts – YELLING AT YOU!", class_="betts-face")

st.markdown(f'<div class="betts-yell">{st.session_state.get("message", "FLY THROUGH THE HIGHWAY – AVOID DEBRIS!")}</div>', unsafe_allow_html=True)

# State
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'car_y' not in st.session_state:
    st.session_state.car_y = 200
if 'game_running' not in st.session_state:
    st.session_state.game_running = False
if 'obstacles' not in st.session_state:
    st.session_state.obstacles = []
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()
if 'message' not in st.session_state:
    st.session_state.message = "CLICK/SPACE TO JUMP – DON'T HIT DEBRIS!"

highway = st.container()
with highway:
    st.markdown('<div class="highway">', unsafe_allow_html=True)

    if not st.session_state.game_running:
        st.markdown("**Patrol car (🚔) drives right. Click or press SPACE to jump up. Avoid debris/cars (gray obstacles).**")
        if st.button("START PATROL – FLAP THROUGH I-5!", type="primary", use_container_width=True):
            st.session_state.game_running = True
            st.session_state.score = 0
            st.session_state.car_y = 200
            st.session_state.obstacles = []
            st.session_state.last_update = time.time()
            st.session_state.message = random.choice([
                "DON'T HIT ANYTHING, YOU LAZY TROOPER!",
                "AVOID DEBRIS OR I'LL HAVE YOUR BADGE!",
                "FLY STRAIGHT – NO EXCUSES!"
            ])
            st.rerun()
    else:
        now = time.time()
        dt = now - st.session_state.last_update

        if dt > 0.05:  # ~20 fps
            # Gravity
            st.session_state.car_y += 8  # fall speed

            # Jump if clicked (Streamlit button below)
            # (We use a hidden button for space/click)

            # Spawn obstacles
            if random.random() < 0.02:
                obs_y = random.randint(0, 400)
                obs_type = random.choice(["debris", "car"])
                st.session_state.obstacles.append({"x": 400, "y": obs_y, "type": obs_type})

            # Move obstacles left
            for obs in st.session_state.obstacles[:]:
                obs["x"] -= 5
                if obs["x"] < -50:
                    st.session_state.obstacles.remove(obs)
                    st.session_state.score += 1

            # Collision check
            car_rect = {"left": 50, "right": 100, "top": st.session_state.car_y, "bottom": st.session_state.car_y + 30}
            hit = False
            for obs in st.session_state.obstacles:
                obs_rect = {"left": obs["x"], "right": obs["x"] + 50, "top": obs["y"], "bottom": obs["y"] + 50}
                if (car_rect["right"] > obs_rect["left"] and car_rect["left"] < obs_rect["right"] and
                    car_rect["bottom"] > obs_rect["top"] and car_rect["top"] < obs_rect["bottom"]):
                    hit = True
                    break

            if hit or st.session_state.car_y > 550 or st.session_state.car_y < 0:
                st.session_state.game_running = False
                st.session_state.message = "CRASHED! Betts says: 'YOU'RE FIRED, IDIOT!'"
                st.error("**CRASH!** Debris or car hit – game over.")
                st.rerun()

            st.session_state.last_update = now
            st.rerun()

        # Render highway scene
        st.markdown(f"""
        <div style="position: relative; height: 500px; overflow: hidden;">
            <div style="position: absolute; left: 50px; top: {st.session_state.car_y}px; font-size: 50px;">🚔</div>
            {"".join([f'<div style="position: absolute; left: {obs["x"]}px; top: {obs["y"]}px; font-size: 40px;">{"🪨" if obs["type"] == "debris" else "🚗"}</div>' for obs in st.session_state.obstacles])}
        </div>
        """, unsafe_allow_html=True)

        # Jump button (click anywhere or use space via browser)
        if st.button("JUMP / FLAP UP (or press SPACE)", type="primary", key="jump", use_container_width=True):
            st.session_state.car_y -= 60  # jump strength
            st.rerun()

        st.metric("SCORE", st.session_state.score)

    st.markdown('</div>', unsafe_allow_html=True)

# Restart
if not st.session_state.game_running and st.session_state.score > 0:
    if st.button("PLAY AGAIN – DON'T CRASH THIS TIME"):
        st.session_state.game_running = True
        st.session_state.score = 0
        st.session_state.car_y = 200
        st.session_state.obstacles = []
        st.rerun()

st.caption("Click the JUMP button (or press SPACE) to flap up. Patrol car auto-drives right. Avoid debris/cars. Betts yells if you crash!")
