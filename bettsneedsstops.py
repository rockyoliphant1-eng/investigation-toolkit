import streamlit as st
import random
import time

# Config for wide layout
st.set_page_config(page_title="I-5 Speeder Hunter - Lt. Betts Edition", layout="wide")

# Session state initialization
for key in ['score', 'wrong_stops', 'time_left', 'game_running', 'spots', 'next_id', 'last_update', 'message']:
    if key not in st.session_state:
        st.session_state[key] = 0 if key in ['score', 'wrong_stops', 'next_id', 'time_left'] else False if key == 'game_running' else {} if key == 'spots' else time.time() if key == 'last_update' else "Get ready to hunt speeders, maggot!"

# Lt. Betts angry image (perfect cartoon yelling state trooper with campaign hat)
BETTS_IMG = "https://media.istockphoto.com/id/1385108467/vector/angry-army-bootcamp-drill-sergeant-cartoon.jpg?s=612x612&w=0&k=20&c=3fGMt7aLzLa0uRGSZREujosQhE77PNWVKPpH6849GFo="

# MAX spots on board
MAX_SPOTS = 12
SPEEDER_PROB = 0.6

# Offensive general yells
general_yells = [
    "CLICK THAT FUCKING SPEEDER YOU WORTHLESS PIECE OF SHIT!",
    "YOU'RE SLOWER THAN A ONE-LEGGED DOG – MOVE YOUR ASS!",
    "I'VE WIPED SMARTER STAINS OFF MY BOOTS THAN YOU!",
    "PULL IT OVER BEFORE I SHOVE YOUR BADGE UP YOUR ASS!",
    "QUOTA'S EMPTY AND YOUR BRAIN'S EMPTIER, LOSER!",
    "YOUR MOM CALLED – SHE WANTS HER BASEMENT DWELLER BACK!",
    "THIS IS PATROLLING? MORE LIKE JERKING OFF WITH A BADGE!",
    "LICK THE HIGHWAY CLEAN IF YOU MISS AGAIN, MAGGOT!"
]

# SUPER OFFENSIVE WRONG CLICK YELLS (can't stop non-speeders)
wrong_yells = [
    "YOU CAN'T STOP NON-SPEEDERS, YOU FUCKING MORON! THAT WAS A MOM WITH KIDS!",
    "LAW-ABIDING SCHOOL BUS? YOU DUMB SHIT, LET THEM GO!",
    "CHURCH VAN FULL OF NUNS? BACK OFF YOU STUPID BASTARD!",
    "FAMILY MINIVAN? YOU JUST PISSED OFF DAD – IDIOT!",
    "AMBULANCE? YOU ALMOST KILLED SOMEONE, YOU RETARDED FUCK!",
    "ICE CREAM TRUCK? KIDS ARE CRYING BECAUSE OF YOU, ASSHOLE!",
    "PRIEST IN A SEDAN? GO TO HELL FOR THAT ONE, SINNER!",
    "WEDDING LIMO? YOU RUINED THEIR DAY, YOU WORTHLESS PRICK!"
]

# Praise for correct (still offensive)
praise_yells = [
    "FINALLY, YOU GOT ONE – YOU LUCKY SHIT!",
    "NOT BAD... FOR A BRAINDEAD MONKEY!",
    "KEEP IT UP OR I'LL STILL FIRE YOUR ASS!",
    "ONE LESS SPEEDER – NOW DO TEN MORE, LOSER!"
]

st.title("🚔 I-5 SPEEDER HUNTER")
st.subheader("Click 🚗? boxes to check for speeders! Wrong ones = Lt. Betts RAGES & time penalty!")

# HUD
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("STOPS", st.session_state.score)
with col2:
    st.metric("WRONGS", st.session_state.wrong_stops)
with col3:
    st.metric("TIME", f"{int(st.session_state.time_left)}s")
