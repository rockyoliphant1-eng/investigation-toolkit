import streamlit as st
from openai import OpenAI
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# -----------------------------
# CONFIG
# -----------------------------

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(
    page_title="LE Investigative Toolkit",
    layout="wide"
)

st.title("Law Enforcement Investigation Toolkit")
st.write("AI-powered report review and crash reconstruction tools.")

# -----------------------------
# TABS
# -----------------------------

tab1, tab2, tab3, tab4 = st.tabs([
    "Report Review",
    "Crash Reconstruction",
    "Scene Diagrams",
    "AI Investigation Assistant"
])

# =====================================================
# TAB 1 — REPORT REVIEW
# =====================================================

with tab1:

    st.header("AI Police Report Reviewer")

    report_text = st.text_area("Paste Police Report", height=300)

    if st.button("Review Report"):

        if report_text.strip() == "":
            st.warning("Please paste a report first.")

        else:

            prompt = f"""
You are a senior law enforcement supervisor reviewing an officer report.

Check for:

• grammar and clarity
• missing investigative details
• weak articulation
• timeline issues
• reasonable suspicion articulation
• probable cause articulation

Provide:

SUMMARY

ISSUES FOUND

MISSING DETAILS

LEGAL REVIEW

SUGGESTED IMPROVEMENTS

SUPERVISOR COMMENTS

REPORT QUALITY SCORE

REPORT:
{report_text}
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role":"user","content":prompt}]
            )

            st.subheader("Review Results")
            st.write(response.choices[0].message.content)

# =====================================================
# TAB 2 — CRASH RECONSTRUCTION
# =====================================================

with tab2:

    st.header("Crash Reconstruction Calculators")

    st.subheader("Speed From Skid Marks")

    drag_factor = st.number_input("Drag Factor", value=0.70)
    skid_distance = st.number_input("Skid Distance (ft)", value=100.0)

    if st.button("Calculate Skid Speed"):

        speed = math.sqrt(30 * drag_factor * skid_distance)
        st.success(f"Estimated Speed: {speed:.2f} mph")

    st.divider()

    st.subheader("Stopping Distance")

    speed_mph = st.number_input("Vehicle Speed (mph)", value=50.0)
    reaction_time = st.number_input("Reaction Time (seconds)", value=1.5)

    if st.button("Calculate Stopping Distance"):

        speed_fps = speed_mph * 1.47
        reaction_distance = speed_fps * reaction_time
        braking_distance = (speed_mph ** 2) / (30 * drag_factor)

        total = reaction_distance + braking_distance

        st.success(f"Reaction Distance: {reaction_distance:.1f} ft")
        st.success(f"Braking Distance: {braking_distance:.1f} ft")
        st.success(f"Total Distance: {total:.1f} ft")

    st.divider()

    st.subheader("Yaw Speed Calculator")

    yaw_radius = st.number_input("Yaw Radius (ft)", value=100.0)
    yaw_drag = st.number_input("Yaw Drag Factor", value=0.75)

    if st.button("Calculate Yaw Speed"):

        yaw_speed = math.sqrt(15 * yaw_radius * yaw_drag)
        st.success(f"Estimated Speed: {yaw_speed:.2f} mph")

    st.divider()

    st.subheader("Delta-V Estimate")

    v1 = st.number_input("Vehicle 1 Speed (mph)", value=40.0)
    v2 = st.number_input("Vehicle 2 Speed (mph)", value=0.0)

    w1 = st.number_input("Vehicle 1 Weight (lbs)", value=4000.0)
    w2 = st.number_input("Vehicle 2 Weight (lbs)", value=4000.0)

    if st.button("Calculate Delta-V"):

        v1_fps = v1 * 1.47
        v2_fps = v2 * 1.47

        total_mass = w1 + w2

        delta_v1 = abs((w2 * (v2_fps - v1_fps)) / total_mass) / 1.47
        delta_v2 = abs((w1 * (v1_fps - v2_fps)) / total_mass) / 1.47

        st.success(f"Vehicle 1 Delta-V: {delta_v1:.2f} mph")
        st.success(f"Vehicle 2 Delta-V: {delta_v2:.2f} mph")

    st.divider()

    st.subheader("Drag Factor Reference")

    surface = st.selectbox(
        "Road Surface",
        ["Dry Asphalt","Wet Asphalt","Dry Concrete","Wet Concrete","Gravel","Snow","Ice"]
    )

    drag_values = {
        "Dry Asphalt":0.70,
        "Wet Asphalt":0.60,
        "Dry Concrete":0.80,
        "Wet Concrete":0.70,
        "Gravel":0.50,
        "Snow":0.30,
        "Ice":0.10
    }

    st.info(f"Typical Drag Factor: {drag_values[surface]}")

# =====================================================
# TAB 3 — SCENE DIAGRAMS
# =====================================================

with tab3:

    st.header("Crash Scene Diagram Generator")

    lane_width = st.number_input("Lane Width (ft)", value=12.0)

    v1_x = st.number_input("Vehicle 1 X Position", value=0.0)
    v1_y = st.number_input("Vehicle 1 Y Position", value=0.0)

    v2_x = st.number_input("Vehicle 2 X Position", value=40.0)
    v2_y = st.number_input("Vehicle 2 Y Position", value=0.0)

    if st.button("Generate Diagram"):

        fig, ax = plt.subplots()

        road = patches.Rectangle(
            (-100,-lane_width),
            200,
            lane_width*2,
            edgecolor='gray',
            facecolor='lightgray'
        )

        ax.add_patch(road)

        vehicle1 = patches.Rectangle((v1_x,v1_y),15,6,color='blue')
        vehicle2 = patches.Rectangle((v2_x,v2_y),15,6,color='red')

        ax.add_patch(vehicle1)
        ax.add_patch(vehicle2)

        ax.set_xlim(-100,100)
        ax.set_ylim(-50,50)

        ax.set_title("Crash Scene Diagram (Top View)")
        ax.grid(True)

        st.pyplot(fig)

# =====================================================
# TAB 4 — AI INVESTIGATION ASSISTANT
# =====================================================

with tab4:

    st.header("AI Crash Reconstruction Assistant")

    notes = st.text_area("Enter Investigation Notes")

    if st.button("Analyze Investigation"):

        prompt = f"""
You are a professional traffic collision reconstructionist.

Analyze the notes and provide:

• possible collision sequence
• speed considerations
• missing investigative evidence
• weaknesses in documentation
• recommended reconstruction steps

NOTES:
{notes}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}]
        )


        st.write(response.choices[0].message.content)
