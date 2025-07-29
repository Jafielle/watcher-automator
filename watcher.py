import datetime
import pytz
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- AUTORIZACIÓN ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("watcherreminderbot-021b9e58a2fe.json", scope)
client = gspread.authorize(creds)

# --- ACCEDER A LA HOJA ---
spreadsheet = client.open("WatcherTasks")
worksheet = spreadsheet.sheet1

# --- CONFIGURAR ZONA HORARIA LOCAL ---
zona_colombia = pytz.timezone("America/Bogota")
ahora_local = datetime.datetime.now(zona_colombia)
hoy = ahora_local.date().strftime('%Y-%m-%d')
hora_actual = ahora_local.time()

print(f"📅 Hoy es: {hoy}, hora actual (Bogotá): {hora_actual}")
tareas = worksheet.get_all_records()

# --- REVISAR TAREAS ---
for i, tarea in enumerate(tareas, start=2):  # Empieza desde fila 2 (por encabezados)
    fecha = tarea['Fecha']
    hora = tarea['Hora']
    enviar = tarea['Enviar?'].strip().lower()
    enviada = tarea['Enviada?'].strip()

    print(f"\n🔍 Revisando fila {i}: {tarea}")

    if fecha == hoy and enviar == "si" and enviada == "":
        try:
            hora_tarea = datetime.datetime.strptime(hora, "%H:%M").time()
        except ValueError:
            print(f"⛔ Error en la hora: {hora} (fila {i})")
            continue

        if hora_actual >= hora_tarea:
            print(f"🔔 ¡Recordatorio! {tarea['Tarea']} programada para las {hora}")
            worksheet.update_cell(i, 5, "sí")  # Columna E = 5
        else:
            print(f"⏳ Aún no es hora de: {tarea['Tarea']} a las {hora}")
    else:
        print(f"❌ No cumple condiciones: Fecha={fecha}, Enviar={enviar}, Enviada={enviada}")
