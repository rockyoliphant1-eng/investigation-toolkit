import streamlit as st
import random
import time

st.set_page_config(page_title="I-5 Trooper Dash", layout="wide")

# Custom CSS for angry Betts box
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

    .game-box {
        background: linear-gradient(to bottom, #228B22, #556B2F);
        border: 5px dashed #FF8C00;
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Session state
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'time_left' not in st.session_state:
    st.session_state.time_left = 60
if 'game_running' not in st.session_state:
    st.session_state.game_running = False
if 'message' not in st.session_state:
    st.session_state.message = random.choice([
        "CLICK FASTER YOU LAZY PIECE OF SHIT!",
        "YOU'RE LETTING THEM GET AWAY – PATHETIC!",
        "MY GRANDMA WRITES MORE TICKETS THAN YOU!",
        "QUOTA TIME – MOVE YOUR SORRY ASS!"
    ])
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()
if 'warning_timer' not in st.session_state:
    st.session_state.warning_timer = 0  # for temp popup

# Angry Betts image
BETTS_IMG = "https://thumbs.dreamstime.com/b/angry-army-bootcamp-drill-sergeant-soldier-shouting-cartoon-209860607.jpg"

st.title("🚔 I-5 Trooper Dash – Catch Speeders!")

st.image(BETTS_IMG, width=280, caption="Lt. Scott Betts – FURIOUS!", output_format="auto", use_column_width=False, clamp=False, channels="RGB", class_="betts-face")

st.markdown(f'<div class="betts-yell">{st.session_state.message}</div>', unsafe_allow_html=True)

# HUD
col1, col2 = st.columns(2)
col1.metric("SCORE", st.session_state.score)
col2.metric("TIME LEFT", f"{int(st.session_state.time_left)}s")

# Temp warning popup logic
if st.session_state.warning_timer > time.time():
    st.warning("**YOU VIOLATED AN INNOCENT CITIZEN'S RIGHTS!** Lt. Betts: 'Keep that up and you're FIRED, you idiot! Back off the non-speeders!'")
    st.rerun()

game_area = st.container()
with game_area:
    st.markdown('<div class="game-box">', unsafe_allow_html=True)
    st.markdown("**CLICK THE SPEEDING CARS (🚗💨) – AVOID INNOCENTS (🚐 or 🚍)!**")

    if not st.session_state.game_running:
        if st.button("START PATROL – 60 SECONDS OF CHAOS!", type="primary", use_container_width=True):
            st.session_state.game_running = True
            st.session_state.score = 0
            st.session_state.time_left = 60
            st.session_state.last_update = time.time()
            st.session_state.message = random.choice([
                "CLICK FASTER YOU LAZY PIECE OF SHIT!",
                "YOU'RE LETTING THEM GET AWAY – PATHETIC!",
                "MY GRANDMA WRITES MORE TICKETS THAN YOU!",
                "QUOTA TIME – MOVE YOUR SORRY ASS!"
            ])
            st.rerun()
    else:
        now = time.time()
        if now - st.session_state.last_update >= 1.0:
            st.session_state.time_left -= 1
            st.session_state.last_update = now

            if random.random() < 0.2:
                st.session_state.message = random.choice([
                    "CLICK FASTER YOU LAZY PIECE OF SHIT!",
                    "YOU'RE LETTING THEM GET AWAY – PATHETIC!",
                    "MY GRANDMA WRITES MORE TICKETS THAN YOU!",
                    "QUOTA TIME – MOVE YOUR SORRY ASS!",
                    "I'LL SHOVE YOUR BADGE WHERE THE SUN DON'T SHINE!"
                ])

            if st.session_state.time_left <= 0:
                st.session_state.game_running = False
                st.success(f"**ROUND OVER! Final Score: {st.session_state.score}**")
                st.balloons()
                st.rerun()

            st.rerun()

        # Interactive buttons – mix of speeders and innocents
        cols = st.columns(4)
        for i in range(8):
            col = cols[i % 4]
            with col:
                # 60% speeder, 40% innocent
                is_speeder = random.random() < 0.6
                emoji = "🚗💨" if is_speeder else random.choice(["🚐", "🚍"])
                btn_label = emoji

                if st.button(btn_label, key=f"car_{i}_{time.time()}", help="Click to stop (hope it's a speeder!)"):
                    if is_speeder:
                        st.session_state.score += 1
                        st.success(random.choice(["GOT 'EM!", "PULLED OVER!", "TICKET WRITTEN!", "NICE STOP!"]))
                        if st.session_state.score % 5 == 0:
                            st.balloons()
                    else:
                        # Temp popup for 5 seconds
                        st.session_state.warning_timer = time.time() + 5
                        st.session_state.message = random.choice([
                            "YOU JUST VIOLATED AN INNOCENT FAMILY'S RIGHTS, YOU IDIOT!",
                            "THAT WAS A SCHOOL BUS – YOU'RE GETTING FIRED IF YOU KEEP THIS UP!",
                            "INNOCENT CITIZEN STOPPED? RIGHTS VIOLATED – BETTS IS PISSED!",
                            "WRONG CAR! BACK OFF OR LOSE YOUR BADGE!"
                        ])
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# Restart
if not st.session_state.game_running and st.session_state.score > 0:
    if st.button("PLAY AGAIN"):
        st.session_state.game_running = True
        st.session_state.time_left = 60
        st.session_state.score = 0
        st.rerun()
