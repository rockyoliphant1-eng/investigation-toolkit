import streamlit as st
import random
import time

st.set_page_config(page_title="I-5 Speeder Hunt - Lt. Betts Rage Mode", layout="wide")

# Session state
keys_defaults = {
    'score': 0,
    'wrong_stops': 0,
    'time_left': 60,
    'game_running': False,
    'spots': {},          # id: is_speeder (bool)
    'next_id': 0,
    'last_update': time.time(),
    'message': "Hunt those speeders, you worthless maggot!"
}
for k, v in keys_defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Lt. Betts angry yelling image (campaign hat, red face, pointing/furious)
BETTS_IMG = "https://media.istockphoto.com/id/2233166435/vector/drill-instructor-sergeant-bootcamp-army-soldier.jpg?s=612x612&w=0&k=20&c=9mnbGiXMJL6l3wDdLGHyiPZAQ1BgEdJfkTXq3VAxAFo="

# General yells (pressure)
general_yells = [
    "CLICK FASTER YOU LAZY PIECE OF SHIT!",
    "YOU'RE LETTING SPEEDERS RUN WILD – PATHETIC!",
    "MY GRANDMA WOULD HAVE MORE STOPS BY NOW!",
    "QUOTA OR BUST – MOVE YOUR SORRY ASS!",
    "THIS AIN'T A TEA PARTY – ENFORCE!",
    "YOU CALL THAT PATROLLING? DISGRACEFUL!"
]

# Right pick praise (still mean)
praise_yells = [
    "FINALLY! ONE LESS ASSHOLE ON THE ROAD!",
    "NOT COMPLETELY USELESS... YET!",
    "KEEP GOING OR I'LL STILL FIRE YOU!",
    "GOOD HIT – NOW DO IT 20 MORE TIMES, IDIOT!"
]

# Wrong pick – SUPER OFFENSIVE, obvious rage
wrong_yells = [
    "YOU JUST PULLED OVER A FUCKING SCHOOL BUS FULL OF KIDS, YOU MORON!",
    "THAT WAS A MOM WITH THREE TODDLERS – YOU'RE A DISGRACE!",
    "AMBULANCE WITH SIRENS? YOU ALMOST KILLED SOMEONE, DUMBASS!",
    "ICE CREAM TRUCK? KIDS ARE CRYING BECAUSE OF YOUR STUPID ASS!",
    "CHURCH VAN? GO BURN IN HELL FOR THAT ONE!",
    "WEDDING LIMO? YOU RUINED THEIR BIG DAY, YOU WORTHLESS PRICK!",
    "GRANDMA'S OLD SEDAN? SHE'S 92 AND YOU SCARED HER TO DEATH!",
    "DELIVERY VAN? YOU JUST DELAYED SOMEONE'S DINNER, ASSHOLE!"
]

# Max spots on screen
MAX_SPOTS = 20

st.title("🚔 I-5 SPEEDER HUNT – LT. BETTS IS WATCHING!")
st.subheader("Click boxes to check vehicles. Speeders = points. Innocents = Betts loses his shit & you lose time!")

# HUD
cols = st.columns(4)
cols[0].metric("STOPS", st.session_state.score)
cols[1].metric("WRONGS", st.session_state.wrong_stops)
cols[2].metric("TIME LEFT", f"{max(0, int(st.session_state.time_left))}s")
avg = st.session_state.score / max(1, 60 - st.session_state.time_left)
cols[3].metric("RATE", f"{avg:.1f}/s")

# Yelling display – red & bold
st.error(f"**Lt. Betts SCREAMING:** {st.session_state.message}")

# Betts image
st.image(BETTS_IMG, width=220, caption="Lt. Scott Betts – Ready to Destroy You")

