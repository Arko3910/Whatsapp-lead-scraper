A fully automated workflow for receiving WhatsApp Group links, extracting phone numbers, organizing them, and delivering structured results to clients.

Overview

This system automates the entire journey from client request to final delivery of extracted WhatsApp phone numbers. It is designed to be fast, stable, scalable, and simple for operators to manage.

The workflow uses:

A custom HTML dashboard for submitting group extraction requests

Two n8n workflows:

request_extract – receives client requests and notifies the operator

receive_results – receives extracted numbers, cleans the data, stores them, and notifies the client

Everything flows smoothly through API endpoints, Google Sheets, and automated email communication.

How It Works
1. Client Submits a Request

Clients open the dashboard and enter:

Their name

WhatsApp group link

(Optional) Callback URL

(Optional) Email address

The dashboard instantly sends the data to the Request Extract Webhook.

2. Request Logging & Operator Notification

The request_extract workflow performs three automated tasks:

Logs the request to a Google Sheet for record-keeping

Sends an automated email to the operator with request details

Returns a success response to the front-end

This ensures that every request is tracked and no submission is ever missed.

3. Extraction Process (Automated Flow)

Once the operator processes the request, the extracted phone numbers are sent back to the system through the Receive Results Webhook in the following structure:

{
  "phones": ["017xxxxxxx", "88018xxxxxxx"],
  "groupLink": "https://chat.whatsapp.com/xxxx",
  "clientName": "Client Name",
  "clientEmail": "example@email.com",
  "callback": "https://client-api.com/receive"
}

4. Append to Client Sheet

The receive_results workflow:

Cleans and restructures phone numbers

Creates individual rows for each number

Automatically appends them to a client-specific Google Sheet

Ensures proper formatting and timestamp tracking

This keeps every client’s data organized, accessible, and ready to use.

5. Notify the Client Automatically

After saving the numbers, the system automatically:

Sends an email to the client informing them that the extraction is complete

If a callback URL was provided, it sends the final dataset back to the client via POST

Clients always receive real-time updates without waiting or manual follow-up.

Core Automations
✔ Automated Data Intake

Receives client submissions instantly through the dashboard → n8n webhook.

✔ Automated Storage

Every request and every extracted number is logged in Google Sheets.

✔ Automated Notifications

Both operator and client receive instant email updates.

✔ Automated Delivery

Clients can receive results through email or callback API.

Key Benefits

No manual data entry

Zero chance of losing requests

Fast processing flow

Fully trackable client records

Scalable for high-volume operations

Seamless experience for end clients

File Structure
/project
│
├── dashboard.html                 # Client-facing request dashboard
├── n8n_request_extract.json       # Workflow for intake & operator alerts
└── n8n_receive_results.json       # Workflow for processing results & client alerts

How to Deploy

Upload both JSON files to n8n

Replace:

Webhook URLs

Google Sheet IDs

Email credentials

Upload dashboard.html to your hosting (VPS / Netlify / Cloudflare / Firebase)

Replace the endpoint URL inside dashboard.html

Done — the full system runs automatically
