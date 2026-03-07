import streamlit as st
import random
import time

# Session state init (same as before)
if "score" not in st.session_state:
    st.session_state.score = 0
if "time_left" not in st.session_state:
    st.session_state.time_left = 60
if "game_running" not in st.session_state:
    st.session_state.game_running = False
if "cars" not in st.session_state:
    st.session_state.cars = []  # list of dicts: {'id': int, 'x': float, 'y': float}
if "next_car_time" not in st.session_state:
    st.session_state.next_car_time = time.time()
if "message" not in st.session_state:
    st.session_state.message = "Get ready, Trooper!"

# Lieutenant Betts image (angry yelling with campaign hat – cartoon style for fun)
BETTS_IMG = "https://thumbs.dreamstime.com/z/angry-army-bootcamp-drill-sergeant-soldier-pointing-viewer-shouting-cartoon-angry-army-bootcamp-drill-sergeant-245204815.jpg"

# FUNNIER YELLS – over-the-top, absurd, roast-heavy for maximum laughs
betts_yells = [
    "TROOPER! CLICK THAT SPEEDER OR I'LL MAKE YOU WRITE TICKETS WITH YOUR TEETH!",
    "YOU'RE SLOWER THAN A TURTLE ON VALIUM – MY GRANDMA JUST PASSED YOU IN HER SCOOTER!",
    "I'VE SEEN MORE ACTION FROM A PARKED DONUT – CLICK FASTER BEFORE I RECYCLE YOU TO PARKING ENFORCEMENT!",
    "THAT CAR'S DOING 90? YOU'RE DOING 0! PULL IT OVER OR I'LL PULL YOUR BADGE!",
    "QUOTA'S AT ZERO AND YOU'RE AT ZERO BRAIN CELLS – MOVE IT, MAGGOT!",
    "YOUR PARENTS SENT ME A THANK-YOU NOTE FOR TAKING YOU OFF THEIR HANDS – DON'T MAKE ME SEND ONE BACK!",
    "I'M GONNA TAKE YOUR BADGE, SHOVE IT IN A BOX, AND MAIL IT TO YOUR MOM WITH A NOTE: 'HE TRIED.'",
    "YOU CALL THAT PATROLLING? I CALL IT NAP TIME! CLICK OR I'LL SMOKE YOU LIKE A BAD CIGAR!",
    "IF YOU MISS ONE MORE, I'LL MAKE YOU CLEAN THE INTERCEPTOR WITH YOUR TONGUE – AND IT'S GOT BUG GUTS!",
    "YOU'RE LETTING THEM GET AWAY? I'D RATHER HAVE A HAMSTER ON THE FORCE – AT LEAST IT'D RUN!",
    "THIS IS I-5, NOT A TEA PARTY! ENFORCE THE SPEED LIMIT OR I'LL ENFORCE MY BOOT ON YOUR BUTT!",
    "YOUR REFLEXES ARE SO SLOW, A SLOTH JUST LAPSED YOU – CLICK NOW OR FOREVER HOLD YOUR PEACE (AND TICKETS)!"
]

st.set_page_config(page_title="I-5 Speed Catcher", layout="wide")

# Header with Betts yelling
col_img, col_title = st.columns([1, 4])
with col_img:
    st.image(BETTS_IMG, width=180, caption="Lt. Scott Betts – Losing His Mind Over You!")
with col_title:
    st.title("🚔 I-5 SPEEDING CAR CATCHER!")
    st.subheader("Click the speeding cars before Lt. Betts has a full meltdown!")

# Game HUD (same as before)
hud_col1, hud_col2, hud_col3 = st.columns(3)
with hud_col1:
    st.metric("SCORE", st.session_state.score, delta_color="normal")
with hud_col2:
    st.metric("TIME LEFT", f"{int(st.session_state.time_left)}s")
with hud_col3:
    if st.session_state.score > 0:
        st.metric("CARS/SEC", f"{st.session_state.score / (60 - st.session_state.time_left):.1f}")

# Yelling radio – now even funnier!
st.info(f"**Lt. Betts SCREAMING at you:** {st.session_state.message}")

# Game area – clickable container for cars (same logic)
game_container = st.container()
with game_container:
    if st.session_state.game_running:
        # Timer logic (unchanged)
        current_time = time.time()
        if current_time - st.session_state.start_time >= 1:
            st.session_state.time_left -= 1
            st.session_state.start_time = current_time
            if st.session_state.time_left <= 0:
                st.session_state.game_running = False
                st.balloons()
                st.success(f"**ROUND OVER! Final Score: {st.session_state.score}** – Lt. Betts says: 'Not terrible... for a civilian.'")
                if st.button("Play Again – Prove Betts Wrong!"):
                    st.session_state.score = 0
                    st.session_state.time_left = 60
                    st.session_state.cars = []
                    st.session_state.game_running = True
                    st.session_state.start_time = time.time()
                    st.session_state.next_car_time = time.time() + 1.5
                    st.rerun()

        # Spawn cars (unchanged – gets faster with score)
        spawn_rate = max(0.4, 2.0 - (st.session_state.score / 20))
        if current_time > st.session_state.next_car_time:
            car_id = len(st.session_state.cars)
            x = random.uniform(10, 90)
            y = random.uniform(10, 80)
            st.session_state.cars.append({"id": car_id, "x": x, "y": y})
            st.session_state.next_car_time = current_time + random.uniform(spawn_rate - 0.3, spawn_rate + 0.5)

        # Clickable cars
        for car in st.session_state.cars[:]:
            car_emoji = random.choice(["🚗💨", "🏎️💨", "🚙💨", "🛻💨"])
            if st.button(
                car_emoji,
                key=f"car_{car['id']}",
                help="CLICK TO PULL OVER – SAVE YOUR BADGE!",
                use_container_width=False,
                type="primary"
            ):
                st.session_state.score += 1
                st.session_state.cars.remove(car)
                st.session_state.message = random.choice(betts_yells[:4])  # Quick angry praise
                if st.session_state.score % 5 == 0:
                    st.balloons()
                    st.session_state.message = random.choice(betts_yells[4:])  # Extra roast on multiples
                st.rerun()

        # Visual highway zone
        st.markdown(
            "<div style='height: 400px; background: linear-gradient(to bottom, #4CAF50, #8BC34A); border: 4px dashed #FF9800; border-radius: 15px; display: flex; align-items: center; justify-content: center; color: white; font-size: 24px; font-weight: bold;'>"
            "I-5 CHAOS ZONE – SPEEDERS EVERYWHERE – CLICK 'EM BEFORE BETTS EXPLODES!</div>",
            unsafe_allow_html=True
        )

    else:
        # Start screen
        st.markdown("<h2 style='text-align: center; color: #FF5722;'>READY TO FACE LT. BETTS' WRATH?</h2>", unsafe_allow_html=True)
        if st.button("START PATROL – SURVIVE 60 SECONDS OF YELLING!", type="primary", use_container_width=True):
            st.session_state.game_running = True
            st.session_state.start_time = time.time()
            st.session_state.next_car_time = time.time() + 1.5
            st.session_state.message = random.choice(betts_yells)
            st.rerun()

# Random yell updates for extra pressure & laughs
if st.session_state.game_running and random.random() < 0.1 + (st.session_state.score / 150):
    st.session_state.message = random.choice(betts_yells)
    st.rerun()

st.markdown("---")
st.caption("Lt. Betts is angrier (and funnier) than ever! Click those speeders fast – or he'll roast you into next week. Pure chaos fun on Streamlit. 🚔😂")
