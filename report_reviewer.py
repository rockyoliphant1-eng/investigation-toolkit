import streamlit as st
import re
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# =====================================================
# PAGE SETUP
# =====================================================

st.set_page_config(
    page_title="Law Enforcement Investigative Toolkit",
    layout="wide"
)

# =====================================================
# STYLE (BADGE + POLICE LIGHTS)
# =====================================================

st.markdown("""
<style>

.header {
    text-align:center;
}

.title {
    font-size:40px;
    font-weight:bold;
}

.subtitle {
    color:gray;
}

.lights {
    height:10px;
    background: linear-gradient(90deg, red 50%, blue 50%);
    background-size:40px 10px;
    animation: flash 1s linear infinite;
}

@keyframes flash {
    from {background-position:0px;}
    to {background-position:40px;}
}

.card {
    background:#f8fafc;
    padding:20px;
    border-radius:10px;
    border:1px solid #e2e8f0;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="lights"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="header">
<div class="title">🛡️ Law Enforcement Investigative Toolkit</div>
<div class="subtitle">Report review • Reconstruction tools • Investigation analysis</div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# SECURITY MODE
# =====================================================

secure_mode = st.toggle("🔒 Secure Mode (Block external AI)", value=True)

if not secure_mode:
    from openai import OpenAI
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# =====================================================
# SMART PII SCRUBBER
# =====================================================

def scrub_police_pii(text):

    # ------------------------------------------------
    # PERSON IDENTIFIERS
    # ------------------------------------------------

    text = re.sub(r'\bDOB[: ]*\d{1,2}[/-]\d{1,2}[/-]\d{4}\b',
                  '[DOB REDACTED]', text, flags=re.IGNORECASE)

    text = re.sub(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b',
                  '[DOB REDACTED]', text)

    text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b',
                  '[SSN REDACTED]', text)

    # ------------------------------------------------
    # VEHICLE IDENTIFIERS
    # ------------------------------------------------

    text = re.sub(r'\b[A-HJ-NPR-Z0-9]{17}\b',
                  '[VIN REDACTED]', text)

    text = re.sub(r'\b[A-Z]{3}-?\d{3,4}\b',
                  '[PLATE REDACTED]', text)

    # ------------------------------------------------
    # LICENSE NUMBERS
    # ------------------------------------------------

    text = re.sub(r'\b[A-Z]\d{2}-\d{3}-\d{3}\b',
                  '[DL REDACTED]', text)

    # ------------------------------------------------
    # PHONE NUMBERS
    # ------------------------------------------------

    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
                  '[PHONE REDACTED]', text)

    # ------------------------------------------------
    # ADDRESS
    # ------------------------------------------------

    text = re.sub(
        r'\b\d{1,5}\s[A-Za-z]+\s(?:Street|St|Road|Rd|Ave|Avenue|Blvd|Lane|Ln|Drive|Dr|Court|Ct)\b',
        '[ADDRESS REDACTED]',
        text
    )

    text = re.sub(r'\bApt\.?\s?\w+\b',
                  '[APT REDACTED]', text)

    # ------------------------------------------------
    # AGENCY IDENTIFIERS
    # ------------------------------------------------

    text = re.sub(r'\bBadge\s?#?\d+\b',
                  '[BADGE REDACTED]', text, flags=re.IGNORECASE)

    text = re.sub(r'\bUnit\s?#?\d+\b',
                  '[UNIT REDACTED]', text, flags=re.IGNORECASE)

    text = re.sub(r'\bCase\s?#?\d+\b',
                  '[CASE REDACTED]', text, flags=re.IGNORECASE)

    # ------------------------------------------------
    # ROLE-BASED NAME REDACTION
    # ------------------------------------------------

    roles = [
        "driver",
        "suspect",
        "subject",
        "victim",
        "witness",
        "officer",
        "deputy",
        "passenger"
    ]

    for role in roles:

        text = re.sub(
            rf"\b{role}\s+[A-Z][a-z]+\s?[A-Z]?[a-z]*\b",
            f"{role} [NAME REDACTED]",
            text,
            flags=re.IGNORECASE
        )

    # ------------------------------------------------
    # NAME AFTER IDENTIFIER
    # ------------------------------------------------

    text = re.sub(
        r'identified by license as\s+[A-Z][a-z]+\s[A-Z][a-z]+',
        'identified by license as [NAME REDACTED]',
        text,
        flags=re.IGNORECASE
    )

    return text

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "Report Review",
    "Defense Review",
    "Crash Reconstruction",
    "Scene Diagrams"
])

# =====================================================
# REPORT REVIEW
# =====================================================

with tab1:

    st.header("📝 Police Report Review")

    report = st.text_area("Paste Report", height=300)

    if st.button("Analyze Report"):

        if report.strip() == "":
            st.warning("Please paste a report")

        else:

            clean = scrub_police_pii(report)

            with st.expander("Sanitized Report"):
                st.write(clean)

            if secure_mode:

                st.success("Secure Mode enabled — report not sent to AI")

            else:

                prompt = f"""
You are a senior police supervisor reviewing a report.

Identify:
• articulation weaknesses
• missing investigative steps
• timeline problems
• probable cause issues

REPORT:
{clean}
"""

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role":"user","content":prompt}]
                )

                st.write(response.choices[0].message.content)

# =====================================================
# DEFENSE ATTORNEY REVIEW
# =====================================================

with tab2:

    st.header("⚖️ Defense Attorney Analysis")

    defense = st.text_area("Paste Report for Defense Review")

    if st.button("Run Defense Analysis"):

        if defense.strip() == "":
            st.warning("Paste a report")

        else:

            clean = scrub_police_pii(defense)

            if secure_mode:

                st.warning("Secure Mode enabled — AI analysis disabled")

            else:

                prompt = f"""
You are a criminal defense attorney reviewing a police report.

Identify possible weaknesses such as:

• probable cause challenges
• reasonable suspicion issues
• articulation weaknesses
• missing evidence
• timeline inconsistencies

Explain how the defense could challenge the report.

REPORT:
{clean}
"""

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role":"user","content":prompt}]
                )

                st.write(response.choices[0].message.content)

# =====================================================
# CRASH RECONSTRUCTION
# =====================================================

with tab3:

    st.header("🚔 Crash Reconstruction")

    drag = st.number_input("Drag Factor", value=0.70)
    skid = st.number_input("Skid Distance (ft)", value=100.0)

    if st.button("Calculate Speed"):

        speed = math.sqrt(30 * drag * skid)
        st.success(f"Estimated Speed: {speed:.2f} mph")

    st.subheader("Delta-V")

    v1 = st.number_input("Vehicle 1 Speed", value=40.0)
    v2 = st.number_input("Vehicle 2 Speed", value=0.0)

    w1 = st.number_input("Vehicle 1 Weight", value=4000.0)
    w2 = st.number_input("Vehicle 2 Weight", value=4000.0)

    if st.button("Calculate Delta-V"):

        v1fps = v1 * 1.47
        v2fps = v2 * 1.47

        total = w1 + w2

        dv1 = abs((w2*(v2fps-v1fps))/total)/1.47
        dv2 = abs((w1*(v1fps-v2fps))/total)/1.47

        st.success(f"Vehicle 1 ΔV: {dv1:.2f} mph")
        st.success(f"Vehicle 2 ΔV: {dv2:.2f} mph")

# =====================================================
# SCENE DIAGRAM
# =====================================================

with tab4:

    st.header("🗺 Crash Scene Diagram")

    lane = st.number_input("Lane Width", value=12.0)

    v1x = st.number_input("Vehicle 1 X", value=0.0)
    v1y = st.number_input("Vehicle 1 Y", value=0.0)

    v2x = st.number_input("Vehicle 2 X", value=40.0)
    v2y = st.number_input("Vehicle 2 Y", value=0.0)

    if st.button("Generate Diagram"):

        fig, ax = plt.subplots()

        road = patches.Rectangle(
            (-100,-lane),
            200,
            lane*2,
            edgecolor="gray",
            facecolor="lightgray"
        )

        ax.add_patch(road)

        car1 = patches.Rectangle((v1x,v1y),15,6,color="blue")
        car2 = patches.Rectangle((v2x,v2y),15,6,color="red")

        ax.add_patch(car1)
        ax.add_patch(car2)

        ax.set_xlim(-100,100)
        ax.set_ylim(-50,50)

        ax.set_title("Crash Scene Diagram")

        ax.grid(True)

        st.pyplot(fig)