if not st.session_state.game_running:
    if st.button("🚨 START PATROL – SURVIVE THE RAGE! 🚨", type="primary", use_container_width=True):
        st.session_state.game_running = True
        st.session_state.score = 0
        st.session_state.wrong_stops = 0
        st.session_state.time_left = 60
        st.session_state.spots = {}
        st.session_state.next_id = 0
        st.session_state.last_update = time.time()
        st.session_state.message = random.choice(general_yells)
        # Seed initial board with lots of options
        for _ in range(12):
            spot_id = st.session_state.next_id
            st.session_state.spots[spot_id] = random.random() < 0.6  # ~60% speeders
            st.session_state.next_id += 1
        st.rerun()
else:
    current_time = time.time()
    delta = current_time - st.session_state.last_update

    if delta >= 1.0:
        st.session_state.time_left = max(0, st.session_state.time_left - 1)
        st.session_state.last_update = current_time

        # Spawn new spots constantly (more options!)
        add_count = random.randint(2, 4) if len(st.session_state.spots) < MAX_SPOTS else 0
        for _ in range(add_count):
            if len(st.session_state.spots) >= MAX_SPOTS:
                break
            spot_id = st.session_state.next_id
            st.session_state.spots[spot_id] = random.random() < 0.6
            st.session_state.next_id += 1

        # Random pressure yell
        if random.random() < 0.18:
            st.session_state.message = random.choice(general_yells)

        if st.session_state.time_left <= 0:
            st.session_state.game_running = False
            end_msg = "YOU SURVIVED... BARELY!" if st.session_state.score >= 30 else "WHAT A JOKE! CLEAN OUT YOUR LOCKER!"
            st.session_state.message = end_msg
            st.balloons() if st.session_state.score >= 30 else None
            st.rerun()

        st.rerun()

    # Render lots of clickable spots (grid-like but dynamic columns)
    st.markdown("### **CLICK ANY BOX – ONE CLICK ONLY!**")
    spot_ids = list(st.session_state.spots.keys())
    random.shuffle(spot_ids)  # Shuffle for variety each time

    cols_per_row = 5
    for i in range(0, len(spot_ids), cols_per_row):
        row_ids = spot_ids[i:i + cols_per_row]
        row_cols = st.columns(cols_per_row)
        for j, spot_id in enumerate(row_ids):
            with row_cols[j]:
                if st.button("VEHICLE ?\n**PULL OVER?**", key=f"spot_{spot_id}", help="One click – choose wisely!"):
                    is_speeder = st.session_state.spots.pop(spot_id, False)
                    if is_speeder:
                        st.session_state.score += 1
                        st.session_state.message = random.choice(praise_yells)
                        st.success("✅ SPEEDER CAUGHT! +1 POINT\n🚔 Lights & sirens! Great pull!")
                        st.balloons() if st.session_state.score % 5 == 0 else None
                        # Bonus spawn on hit
                        if len(st.session_state.spots) < MAX_SPOTS:
                            new_id = st.session_state.next_id
                            st.session_state.spots[new_id] = random.random() < 0.6
                            st.session_state.next_id += 1
                    else:
                        st.session_state.wrong_stops += 1
                        st.session_state.time_left = max(0, st.session_state.time_left - 4)
                        st.session_state.message = random.choice(wrong_yells)
                        st.error("❌ WRONG! NON-SPEEDER!\n-4 SECONDS – YOU IDIOT!\n(That was innocent traffic!)")
                    st.rerun()

    if not spot_ids:
        st.info("Board empty... more vehicles incoming!")

# Play again / footer
if not st.session_state.game_running and st.session_state.score > 0:
    if st.button("PLAY AGAIN – DON'T MAKE BETTS MAD THIS TIME"):
        st.session_state.game_running = True
        st.session_state.time_left = 60
        st.session_state.score = 0
        st.session_state.wrong_stops = 0
        st.session_state.spots = {}
        st.session_state.next_id = 0
        st.rerun()

st.markdown("---")
st.caption("Single-click hunt: Lots of vehicles, obvious feedback, constant action. Click fast or Lt. Betts will roast you alive! Reboot if frozen. Pure chaos fun.")
