import streamlit as st
import random
import time

# Session state init
if "score" not in st.session_state:
    st.session_state.score = 0
if "time_left" not in st.session_state:
    st.session_state.time_left = 60
if "game_running" not in st.session_state:
    st.session_state.game_running = False
if "cars" not in st.session_state:
    st.session_state.cars = []  
if "next_car_time" not in st.session_state:
    st.session_state.next_car_time = time.time()
if "message" not in st.session_state:
    st.session_state.message = "Get your lazy ass ready, Trooper!"

# Betts image
BETTS_IMG = "https://thumbs.dreamstime.com/z/angry-army-bootcamp-drill-sergeant-soldier-pointing-viewer-shouting-cartoon-angry-army-bootcamp-drill-sergeant-245204815.jpg"

# SUPER OFFENSIVE, MEAN YELLS – drill sergeant style, heavy roasts
betts_yells = [
    "CLICK THAT FUCKING SPEEDER YOU WORTHLESS PIECE OF SHIT!",
    "YOU'RE SLOWER THAN A ONE-LEGGED DOG IN A RACE – MY DEAD GRANDMA MOVES FASTER!",
    "I'VE WIPED SMARTER STAINS OFF MY BOOTS THAN YOU – CLICK OR QUIT!",
    "THAT CAR'S HAULING ASS AND YOU'RE HAULING NOTHING – PULL IT OVER BEFORE I SHOVE YOUR BADGE UP YOURS!",
    "QUOTA'S EMPTY AND YOUR HEAD'S EMPTIER – GET MOVING, YOU PATHETIC LOSER!",
    "YOUR MOM MUST BE SO PROUD OF HER USELESS SPAWN – CLICK FASTER OR I'LL CALL HER TO COMPLAIN!",
    "YOU CALL THIS PATROLLING? I CALL IT MASTURBATION WITH A BADGE – DO SOMETHING USEFUL!",
    "IF YOU MISS ONE MORE, I'LL MAKE YOU LICK THE HIGHWAY CLEAN – STARTING WITH THE BUGS ON MY WINDSHIELD!",
    "YOU'RE LETTING THEM ESCAPE? I'D RATHER HAVE A RETARDED MONKEY ON DUTY – AT LEAST IT'D TRY!",
    "THIS IS I-5, NOT YOUR MOM'S BASEMENT – ENFORCE THE LAW OR I'LL ENFORCE MY FIST ON YOUR FACE!",
    "YOUR REFLEXES SUCK SO BAD A BLIND TURTLE JUST PASSED YOU – CLICK NOW, ASSHOLE!",
    "YOU'RE A DISGRACE TO THE BADGE – CLICK THOSE CARS OR I'LL MAKE YOU EAT YOUR NEXT TICKET BOOK!"
]

st.set_page_config(page_title="I-5 Speed Catcher – Betts Edition", layout="wide")

col_img, col_title = st.columns([1, 4])
with col_img:
    st.image(BETTS_IMG, width=180, caption="Lt. Scott Betts – About to Lose His Shit")
with col_title:
    st.title("🚔 I-5 SPEEDING CAR CATCHER – SURVIVE BETTS' RAGE!")
    st.subheader("Click the damn cars before he has a stroke!")

hud_col1, hud_col2, hud_col3 = st.columns(3)
with hud_col1:
    st.metric("SCORE", st.session_state.score)
with hud_col2:
    st.metric("TIME LEFT", f"{int(st.session_state.time_left)}s")
with hud_col3:
    if st.session_state.score > 0:
        st.metric("CARS/SEC", f"{st.session_state.score / max(1, 60 - st.session_state.time_left):.1f}")

st.error(f"**Lt. Betts ROARING at you:** {st.session_state.message}")  # Made it red/error for intensity

game_container = st.container()
with game_container:
    if st.session_state.game_running:
        current_time = time.time()
        if current_time - st.session_state.start_time >= 1:
            st.session_state.time_left -= 1
            st.session_state.start_time = current_time
            if st.session_state.time_left <= 0:
                st.session_state.game_running = False
                st.balloons()
                st.success(f"**ROUND OVER! Score: {st.session_state.score}** – Betts grunts: 'Not complete garbage... barely.'")
                if st.button("Play Again – Don't Piss Him Off This Time"):
                    st.session_state.score = 0
                    st.session_state.time_left = 60
                    st.session_state.cars = []
                    st.session_state.game_running = True
                    st.session_state.start_time = time.time()
                    st.session_state.next_car_time = time.time() + 1.5
                    st.rerun()

        spawn_rate = max(0.3, 2.0 - (st.session_state.score / 15))  
        if current_time > st.session_state.next_car_time:
            car_id = len(st.session_state.cars)
            x = random.uniform(5, 95)
            y = random.uniform(10, 85)
            st.session_state.cars.append({"id": car_id, "x": x, "y": y})
            st.session_state.next_car_time = current_time + random.uniform(spawn_rate - 0.4, spawn_rate + 0.6)

        for car in st.session_state.cars[:]:
            car_emoji = random.choice(["🚗💨", "🏎️💨", "🚙💨", "🛻💨"])
            if st.button(
                car_emoji,
                key=f"car_{car['id']}",
                help="CLICK THIS BASTARD – SAVE YOUR JOB!",
                type="primary"
            ):
                st.session_state.score += 1
                st.session_state.cars.remove(car)
                st.session_state.message = random.choice(betts_yells)
                if st.session_state.score % 5 == 0:
                    st.balloons()
                st.rerun()

        st.markdown(
            "<div style='height: 450px; background: linear-gradient(to bottom, #228B22, #556B2F); border: 5px solid #FF4500; border-radius: 20px; display: flex; align-items: center; justify-content: center; color: #FFD700; font-size: 28px; font-weight: bold; text-shadow: 2px 2px #000;'>"
            "I-5 MADHOUSE – SPEEDERS RUNNING WILD – CLICK THE FUCKERS!</div>",
            unsafe_allow_html=True
        )

    else:
        st.markdown("<h2 style='text-align: center; color: #FF0000;'>READY TO GET SCREAMED AT?</h2>", unsafe_allow_html=True)
        if st.button("START PATROL – 60s OF PURE HELL!", type="primary", use_container_width=True):
            st.session_state.game_running = True
            st.session_state.start_time = time.time()
            st.session_state.next_car_time = time.time() + 1.0
            st.session_state.message = random.choice(betts_yells)
            st.rerun()

# Random offensive yell pressure
if st.session_state.game_running and random.random() < 0.12 + (st.session_state.score / 120):
    st.session_state.message = random.choice(betts_yells)
    st.rerun()

st.markdown("---")
st.caption("Lt. Betts is now **brutally** offensive – click fast or get roasted! Pure chaotic fun. If still blank, reboot on Cloud or test locally. Let me know what the logs say!")
