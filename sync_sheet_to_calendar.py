from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# === CONFIGURACIÓN ===
SERVICE_ACCOUNT_FILE = 'watcherreminderbot-021b9e58a2fe.json'
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '1FOvoDK8fwl-VIvW3jRwKbk4csNs26Ip8zKkHnsTEFaA'
RANGE_NAME = 'Hoja 1!A2:E'  # Suponiendo que los encabezados están en la fila 1
CALENDAR_ID = 'abrilgomez.aray@gmail.com'  # o tu ID si usas otro calendario

# === AUTENTICACIÓN ===
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

sheets_service = build('sheets', 'v4', credentials=credentials)
calendar_service = build('calendar', 'v3', credentials=credentials)

# === LEER DATOS DE SHEET ===
sheet = sheets_service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
rows = result.get('values', [])

if not rows:
    print("❌ No hay tareas.")
else:
    updates = []
    for i, row in enumerate(rows):
        if len(row) < 5:
            row += [''] * (5 - len(row))  # Completar columnas vacías

        tarea, fecha, hora, enviar, enviada = row

        if enviar.strip().lower() == 'si' and enviada.strip().lower() != 'sí':
            print(f"📆 Agendando: {tarea} - {fecha} {hora}")

            # Convertir fecha y hora a formato RFC3339
            start_datetime = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
            end_datetime = start_datetime + timedelta(minutes=30)

            event = {
                'summary': tarea,
                'start': {'dateTime': start_datetime.isoformat(), 'timeZone': 'America/Bogota'},
                'end': {'dateTime': end_datetime.isoformat(), 'timeZone': 'America/Bogota'},
            }

            event = calendar_service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
            print(f"✅ Evento creado: {event.get('htmlLink')}")

            # Actualizar celda "Enviada?" en la hoja (columna E, que es columna 5 => índice 4)
            row_index = i + 2  # porque empezamos en A2
            update_range = f'Hoja 1!E{row_index}'
            sheets_service.spreadsheets().values().update(
                spreadsheetId=SPREADSHEET_ID,
                range=update_range,
                valueInputOption='USER_ENTERED',
                body={'values': [['sí']]}
            ).execute()