with col4:
    avg = st.session_state.score / max(1, 60 - st.session_state.time_left)
    st.metric("RATE", f"{avg:.1f}/s")

# Betts yelling (red error style)
st.error(f"**Lt. Betts ROARING:** {st.session_state.message}")

# Betts image
col_betts, _ = st.columns([1, 4])
with col_betts:
    st.image(BETTS_IMG, width=220, caption="Lt. Scott Betts - FURIOUS!")

# Game logic
if not st.session_state.game_running:
    if st.button("🚨 START PATROL - HUNT SPEEDERS ON I-5! 🚨", type="primary", use_container_width=True):
        st.session_state.game_running = True
        st.session_state.score = 0
        st.session_state.wrong_stops = 0
        st.session_state.time_left = 60
        st.session_state.spots = {}
        st.session_state.next_id = 0
        st.session_state.last_update = time.time()
        st.session_state.message = random.choice(general_yells)
        # Initial board populate
        for _ in range(10):
            spot_id = st.session_state.next_id
            st.session_state.spots[spot_id] = random.random() < SPEEDER_PROB
            st.session_state.next_id += 1
        st.rerun()
else:
    # Timer and spawn
    current_time = time.time()
    if current_time - st.session_state.last_update >= 1.0:
        st.session_state.time_left = max(0, st.session_state.time_left - 1)
        st.session_state.last_update = current_time
        # Spawn new spots to fill board
        spots_to_add = min(2, MAX_SPOTS - len(st.session_state.spots))
        for _ in range(spots_to_add):
            spot_id = st.session_state.next_id
            st.session_state.spots[spot_id] = random.random() < SPEEDER_PROB
            st.session_state.next_id += 1
        # Random yell pressure
        if random.random() < 0.15:
            st.session_state.message = random.choice(general_yells)
        if st.session_state.time_left <= 0:
            st.session_state.game_running = False
            if st.session_state.score > 25:
                st.session_state.message = "NOT BAD, TROOPER... YOU'RE NOT TOTALLY USELESS!"
            else:
                st.session_state.message = "PATHETIC! MY DOG WRITES BETTER TICKETS!"
            st.balloons()
            st.rerun()
        st.rerun()

    # Render interactive board - scattered grid
    st.markdown("### **Hunt the Speeders Below!**")
    spot_ids = list(st.session_state.spots.keys())
    random.shuffle(spot_ids)  # Random positions each render
    num_rows = (len(spot_ids) + 3) // 4
    for row_start in range(0, len(spot_ids), 4):
        row_ids = spot_ids[row_start:row_start + 4]
        cols = st.columns(4)
        for col_idx, spot_id in enumerate(row_ids):
            with cols[col_idx]:
                if st.button("🚗 ?\n**Check Speed!**", key=f"spot_{spot_id}", help="Pull over if speeding?", type="secondary"):
                    is_speeder = st.session_state.spots.pop(spot_id)
                    if is_speeder:
                        st.session_state.score += 1
                        st.session_state.message = random.choice(praise_yells)
                        # Bonus spawn on success
                        if len(st.session_state.spots) < MAX_SPOTS:
                            new_id = st.session_state.next_id
                            st.session_state.spots[new_id] = random.random() < SPEEDER_PROB
                            st.session_state.next_id += 1
                        st.success("🚨 SPEEDER PULLED OVER! +1")
                    else:
                        st.session_state.wrong_stops += 1
                        st.session_state.time_left = max(0, st.session_state.time_left - 4)
                        st.session_state.message = random.choice(wrong_yells)
                        st.error("❌ NON-SPEEDER! -4s")
                    st.rerun()

    # Empty spots visual
    if len(spot_ids) == 0:
        st.warning("Board clear! More coming...")

# Footer
st.markdown("---")
st.caption("Click wisely or Lt. Betts will destroy you! Reboot app if stuck (hamburger menu). Pure I-5 chaos in your browser. 🚔💨")
