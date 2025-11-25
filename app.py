import streamlit as st
from PIL import Image
import random
import io

st.set_page_config(page_title="Ema Claims MVP", layout="centered")

def mock_extract_from_image(image_bytes):
    # Mocked extraction: randomly pick values for demo
    makes = ["Hyundai", "Maruti Suzuki", "Tata", "Mahindra", "Honda"]
    damages = ["Front bumper", "Rear bumper", "Side door", "Windshield", "Headlight"]
    return {
        "vehicle_make": random.choice(makes),
        "license_plate": "MH12AB" + str(random.randint(1000,9999)),
        "damage_detected": random.choice(damages),
        "damage_severity": random.choice(["Minor", "Moderate", "Severe"]),
        "estimated_damage_percent": random.randint(5,75)
    }

def mock_triage(severity, damage_percent):
    # Simple rule-based triage
    if severity == "Severe" or damage_percent > 50:
        return "High"
    if severity == "Moderate" or damage_percent > 20:
        return "Medium"
    return "Low"

def mock_fraud_score(data):
    # Mocked scoring using random factors
    score = 10
    if data.get("damage_severity") == "Severe":
        score += 20
    score += int(data.get("estimated_damage_percent", 0) / 2)
    score += random.randint(0,15)
    return min(score, 100)

def mock_settlement_estimate(damage_percent, severity):
    base_value = 15000  # base for demo
    multiplier = 1 + (damage_percent / 100.0)
    if severity == "Severe":
        multiplier += 0.5
    estimated = int(base_value * multiplier)
    return estimated

st.title("Ema — Claims Processing MVP (Prototype)")
st.write("Option A — Simple UI. This is a **mocked** agentic claims prototype for demonstration purposes.")

with st.sidebar:
    st.header("FNOL Intake")
    claimant_name = st.text_input("Claimant Name", "Amit Kumar")
    policy_number = st.text_input("Policy Number", "POL123456789")
    contact = st.text_input("Contact Number / Email", "99999XXXXX / amit@example.com")
    accident_date = st.date_input("Accident Date")
    submit_btn = st.button("Start FNOL")

st.header("1) Upload Photos / Evidence")
uploaded = st.file_uploader("Upload accident photos (optional)", type=["jpg","jpeg","png"], accept_multiple_files=True)

if submit_btn or uploaded:
    st.subheader("AI Intake & Extraction")
    if uploaded:
        images_info = []
        for f in uploaded:
            img_bytes = f.read()
            info = mock_extract_from_image(img_bytes)
            images_info.append(info)
        # aggregate simple view
        info = images_info[0]
        st.success("AI extracted the following (mocked):")
        st.write({
            "vehicle_make": info["vehicle_make"],
            "license_plate": info["license_plate"],
            "damage_detected": info["damage_detected"],
            "damage_severity": info["damage_severity"],
            "estimated_damage_percent": info["estimated_damage_percent"]
        })
    else:
        st.info("No image uploaded — using sample/mock extraction.")
        info = mock_extract_from_image(b"")
        st.write(info)

    st.markdown("---")
    st.subheader("2) Triage & Assignment")
    triage = mock_triage(info["damage_severity"], info["estimated_damage_percent"])
    st.write(f"**Triage Level:** {triage}")
    # Mock adjuster assignment
    adjusters = {
        "Low": "Adjuster - Rajesh (Quick Claims)",
        "Medium": "Adjuster - Priya (Experienced)",
        "High": "Adjuster - Anil (Senior - SIU notified)"
    }
    assigned = adjusters.get(triage, "Adjuster - Default")
    st.write(f"**Assigned To:** {assigned}")

    st.markdown("---")
    st.subheader("3) Investigation Orchestration")
    st.write("Agent actions (mocked):")
    st.write("- Requested documents: RC, DL, FIR (if applicable)")
    st.write("- Scheduled appraiser visit within 48 hours (mocked)")
    st.write("- Sent SMS/Email reminders to claimant")

    st.markdown("---")
    st.subheader("4) Fraud Risk Scoring")
    fraud_score = mock_fraud_score(info)
    st.metric("Fraud Risk Score", f"{fraud_score}%")
    if fraud_score > 60:
        st.warning("High fraud risk — escalate to SIU.")
    elif fraud_score > 30:
        st.info("Medium fraud risk — flag for manual review.")
    else:
        st.success("Low fraud risk.")

    st.markdown("---")
    st.subheader("5) Settlement Recommendation")
    est = mock_settlement_estimate(info["estimated_damage_percent"], info["damage_severity"])
    st.write(f"Estimated Repair Cost (mocked): ₹{est:,}")
    st.write("AI Suggested Action: **Approve repair estimate**" if triage != "High" else "AI Suggested Action: **Hold & Investigate**")

    st.markdown("---")
    st.subheader("Export / Next Steps")
    st.write("You can export the extracted FNOL as JSON for the existing claims system (mocked).")

    export = {
        "claimant_name": claimant_name,
        "policy_number": policy_number,
        "contact": contact,
        "accident_date": str(accident_date),
        "extracted_info": info,
        "triage": triage,
        "assigned_adjuster": assigned,
        "fraud_score": fraud_score,
        "settlement_estimate": est
    }

    st.download_button("Download FNOL JSON", data=io.BytesIO(json.dumps(export, indent=2).encode('utf-8')), file_name="fnol_export.json", mime="application/json")

st.sidebar.markdown("---")
st.sidebar.write("Prototype notes:")
st.sidebar.write("- All AI behaviors are mocked for prototype demo. Replace mocks with real ML/vision models and agents for production.")
st.sidebar.write("- For deployment: upload to Streamlit Cloud and deploy the repository.")
