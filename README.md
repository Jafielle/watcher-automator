# watcher-automator
Personal task and reminder automator. Reads tasks from Google Sheets and syncs them with Google Calendar. Ongoing personal automation project for reminders and study management.

# Watcher Automator

**Personal Task & Reminder Automator**  
Reads tasks from Google Sheets and automatically syncs them with Google Calendar.

## 🔧 What it does

Watcher Automator is a personal automation tool that:

- Reads tasks from a Google Sheets document.
- Checks if the task is scheduled for today and hasn't been sent yet.
- If it's time, creates a Google Calendar event automatically.
- Updates the sheet to mark the task as "sent".

## 📚 Main Scripts

- `watcher.py`: Checks the sheet and triggers reminders.
- `sync_sheet_to_calendar.py`: Creates calendar events from sheet data.
- `calendar_client.py`: Handles authentication and calendar connection.
- `insert_event_test.py`: Simple script to test calendar integration.

## 🔐 Requirements

- Google Cloud project with Calendar and Sheets API enabled.
- A Service Account key (JSON format).
- Permissions to access the target Google Sheet and Calendar.

## 🕒 Timezone

All scheduling is set to `America/Bogota`.

## 🚧 Status

Actively maintained as part of a long-term automation project.

---

✨ Made with care by Abril Gómez
