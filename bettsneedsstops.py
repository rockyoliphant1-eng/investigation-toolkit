import streamlit as st
import random
import time

st.set_page_config(page_title="I-5 Speeder Reveal Hunt – Lt. Betts Rage", layout="wide")

# ────────────────────────────────────────────────
# Session State Setup
# ────────────────────────────────────────────────
defaults = {
    'score': 0,
    'wrong_stops': 0,
    'time_left': 60,
    'game_running': False,
    'spots': {},           # id → {'is_speeder': bool, 'revealed': bool, 'vehicle_type': str}
    'next_id': 0,
    'last_update': time.time(),
    'message': "Hunt speeders, you worthless maggot!"
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ────────────────────────────────────────────────
# Lt. Betts image – angry yelling state trooper with campaign hat
# ────────────────────────────────────────────────
BETTS_IMG = "https://media.istockphoto.com/id/2233166435/vector/drill-instructor-sergeant-bootcamp-army-soldier.jpg?s=612x612&w=0&k=20&c=9mnbGiXMJL6l3wDdLGHyiPZAQ1BgEdJfkTXq3VAxAFo="

# ────────────────────────────────────────────────
# Yells
# ────────────────────────────────────────────────
general_yells = [
    "CLICK FASTER YOU LAZY PIECE OF SHIT!",
    "YOU'RE LETTING SPEEDERS RUN WILD – PATHETIC!",
    "MY GRANDMA WOULD HAVE MORE STOPS BY NOW!",
    "QUOTA OR BUST – MOVE YOUR SORRY ASS!",
    "THIS AIN'T A TEA PARTY – ENFORCE!",
    "YOU CALL THAT PATROLLING? DISGRACEFUL!"
]

praise_yells = [
    "FINALLY! ONE LESS ASSHOLE ON THE ROAD!",
    "NOT COMPLETELY USELESS... YET!",
    "KEEP GOING OR I'LL STILL FIRE YOU!",
    "GOOD HIT – NOW DO IT 20 MORE TIMES, IDIOT!"
]

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

# ────────────────────────────────────────────────
# Vehicle types (for flavor when revealed)
# ────────────────────────────────────────────────
speeder_types = [
    "Speeding Sports Car", "Reckless Pickup", "Modified Civic", "Luxury Sedan Racing",
    "Motorcycle Doing Wheelies", "Souped-up Mustang", "Drift King Toyota"
]

innocent_types = [
    "Family Minivan", "School Bus", "Ambulance", "Ice Cream Truck", "Church Van",
    "Wedding Limo", "Grandma's Old Sedan", "Delivery Van", "Soccer Mom SUV",
    "Priest's Toyota", "Mom with Toddlers", "Carpool Van"
]

# ────────────────────────────────────────────────
# Constants
# ────────────────────────────────────────────────
MAX_SPOTS = 20
SPEEDER_PROB = 0.60
SPAWN_PER_SECOND = (2, 4)

# ────────────────────────────────────────────────
# UI Header
# ────────────────────────────────────────────────
st.title("🚔 I-5 SPEEDER REVEAL HUNT")
st.subheader("Click any box → it reveals if it's a speeder or innocent vehicle. One click only!")

# HUD
c1, c2, c3, c4 = st.columns(4)
c1.metric("STOPS", st.session_state.score)
c2.metric("WRONGS", st.session_state.wrong_stops)
c3.metric("TIME LEFT", f"{max(0, int(st.session_state.time_left))}s")
rate = st.session_state.score / max(1, 60 - st.session_state.time_left)
c4.metric("RATE", f"{rate:.1f}/s")

# Yelling
st.error(f"**Lt. Betts SCREAMING:** {st.session_state.message}")

# Betts image
st.image(BETTS_IMG, width=220, caption="Lt. Scott Betts – About to Explode")

# ────────────────────────────────────────────────
# Game Logic
# ────────────────────────────────────────────────
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

        # Seed initial vehicles
        for _ in range(12):
            spot_id = st.session_state.next_id
            is_speeder = random.random() < SPEEDER_PROB
            vehicle = random.choice(speeder_types if is_speeder else innocent_types)
            st.session_state.spots[spot_id] = {
                'is_speeder': is_speeder,
                'revealed': False,
                'vehicle_type': vehicle
            }
            st.session_state.next_id += 1
        st.rerun()
else:
    now = time.time()
    if now - st.session_state.last_update >= 1.0:
        st.session_state.time_left = max(0, st.session_state.time_left - 1)
        st.session_state.last_update = now

        # Spawn new vehicles
        if len(st.session_state.spots) < MAX_SPOTS:
            add_count = random.randint(*SPAWN_PER_SECOND)
            for _ in range(add_count):
                if len(st.session_state.spots) >= MAX_SPOTS:
                    break
                spot_id = st.session_state.next_id
                is_speeder = random.random() < SPEEDER_PROB
                vehicle = random.choice(speeder_types if is_speeder else innocent_types)
                st.session_state.spots[spot_id] = {
                    'is_speeder': is_speeder,
                    'revealed': False,
                    'vehicle_type': vehicle
                }
                st.session_state.next_id += 1

        # Random pressure
        if random.random() < 0.18:
            st.session_state.message = random.choice(general_yells)

        # Time up?
        if st.session_state.time_left <= 0:
            st.session_state.game_running = False
            msg = "YOU SURVIVED... BARELY!" if st.session_state.score >= 35 else "WHAT A JOKE! CLEAN OUT YOUR LOCKER!"
            st.session_state.message = msg
            if st.session_state.score >= 35:
                st.balloons()
            st.rerun()

        st.rerun()

    # ────────────────────────────────────────────────
    # Render clickable board
    # ────────────────────────────────────────────────
    st.markdown("### **CLICK ANY BOX – IT REVEALS THE VEHICLE**")

    spot_ids = list(st.session_state.spots.keys())
    random.shuffle(spot_ids)

    cols_per_row = 5
    for i in range(0, len(spot_ids), cols_per_row):
        row_ids = spot_ids[i:i + cols_per_row]
        row_cols = st.columns(cols_per_row)
        for j, spot_id in enumerate(row_ids):
            with row_cols[j]:
                spot = st.session_state.spots[spot_id]

                if not spot['revealed']:
                    # Hidden – clickable mystery box
                    if st.button("VEHICLE ?\n**CHECK**", key=f"check_{spot_id}", help="One click reveals"):
                        spot['revealed'] = True
                        if spot['is_speeder']:
                            st.session_state.score += 1
                            st.session_state.message = random.choice(praise_yells)
                            st.success(f"✅ SPEEDER!\n**{spot['vehicle_type']}** caught!\n+1 POINT")
                            st.balloons() if st.session_state.score % 5 == 0 else None
                            # Bonus spawn
                            if len(st.session_state.spots) < MAX_SPOTS:
                                new_id = st.session_state.next_id
                                is_new = random.random() < SPEEDER_PROB
                                veh_new = random.choice(speeder_types if is_new else innocent_types)
                                st.session_state.spots[new_id] = {
                                    'is_speeder': is_new,
                                    'revealed': False,
                                    'vehicle_type': veh_new
                                }
                                st.session_state.next_id += 1
                        else:
                            st.session_state.wrong_stops += 1
                            st.session_state.time_left = max(0, st.session_state.time_left - 4)
                            st.session_state.message = random.choice(wrong_yells)
                            st.error(f"❌ INNOCENT!\n**{spot['vehicle_type']}** – you idiot!\n-4 SECONDS")
                        st.rerun()
                else:
                    # Already revealed – show result (non-clickable)
                    if spot['is_speeder']:
                        st.success(f"✅ **{spot['vehicle_type']}** (speeder)")
                    else:
                        st.error(f"❌ **{spot['vehicle_type']}** (innocent)")

    if not spot_ids:
        st.info("Board cleared – more vehicles incoming!")

# ────────────────────────────────────────────────
# Play again / footer
# ────────────────────────────────────────────────
if not st.session_state.game_running and st.session_state.score > 0:
    if st.button("PLAY AGAIN – DON'T PISS OFF BETTS AGAIN"):
        st.session_state.game_running = True
        st.session_state.time_left = 60
        st.session_state.score = 0
        st.session_state.wrong_stops = 0
        st.session_state.spots = {}
        st.session_state.next_id = 0
        st.rerun()

st.markdown("---")
st.caption("Single-click reveal hunt: Boxes show speeder or innocent vehicle immediately. Constant spawning. High score = impress Lt. Betts (good luck). Reboot app if frozen.")
