import streamlit as st
import random
import time

# Wide layout + custom CSS for game feel
st.set_page_config(page_title="I-5 Trooper Dash – Lt. Betts Fury", layout="wide")

# Custom CSS for angry yelling box & game style
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bangers&display=swap');

    .betts-yell {
        background: linear-gradient(135deg, #ff0000, #cc0000);
        color: #ffff00 !important;
        font-family: 'Bangers', cursive !important;
        font-size: 48px !important;
        text-align: center !important;
        padding: 40px 20px !important;
        border: 8px solid #000 !important;
        border-radius: 20px !important;
        box-shadow: 0 0 30px #ff4500 !important;
        margin: 20px 0 !important;
        text-shadow: 4px 4px 8px #000 !important;
        letter-spacing: 2px !important;
    }

    .betts-face {
        display: block !important;
        margin: 0 auto 20px !important;
        border: 6px solid #ffd700 !important;
        border-radius: 50% !important;
        box-shadow: 0 0 25px #ff4500 !important;
    }

    .game-area {
        background: linear-gradient(to bottom, #228B22 40%, #556B2F 100%);
        border: 6px dashed #FF8C00;
        border-radius: 25px;
        padding: 30px;
        margin: 20px 0;
    }

    .score-flash {
        font-size: 60px !important;
        color: #00ff00 !important;
        animation: flash 1s infinite;
    }

    @keyframes flash {
        0% { opacity: 1; }
        50% { opacity: 0.4; }
        100% { opacity: 1; }
    }
    </style>
""", unsafe_allow_html=True)

# Session state
if "score" not in st.session_state:
    st.session_state.score = 0
if "time_left" not in st.session_state:
    st.session_state.time_left = 60
if "game_running" not in st.session_state:
    st.session_state.game_running = False
if "message" not in st.session_state:
    st.session_state.message = "GET THOSE SPEEDERS, TROOPER!"
if "last_update" not in st.session_state:
    st.session_state.last_update = time.time()

# Angry Betts image (furious yelling cartoon with campaign hat)
BETTS_IMG = "https://thumbs.dreamstime.com/b/angry-army-bootcamp-drill-sergeant-soldier-shouting-cartoon-209860607.jpg"

# Funny/offensive yells
yells = [
    "CLICK FASTER YOU LAZY PIECE OF SHIT!",
    "YOU'RE LETTING THEM GET AWAY – PATHETIC LOSER!",
    "MY GRANDMA WRITES MORE TICKETS THAN YOU!",
    "QUOTA TIME – MOVE YOUR SORRY ASS!",
    "THIS IS I-5, NOT NAP TIME!",
    "YOU CALL THAT PATROLLING? DISGRACE!",
    "I'LL SHOVE YOUR BADGE WHERE THE SUN DON'T SHINE!",
    "KEEP MISSING AND YOU'RE WALKING A BEAT IN A PARK!",
    "SPEEDERS LAUGHING AT YOU – CLICK NOW!",
    "YOU'RE SLOWER THAN A DEAD SLUG!"
]

st.title("🚔 I-5 TROOPER DASH – CATCH THE SPEEDERS!")

st.image(BETTS_IMG, width=300, caption="Lt. Scott Betts – LOSING HIS MIND!", output_format="auto", use_column_width=False, clamp=False, channels="RGB", class_="betts-face")

st.markdown(f'<div class="betts-yell">{st.session_state.message}</div>', unsafe_allow_html=True)

# HUD
cols = st.columns(3)
cols[0].metric("SCORE", st.session_state.score)
cols[1].metric("TIME LEFT", f"{int(st.session_state.time_left)}s", delta_color="inverse" if st.session_state.time_left < 10 else "normal")
cols[2].metric("HIGH SCORE", st.session_state.get("high_score", 0))

if st.session_state.time_left < 10:
    st.warning("**TIME CRITICAL – BETTS IS ABOUT TO EXPLODE!**")

game_area = st.container()
with game_area:
    st.markdown('<div class="game-area">', unsafe_allow_html=True)
    st.markdown("**CLICK THE SPEEDING CARS (🚗💨) FAST!** Each click = potential stop. Rack up points before time runs out!")

    if not st.session_state.game_running:
        if st.button("START PATROL – SURVIVE BETTS' WRATH!", type="primary", use_container_width=True):
            st.session_state.game_running = True
            st.session_state.score = 0
            st.session_state.time_left = 60
            st.session_state.last_update = time.time()
            st.session_state.message = random.choice(yells)
            st.rerun()
    else:
        now = time.time()
        if now - st.session_state.last_update >= 1:
            st.session_state.time_left -= 1
            st.session_state.last_update = now

            # Random yell pressure
            if random.random() < 0.25:
                st.session_state.message = random.choice(yells)

            if st.session_state.time_left <= 0:
                st.session_state.game_running = False
                if st.session_state.score > st.session_state.get("high_score", 0):
                    st.session_state.high_score = st.session_state.score
                    st.success(f"**NEW HIGH SCORE: {st.session_state.score}!** Betts is... slightly less disgusted.")
                else:
                    st.warning(f"**ROUND OVER – Score: {st.session_state.score}** Betts says: 'Pathetic. Try harder next time.'")
                st.balloons()
                st.rerun()

            st.rerun()

        # Interactive game buttons – like whack-a-mole style
        cols = st.columns(4)
        for i in range(12):  # 12 clickable "targets"
            with cols[i % 4]:
                if st.button("🚗💨", key=f"click_{i}", help="CLICK TO STOP THE SPEEDER!", use_container_width=True, type="primary"):
                    st.session_state.score += random.randint(1, 3)  # Variable points for excitement
                    feedback = random.choice([
                        "BAM! GOT 'EM!",
                        "PULLED OVER – NICE!",
                        "LIGHTS & SIRENS!",
                        "TICKET WRITTEN!"
                    ])
                    st.success(feedback)
                    if st.session_state.score % 10 == 0:
                        st.balloons()
                        st.markdown('<p class="score-flash">LEVEL UP!</p>', unsafe_allow_html=True)
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# Play again
if not st.session_state.game_running and st.session_state.score > 0:
    if st.button("PLAY AGAIN – MAKE BETTS PROUD THIS TIME"):
        st.session_state.game_running = True
        st.session_state.time_left = 60
        st.session_state.score = 0
        st.session_state.message = random.choice(yells)
        st.rerun()

st.markdown("---")
st.caption("Quick arcade-style game: Click the speeding cars as fast as possible! Bigger, angrier Betts yelling, stable layout, video game vibes. High score? Share it with @RockyOliphant!")
