import streamlit as st
from openai import OpenAI
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import re

# ==========================================================
# CONFIG
# ==========================================================

st.set_page_config(
    page_title="LE Investigative Toolkit",
    layout="wide"
)

st.title("Law Enforcement Investigation Toolkit")

st.warning("Secure Mode prevents reports from being sent to external AI systems.")

secure_mode = st.toggle("Secure Mode (Block external AI)", value=True)

if not secure_mode:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ==========================================================
# LAW ENFORCEMENT PII SCRUBBER
# ==========================================================

def scrub_police_pii(text):

    text = re.sub(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', '[NAME REDACTED]', text)

    text = re.sub(r'\bDOB[: ]*\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', '[DOB REDACTED]', text)
    text = re.sub(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', '[DATE REDACTED]', text)

    text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN REDACTED]', text)

    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE REDACTED]', text)

    text = re.sub(r'\b[A-HJ-NPR-Z0-9]{17}\b', '[VIN REDACTED]', text)

    text = re.sub(r'\b[A-Z]{1,3}[0-9]{1,4}\b', '[PLATE REDACTED]', text)

    text = re.sub(
        r'\b\d{1,5}\s[A-Za-z0-9\s]+\s(?:Street|St|Road|Rd|Ave|Avenue|Blvd|Lane|Ln|Drive|Dr|Court|Ct)\b',
        '[ADDRESS REDACTED]',
        text
    )

    text = re.sub(r'\bCase[: ]*\d{2,6}-?\d{2,6}\b', '[CASE NUMBER REDACTED]', text)

    return text


# ==========================================================
# TABS
# ==========================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "Report Review",
    "Defense Attorney Review",
    "Crash Reconstruction",
    "Scene Diagrams"
])

# ==========================================================
# REPORT REVIEW
# ==========================================================

with tab1:

    st.header("Police Report Review")

    report_text = st.text_area("Paste Report", height=300)

    if st.button("Analyze Report"):

        if report_text.strip() == "":
            st.warning("Please paste a report first")

        else:

            clean_report = scrub_police_pii(report_text)

            with st.expander("Sanitized Report (PII Removed)"):
                st.write(clean_report)

            if secure_mode:

                st.success("Secure Mode Enabled — Report NOT sent to AI")

                st.info("Use sanitized preview above for manual review.")

            else:

                prompt = f"""
You are a senior police supervisor reviewing a report.

Identify:

• articulation weaknesses
• missing investigative details
• timeline issues
• probable cause issues

REPORT:
{clean_report}
"""

                try:

                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role":"user","content":prompt}]
                    )

                    st.write(response.choices[0].message.content)

                except Exception:

                    st.error("AI request failed")

# ==========================================================
# DEFENSE ATTORNEY REVIEW
# ==========================================================

with tab2:

    st.header("Defense Attorney Review Mode")

    report_text_defense = st.text_area("Paste Report for Defense Analysis")

    if st.button("Run Defense Review"):

        if report_text_defense.strip() == "":
            st.warning("Paste a report")

        else:

            clean_report = scrub_police_pii(report_text_defense)

            if secure_mode:

                st.warning("Secure Mode enabled. Defense analysis requires AI access.")

            else:

                prompt = f"""
You are a criminal defense attorney reviewing a police report.

Identify potential legal weaknesses such as:

• probable cause challenges
• reasonable suspicion issues
• timeline inconsistencies
• missing officer observations
• articulation problems

Explain how a defense attorney might attack the report.

REPORT:
{clean_report}
"""

                try:

                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role":"user","content":prompt}]
                    )

                    st.write(response.choices[0].message.content)

                except Exception:

                    st.error("AI request failed")


# ==========================================================
# CRASH RECONSTRUCTION
# ==========================================================

with tab3:

    st.header("Crash Reconstruction Calculators")

    drag_factor = st.number_input("Drag Factor", value=0.7)
    skid_distance = st.number_input("Skid Distance (ft)", value=100.0)

    if st.button("Calculate Speed"):

        speed = math.sqrt(30 * drag_factor * skid_distance)

        st.success(f"Estimated Speed: {speed:.2f} mph")

    st.subheader("Delta-V Estimate")

    v1 = st.number_input("Vehicle 1 Speed", value=40.0)
    v2 = st.number_input("Vehicle 2 Speed", value=0.0)

    w1 = st.number_input("Vehicle 1 Weight", value=4000.0)
    w2 = st.number_input("Vehicle 2 Weight", value=4000.0)

    if st.button("Calculate Delta V"):

        v1_fps = v1 * 1.47
        v2_fps = v2 * 1.47

        total_mass = w1 + w2

        dv1 = abs((w2 * (v2_fps - v1_fps)) / total_mass) / 1.47
        dv2 = abs((w1 * (v1_fps - v2_fps)) / total_mass) / 1.47

        st.success(f"Vehicle 1 Delta-V: {dv1:.2f} mph")
        st.success(f"Vehicle 2 Delta-V: {dv2:.2f} mph")

# ==========================================================
# SCENE DIAGRAM
# ==========================================================

with tab4:

    st.header("Crash Scene Diagram")

    lane_width = st.number_input("Lane Width", value=12.0)

    v1x = st.number_input("Vehicle 1 X", value=0.0)
    v1y = st.number_input("Vehicle 1 Y", value=0.0)

    v2x = st.number_input("Vehicle 2 X", value=40.0)
    v2y = st.number_input("Vehicle 2 Y", value=0.0)

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

        car1 = patches.Rectangle((v1x,v1y),15,6,color='blue')
        car2 = patches.Rectangle((v2x,v2y),15,6,color='red')

        ax.add_patch(car1)
        ax.add_patch(car2)

        ax.set_xlim(-100,100)
        ax.set_ylim(-50,50)

        ax.set_title("Crash Scene Diagram")

        ax.grid(True)

        st.pyplot(fig)
