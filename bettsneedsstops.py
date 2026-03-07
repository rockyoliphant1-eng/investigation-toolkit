import streamlit as st
import random
import time

st.set_page_config(page_title="I-5 Speeder Hunt – Lt. Betts Edition", layout="wide")

# Session state defaults
defaults = {
    'score': 0,
    'wrong_stops': 0,
    'time_left': 60,
    'game_running': False,
    'spots': {},           # id → {'is_speeder': bool, 'revealed': bool, 'vehicle_type': str, 'img_url': str}
    'next_id': 0,
    'last_update': time.time(),
    'message': "Hunt those speeders – don't screw up!",
    'spot_order': []       # Fixed order for stable layout
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Lt. Betts angry image (furious yelling with campaign hat)
BETTS_IMG = "https://thumbs.dreamstime.com/b/angry-army-bootcamp-drill-sergeant-soldier-shouting-cartoon-209860607.jpg"

# Vehicle images (speeders vs innocents)
speeder_images = [
    "https://thumbs.dreamstime.com/b/beautiful-red-sports-car-speeding-highway-motion-blur-captured-panning-shot-mesmerizing-display-speed-power-350963559.jpg",
    "https://thumbs.dreamstime.com/b/red-sports-car-racing-sunny-day-speeding-along-high-speed-highway-turn-motion-blur-357021790.jpg",
    "https://thumbs.dreamstime.com/b/red-sports-car-speeding-racetrack-motion-blur-racing-along-showcasing-dynamic-enhances-thrilling-sense-speed-374738560.jpg"
]

innocent_images = [
    "https://roadloft.com/wp-content/uploads/2025/02/ROADLOFT_2024_0002-scaled.jpg",  # Minivan family
    "https://static01.nyt.com/images/2018/08/31/business/31wheels-4/merlin_142982265_f02f9ee8-159f-465a-a0fb-d332029ea03b-superJumbo.jpg",  # Honda Odyssey minivan
    "https://pxl-virginiadotorg.terminalfour.net/fit-in/1429x2000/filters:quality(80)/prod01/vdot-cdn-pxl/media/vdotvirginiagov/news-and-events/news/statewide/2025/Back-to-School.jpeg",  # School bus
    "https://platform.vox.com/wp-content/uploads/sites/2/2024/09/GettyImages-2172006355.jpg?quality=90&strip=all&crop=1.9366197183099%2C0%2C96.12676056338%2C100&w=2400"  # School bus scene
]

# Yells (kept offensive but thematic)
general_yells = [
    "CLICK FASTER YOU LAZY PIECE OF SHIT!",
    "YOU'RE LETTING SPEEDERS RUN WILD – PATHETIC!",
    "MY GRANDMA WOULD HAVE MORE STOPS BY NOW!",
    "QUOTA OR BUST – MOVE YOUR SORRY ASS!"
]

praise_yells = [
    "FINALLY! ONE LESS ASSHOLE ON THE ROAD!",
    "NOT COMPLETELY USELESS... YET!",
    "GOOD HIT – KEEP IT UP, IDIOT!"
]

wrong_yells = [
    "YOU PULLED OVER A SCHOOL BUS FULL OF KIDS, MORON!",
    "THAT WAS A MOM WITH TODDLERS – DISGRACE!",
    "AMBULANCE? YOU ALMOST KILLED SOMEONE, DUMBASS!",
    "ICE CREAM TRUCK? KIDS CRYING BECAUSE OF YOU!"
]

# ────────────────────────────────────────────────
# UI
# ────────────────────────────────────────────────
st.title("🚔 I-5 Speeder Hunt")
st.markdown("**How to play:** Click any **?** box once. It reveals the vehicle with an image. Speeders = +1 point. Innocents = -4 seconds & Betts rages. Survive 60 seconds!")

# HUD
c1, c2, c3, c4 = st.columns(4)
c1.metric("STOPS", st.session_state.score)
c2.metric("WRONGS", st.session_state.wrong_stops)
c3.metric("TIME LEFT", f"{max(0, int(st.session_state.time_left))}s")
rate = st.session_state.score / max(1, 60 - st.session_state.time_left)
c4.metric("RATE", f"{rate:.1f}/s")

st.error(f"**Lt. Betts SCREAMING:** {st.session_state.message}")

st.image(BETTS_IMG, width=220, caption="Lt. Scott Betts – Furious at Your Performance")

if not st.session_state.game_running:
    st.markdown("### Ready to patrol I-5?")
    if st.button("START PATROL – 60 SECONDS OF CHAOS!", type="primary", use_container_width=True):
        st.session_state.game_running = True
        st.session_state.score = 0
        st.session_state.wrong_stops = 0
        st.session_state.time_left = 60
        st.session_state.spots = {}
        st.session_state.next_id = 0
        st.session_state.last_update = time.time()
        st.session_state.message = random.choice(general_yells)
        st.session_state.spot_order = []

        # Initial vehicles (fixed order)
        for _ in range(12):
            spot_id = st.session_state.next_id
            is_speeder = random.random() < 0.6
            img_list = speeder_images if is_speeder else innocent_images
            vehicle = "Speeder" if is_speeder else "Innocent"
            st.session_state.spots[spot_id] = {
                'is_speeder': is_speeder,
                'revealed': False,
                'img_url': random.choice(img_list),
                'type': vehicle
            }
            st.session_state.spot_order.append(spot_id)
            st.session_state.next_id += 1
        st.rerun()
else:
    now = time.time()
    if now - st.session_state.last_update >= 1.0:
        st.session_state.time_left = max(0, st.session_state.time_left - 1)
        st.session_state.last_update = now

        # Spawn new (add to end of order, no shuffle)
        if len(st.session_state.spots) < 20:
            add = random.randint(1, 2)
            for _ in range(add):
                spot_id = st.session_state.next_id
                is_speeder = random.random() < 0.6
                img_list = speeder_images if is_speeder else innocent_images
                vehicle = "Speeder" if is_speeder else "Innocent"
                st.session_state.spots[spot_id] = {
                    'is_speeder': is_speeder,
                    'revealed': False,
                    'img_url': random.choice(img_list),
                    'type': vehicle
                }
                st.session_state.spot_order.append(spot_id)
                st.session_state.next_id += 1

        if st.session_state.time_left <= 0:
            st.session_state.game_running = False
            msg = "You survived... barely!" if st.session_state.score >= 30 else "Pathetic! Clean out your locker!"
            st.session_state.message = msg
            if st.session_state.score >= 30:
                st.balloons()
            st.rerun()

        st.rerun()

    # Render fixed-order board
    st.markdown("### Vehicles on I-5 – Click ? to Reveal (one click only)")

    cols_per_row = 4
    for i in range(0, len(st.session_state.spot_order), cols_per_row):
        row_ids = st.session_state.spot_order[i:i + cols_per_row]
        row_cols = st.columns(cols_per_row)
        for j, spot_id in enumerate(row_ids):
            with row_cols[j]:
                if spot_id not in st.session_state.spots:
                    continue  # cleaned up
                spot = st.session_state.spots[spot_id]

                if not spot['revealed']:
                    if st.button("?\n**REVEAL VEHICLE**", key=f"reveal_{spot_id}", help="Click once to check"):
                        spot['revealed'] = True
                        if spot['is_speeder']:
                            st.session_state.score += 1
                            st.session_state.message = random.choice(praise_yells)
                            st.success(f"**SPEEDER CAUGHT!**\n{spot['type']}\n+1 POINT")
                            st.image(spot['img_url'], width=200)
                            st.balloons() if st.session_state.score % 5 == 0 else None
                        else:
                            st.session_state.wrong_stops += 1
                            st.session_state.time_left = max(0, st.session_state.time_left - 4)
                            st.session_state.message = random.choice(wrong_yells)
                            st.error(f"**WRONG – INNOCENT!**\n{spot['type']}\n-4 SECONDS")
                            st.image(spot['img_url'], width=200)
                        st.rerun()
                else:
                    # Revealed – show image + label
                    color = "success" if spot['is_speeder'] else "error"
                    label = f"**{spot['type']}**"
                    if spot['is_speeder']:
                        st.success(label)
                    else:
                        st.error(label)
                    st.image(spot['img_url'], width=200)

# Play again
if not st.session_state.game_running and st.session_state.score > 0:
    if st.button("PLAY AGAIN – Prove Betts Wrong This Time"):
        st.session_state.game_running = True
        st.session_state.time_left = 60
        st.session_state.score = 0
        st.session_state.wrong_stops = 0
        st.session_state.spots = {}
        st.session_state.spot_order = []
        st.rerun()

st.markdown("---")
st.caption("Reveal vehicles with one click. Stable layout – no confusing shuffling. Score high to shut Lt. Betts up! Reboot app if needed.")
