import gradio as gr
import json
import os
import time
from datetime import datetime

DB_FILE = "database.json"

def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({"requests": {}}, f)
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=4)

# Client submission
def submit_request(client_name, group_name, group_link):
    if not client_name or not group_name or not group_link:
        return "All fields are required", gr.update(visible=False)

    db = load_db()
    req_id = str(int(time.time()))

    db["requests"][req_id] = {
        "client_name": client_name,
        "group_name": group_name,
        "group_link": group_link,
        "numbers": "",
        "status": "pending",
        "time": str(datetime.now())
    }
    save_db(db)

    return (
        f"Submission received.\nYour Request ID: {req_id}\nPlease wait…",
        gr.update(visible=True)
    )

# Client check status
def check_numbers(req_id):
    if not req_id:
        return "Enter your Request ID"

    db = load_db()
    if req_id not in db["requests"]:
        return "Invalid Request ID"

    req = db["requests"][req_id]

    if req["status"] == "pending":
        return "⏳ Extracting numbers… Please wait."

    return req["numbers"]

# Admin list requests
def list_requests():
    db = load_db()
    items = []

    for req_id, data in db["requests"].items():
        items.append(
            f"{req_id} | {data['client_name']} | {data['group_name']} | Status: {data['status']}"
        )

    return "\n".join(items) if items else "No requests available."

# Admin load request
def load_request(req_id):
    db = load_db()

    if req_id not in db["requests"]:
        return "Invalid ID", ""

    return "Request Loaded", db["requests"][req_id].get("numbers", "")

# Admin save numbers
def save_numbers(req_id, numbers):
    db = load_db()

    if req_id not in db["requests"]:
        return "Invalid Request ID"

    db["requests"][req_id]["numbers"] = numbers
    db["requests"][req_id]["status"] = "completed"
    save_db(db)

    return "Numbers updated successfully."

# Build UI
def build_interface():
    with gr.Blocks() as app:

        # Custom styling
        gr.HTML("""
        <style>
        body {
            background: linear-gradient(135deg, #4b0082, #6a0dad);
            color: white;
            font-family: 'Inter', sans-serif;
        }
        .gr-button {
            border-radius: 8px !important;
            padding: 10px 18px !important;
            font-size: 16px !important;
        }
        </style>
        """)

        url_params = gr.JSON(visible=False)

        def route(params):
            return "admin" if params and params.get("admin") == "1" else "client"

        current_page = gr.State("client")

        url_params.change(route, url_params, current_page)

        # Client UI
        with gr.Group(visible=True) as client_ui:
            gr.HTML("<h1 style='text-align:center;'>WhatsApp Group Number Extractor</h1>")
            gr.HTML("<p style='text-align:center;'>Invite this number first: <b>01707137376</b></p>")

            client_name = gr.Textbox(label="Your Name")
            group_name = gr.Textbox(label="Group Name")
            group_link = gr.Textbox(label="Group Link")

            submit_btn = gr.Button("Submit", variant="primary")
            submit_msg = gr.Textbox(label="Status Message")
            req_box = gr.Textbox(label="Enter Request ID to Check", placeholder="Paste Request ID")
            loading_label = gr.Markdown("⏳ Waiting for extraction...", visible=False)
            check_btn = gr.Button("Check Numbers")
            output_box = gr.Textbox(label="Extracted Numbers", lines=6)

            submit_btn.click(submit_request, [client_name, group_name, group_link], [submit_msg, loading_label])
            check_btn.click(check_numbers, req_box, output_box)

        # Admin UI
        with gr.Group(visible=False) as admin_ui:
            gr.HTML("<h1 style='text-align:center;'>Admin Panel</h1>")

            refresh_btn = gr.Button("Refresh Requests")
            request_list = gr.Textbox(label="All Requests", lines=10)
            refresh_btn.click(list_requests, outputs=request_list)

            req_id_admin = gr.Textbox(label="Request ID to Load")
            load_btn = gr.Button("Load")
            load_msg = gr.Textbox(label="Load Status")
            number_box = gr.Textbox(label="Paste Extracted Numbers", lines=8)
            save_btn = gr.Button("Save Numbers")
            save_status = gr.Textbox(label="Save Status")

            load_btn.click(load_request, req_id_admin, [load_msg, number_box])
            save_btn.click(save_numbers, [req_id_admin, number_box], save_status)

        # Switch UI
        def switch(page):
            return (
                gr.update(visible=page == "client"),
                gr.update(visible=page == "admin")
            )

        current_page.change(switch, current_page, [client_ui, admin_ui])

    return app


app = build_interface()
app.launch()
