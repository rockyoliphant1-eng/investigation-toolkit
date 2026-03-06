import streamlit as st
import re
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="LE Investigative Toolkit",
    layout="wide"
)

# =====================================================
# CLEAN UI STYLE
# =====================================================

st.markdown("""
<style>

.header {
    text-align:center;
    margin-bottom:20px;
}

.title {
    font-size:36px;
    font-weight:bold;
}

.subtitle {
    color:gray;
}

.accent-bar {
    height:6px;
    background: linear-gradient(90deg,#1e40af,#64748b);
    border-radius:4px;
    margin-bottom:20px;
}

.card {
    background:#f8fafc;
    padding:18px;
    border-radius:10px;
    border:1px solid #e2e8f0;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="accent-bar"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="header">
<div class="title">🛡 Law Enforcement Investigation Toolkit</div>
<div class="subtitle">Report Review • Reconstruction Tools • Investigation Analysis</div>
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
# PII SCRUBBER
# =====================================================

def scrub_police_pii(text):

    # DOB
    text = re.sub(r'\bDOB[: ]*\d{1,2}[/-]\d{1,2}[/-]\d{4}', '[DOB REDACTED]', text, flags=re.IGNORECASE)
    text = re.sub(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{4}', '[DOB REDACTED]', text)

    # SSN
    text = re.sub(r'\b\d{3}-\d{2}-\d{4}', '[SSN REDACTED]', text)

    # phone
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}', '[PHONE REDACTED]', text)

    # VIN
    text = re.sub(r'\b[A-HJ-NPR-Z0-9]{17}', '[VIN REDACTED]', text)

    # license plates
    text = re.sub(r'\b[A-Z]{3}-?\d{3,4}', '[PLATE REDACTED]', text)

    # driver license
    text = re.sub(r'\b[A-Z]\d{2}-\d{3}-\d{3}', '[DL REDACTED]', text)

    # badge numbers
    text = re.sub(r'Badge\s?#?\d+', '[BADGE REDACTED]', text, flags=re.IGNORECASE)

    # addresses
    text = re.sub(
        r'\b\d{1,5}\s[A-Za-z]+\s(?:Street|St|Road|Rd|Ave|Avenue|Blvd|Lane|Ln|Drive|Dr|Court|Ct)',
        '[ADDRESS REDACTED]',
        text
    )

    text = re.sub(r'\bApt\.?\s?\w+', '[APT REDACTED]', text)

    # names with middle initial
    text = re.sub(
        r'\b[A-Z][a-z]+\s[A-Z]\.\s[A-Z][a-z]+',
        '[NAME REDACTED]',
        text
    )

    # role based names
    roles = ["driver","subject","suspect","victim","witness","officer","deputy"]

    for role in roles:
        text = re.sub(
            rf"\b{role}\s+[A-Z][a-z]+(?:\s[A-Z][a-z]+)?",
            f"{role} [NAME REDACTED]",
            text,
            flags=re.IGNORECASE
        )

    # colon identifiers
    text = re.sub(
        r'(subject|suspect|driver|victim|witness)\s*:\s*[A-Z][a-z]+\s?[A-Z]?\.\s?[A-Z][a-z]+',
        r'\1: [NAME REDACTED]',
        text,
        flags=re.IGNORECASE
    )

    # residual first last names
    text = re.sub(
        r'\b[A-Z][a-z]+\s[A-Z][a-z]+',
        '[NAME REDACTED]',
        text
    )

    return text


# =====================================================
# PII DETECTION REPORT
# =====================================================

def detect_pii(text):

    report = {}

    report["DOB"] = len(re.findall(r'\d{1,2}[/-]\d{1,2}[/-]\d{4}', text))
    report["Plates"] = len(re.findall(r'[A-Z]{3}-?\d{3,4}', text))
    report["VIN"] = len(re.findall(r'[A-HJ-NPR-Z0-9]{17}', text))
    report["Phones"] = len(re.findall(r'\d{3}[-.]?\d{3}[-.]?\d{4}', text))
    report["Addresses"] = len(re.findall(r'\d{1,5}\s[A-Za-z]+\s(?:Street|St|Road|Rd|Ave)', text))

    return report


# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "Report Review",
    "Defense Review",
    "Crash Reconstruction",
    "Scene Diagram"
])

# =====================================================
# REPORT REVIEW
# =====================================================

with tab1:

    st.header("Police Report Review")

    report = st.text_area("Paste Report", height=300)

    if st.button("Analyze Report"):

        if report.strip() == "":
            st.warning("Paste a report first")

        else:

            detection = detect_pii(report)

            st.subheader("PII Detection Summary")

            st.write(detection)

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
• timeline gaps
• probable cause issues

REPORT:
{clean}
"""

                try:

                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role":"user","content":prompt}]
                    )

                    st.write(response.choices[0].message.content)

                except:
                    st.error("AI request failed")

# =====================================================
# DEFENSE REVIEW
# =====================================================

with tab2:

    st.header("Defense Attorney Review")

    defense = st.text_area("Paste Report")

    if st.button("Run Defense Analysis"):

        if defense.strip() == "":
            st.warning("Paste a report")

        else:

            clean = scrub_police_pii(defense)

            if secure_mode:

                st.warning("Secure Mode enabled — AI analysis blocked")

            else:

                prompt = f"""
You are a criminal defense attorney reviewing a police report.

Identify possible weaknesses:

• probable cause issues
• reasonable suspicion issues
• articulation problems
• missing observations
• timeline inconsistencies

Explain how a defense attorney would challenge the report.

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

    st.header("Crash Reconstruction Tools")

    drag = st.number_input("Drag Factor", value=0.70)
    skid = st.number_input("Skid Distance (ft)", value=100.0)

    if st.button("Calculate Speed"):

        speed = math.sqrt(30 * drag * skid)

        st.success(f"Estimated Speed: {speed:.2f} mph")

# =====================================================
# SCENE DIAGRAM
# =====================================================

with tab4:

    st.header("Crash Scene Diagram")

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
