# ✈️ Flight Deals Alert System

A Python automation project that monitors flight prices from San José (SJO) to multiple destinations and automatically notifies users via SMS and email when a deal is found.

## How It Works

1. Pulls destination cities and their lowest known prices from a Google Sheet (via Sheety API)
2. Searches for the cheapest direct flights using SerpAPI (Google Flights engine)
3. If no direct flights are found, automatically falls back to indirect flights
4. If a cheaper price is found, it updates the Google Sheet with the new lowest price
5. Sends an SMS alert via Twilio and an email alert to all registered users

## Tech Stack

- **Python** — core logic
- **SerpAPI** — Google Flights search engine
- **Sheety** — Google Sheets as a database (destinations + user emails)
- **Twilio** — SMS notifications
- **smtplib** — email notifications
- **requests-cache** — caches API responses for 1 hour
- **python-dotenv** — manages environment variables

## Project Structure

\`\`\`
├── main.py                  # Orchestrates the full workflow
├── flight_search.py         # Queries SerpAPI for flights
├── flight_data.py           # Parses and finds the cheapest flight
├── data_manager.py          # Reads/writes to Google Sheets via Sheety
├── notification_manager.py  # Sends SMS (Twilio) and email alerts
\`\`\`

## Setup

1. Clone the repo
2. Install dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`
3. Create a \`.env\` file in the root folder:
   \`\`\`
   SHEETY_ENDPOINT=
   SHEETY_ENDPOINT_USERS=
   SHEETY_AUTHORIZATION=
   SERPAPI_API_KEY=
   SERPAPI_ENDPOINT=
   TWILIO_SID=
   TWILIO_AUTH_TOKEN=
   TWILIO_VIRTUAL_NUMBER=
   TWILIO_VERIFIED_NUMBER=
   EMAIL_PROVIDER_SMTP_ADDRESS=
   MY_EMAIL=
   MY_EMAIL_PASSWORD=
   \`\`\`
4. Run:
   \`\`\`bash
   python main.py
   \`\`\`
