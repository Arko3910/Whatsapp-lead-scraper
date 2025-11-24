# admin.py
import streamlit as st
import json, os, datetime
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore

st.set_page_config(page_title="Extractor Admin", layout="centered")

# ---------- Firebase init ----------
def init_firebase():
    firebase_conf = None
    if "FIREBASE_CONFIG" in st.secrets:
        firebase_conf = st.secrets["FIREBASE_CONFIG"]
    elif os.getenv("FIREBASE_CONFIG"):
        firebase_conf = json.loads(os.getenv("FIREBASE_CONFIG"))
    else:
        st.error("FIREBASE_CONFIG not found. Add your service account JSON to Streamlit secrets (FIREBASE_CONFIG).")
        st.stop()

    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_conf)
        firebase_admin.initialize_app(cred)
    return firestore.Client()

db = init_firebase()

st.title("Operator — WhatsApp Extractor Admin")
st.markdown("You are the operator. See pending requests, scrape numbers, paste them and deliver.")

# Simple auth (optional): ask for password stored in secrets
if "ADMIN_PASSWORD" in st.secrets:
    pwd = st.text_input("Admin password", type="password")
    if pwd != st.secrets["ADMIN_PASSWORD"]:
        st.warning("Enter admin password to continue")
        st.stop()

# Show pending requests
st.subheader("Pending requests")
docs = db.collection("requests").where("status", "==", "waiting").order_by("createdAt").stream()
pending = []
for d in docs:
    rec = d.to_dict()
    rec["id"] = d.id
    pending.append(rec)

if not pending:
    st.info("No pending requests.")
else:
    for rec in pending:
        st.markdown("---")
        st.write("**Request ID:**", rec["id"])
        st.write("Client:", rec.get("clientName"))
        st.write("Group name:", rec.get("groupName"))
        st.write("Group link:", rec.get("groupLink"))
        numbers_text = st.text_area("Paste extracted numbers (one per line) for request: " + rec["id"], key=rec["id"]+"_ta")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Deliver numbers", key=rec["id"]+"_deliver"):
                # normalize
                lines = [l.strip() for l in numbers_text.splitlines() if l.strip()]
                db.collection("requests").document(rec["id"]).update({
                    "numbers": lines,
                    "status": "done",
                    "deliveredAt": datetime.datetime.utcnow().isoformat()
                })
                st.success("Delivered to client and set status=done.")
        with col2:
            if st.button("Skip / Mark failed", key=rec["id"]+"_skip"):
                db.collection("requests").document(rec["id"]).update({
                    "status": "failed",
                    "deliveredAt": datetime.datetime.utcnow().isoformat()
                })
                st.warning("Marked as failed.")

# Optional: search by request ID and view history
st.markdown("---")
st.subheader("Search request")
q = st.text_input("Enter request id")
if q:
    doc = db.collection("requests").document(q).get()
    if doc.exists:
        rec = doc.to_dict()
        st.write(rec)
    else:
        st.error("Request not found.")
