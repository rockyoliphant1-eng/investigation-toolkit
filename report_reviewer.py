import streamlit as st
import math
import re
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# =========================================================
# PAGE CONFIG + SIMPLE STYLING
# =========================================================

st.set_page_config(
    page_title="LE Investigative Toolkit",
    layout="wide"
)

st.markdown("""
<style>
.main-title {
    font-size:36px;
    font-weight:700;
    color:#0f172a;
}
.sub-title {
    color:#334155;
}
.card {
    background-color:#f8fafc;
    padding:20px;
    border-radius:12px;
    border:1px solid #e2e8f0;
    margin-bottom:15px;
}
.warning-box {
    background:#fff7ed;
    border-left:5px solid #fb923c;
    padding:15px;
    border-radius:8px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Law Enforcement Investigation Toolkit</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AI-assisted report review and crash reconstruction tools</div>', unsafe_allow_html=True)

# =========================================================
# SECURITY MODE
# =========================================================

st.markdown('<div class="warning-box">Secure Mode prevents reports from being sent to external AI.</div>', unsafe_allow_html=True)

secure_mode = st.toggle("Secure Mode (Block external AI)", value=True)

if not secure_mode:
    from openai import OpenAI
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# =========================================================
# ADVANCED LAW ENFORCEMENT PII SCRUBBER
# =========================================================

def scrub_police_pii(text):

    # Names (first + last, any case)
    text = re.sub(
        r'\b([A-Za-z]+)\s([A-Za-z]+)\b',
        '[NAME REDACTED]',
        text,
        flags=re.IGNORECASE
    )

    # Last names after role identifiers
    text = re.sub(
        r'\b(suspect|driver|subject|victim|witness|passenger|officer)\s([A-Za-z]+)\b',
        r'\1 [NAME REDACTED]',
        text,
        flags=re.IGNORECASE
    )

    # DOB
    text = re.sub(r'\bDOB[: ]*\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', '[DOB REDACTED]', text)

    # Dates
    text = re.sub(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', '[DATE REDACTED]', text)

    # SSN
    text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN REDACTED]', text)

    # Phone
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE REDACTED]', text)

    # Email
    text = re.sub(r'\S+@\S+\.\S+', '[EMAIL REDACTED]', text)

    # VIN (17 characters)
    text = re.sub(r'\b[A-HJ-NPR-Z0-9]{17}\b', '[VIN REDACTED]', text)

    # License plates
    text = re.sub(r'\b[A-Z]{1,3}[0-9]{1,4}\b', '[PLATE REDACTED]', text)

    # Driver license numbers
    text = re.sub(r'\bDL[: ]*[A-Z0-9]{5,15}\b', '[DL REDACTED]', text)

    # Addresses
    text = re.sub(
        r'\b\d{1,5}\s[A-Za-z0-9\s]+\s(?:Street|St|Road|Rd|Ave|Avenue|Blvd|Lane|Ln|Drive|Dr|Court|Ct)\b',
        '[ADDRESS REDACTED]',
        text
    )

    # Case numbers
    text = re.sub(r'\bcase[: ]*[0-9\-]{4,12}\b', '[CASE NUMBER REDACTED]', text, flags=re.IGNORECASE)

    # GPS coordinates
    text = re.sub(r'\b-?\d{1,3}\.\d+,\s?-?\d{1,3}\.\d+\b', '[GPS REDACTED]', text)

    # Badge numbers
    text = re.sub(r'\bbadge\s?\d{1,6}\b', '[BADGE REDACTED]', text, flags=re.IGNORECASE)

    # Unit numbers
    text = re.sub(r'\bunit\s?\d{1,4}\b', '[UNIT REDACTED]', text, flags=re.IGNORECASE)

    # Clean whitespace
    text = re.sub(r'\s+', ' ', text)

    return text


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "Report Review",
    "Defense Attorney Review",
    "Crash Reconstruction",
    "Scene Diagrams"
])

# =========================================================
# REPORT REVIEW
# =========================================================

with tab1:

    st.header("Police Report Review")

    report_text = st.text_area("Paste Police Report", height=300)

    if st.button("Analyze Report"):

        if report_text.strip() == "":
            st.warning("Paste a report first")

        else:

            clean_report = scrub_police_pii(report_text)

            with st.expander("Sanitized Report"):
                st.write(clean_report)

            if secure_mode:

                st.success("Secure Mode enabled — no external AI used")

            else:

                prompt = f"""
You are a senior police supervisor reviewing a report.

Identify:

- articulation issues
- missing investigative details
- timeline gaps
- probable cause weaknesses

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


# =========================================================
# DEFENSE ATTORNEY REVIEW
# =========================================================

with tab2:

    st.header("Defense Attorney Review Mode")

    report_def = st.text_area("Paste Report")

    if st.button("Run Defense Review"):

        if report_def.strip() == "":
            st.warning("Paste a report")

        else:

            clean_report = scrub_police_pii(report_def)

            if secure_mode:

                st.warning("Secure Mode enabled — AI review blocked")

            else:

                prompt = f"""
You are a criminal defense attorney analyzing a police report.

Identify potential legal weaknesses such as:

- probable cause challenges
- reasonable suspicion issues
- articulation weaknesses
- missing observations
- timeline inconsistencies

Explain how a defense attorney might challenge the report.

REPORT:
{clean_report}
"""

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role":"user","content":prompt}]
                )

                st.write(response.choices[0].message.content)


# =========================================================
# CRASH RECONSTRUCTION
# =========================================================

with tab3:

    st.header("Crash Reconstruction Tools")

    drag = st.number_input("Drag Factor", value=0.70)
    skid = st.number_input("Skid Distance (ft)", value=100.0)

    if st.button("Calculate Skid Speed"):

        speed = math.sqrt(30 * drag * skid)
        st.success(f"Estimated Speed: {speed:.2f} mph")

    st.subheader("Delta-V")

    v1 = st.number_input("Vehicle 1 Speed", value=40.0)
    v2 = st.number_input("Vehicle 2 Speed", value=0.0)

    w1 = st.number_input("Vehicle 1 Weight", value=4000.0)
    w2 = st.number_input("Vehicle 2 Weight", value=4000.0)

    if st.button("Calculate Delta V"):

        v1_fps = v1 * 1.47
        v2_fps = v2 * 1.47

        total = w1 + w2

        dv1 = abs((w2 * (v2_fps - v1_fps)) / total) / 1.47
        dv2 = abs((w1 * (v1_fps - v2_fps)) / total) / 1.47

        st.success(f"Vehicle 1 Delta-V: {dv1:.2f} mph")
        st.success(f"Vehicle 2 Delta-V: {dv2:.2f} mph")


# =========================================================
# SCENE DIAGRAM GENERATOR
# =========================================================

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
            (-100, -lane_width),
            200,
            lane_width*2,
            edgecolor='gray',
            facecolor='lightgray'
        )

        ax.add_patch(road)

        car1 = patches.Rectangle((v1x, v1y), 15, 6, color='blue')
        car2 = patches.Rectangle((v2x, v2y), 15, 6, color='red')

        ax.add_patch(car1)
        ax.add_patch(car2)

        ax.set_xlim(-100,100)
        ax.set_ylim(-50,50)

        ax.set_title("Crash Scene Diagram")
        ax.grid(True)

        st.pyplot(fig)
