import os
import time
import subprocess
import psutil

# Configurazione dei microservizi
MICROSERVICES = [
    {"name": "domain_prediction_service", "port": 5002, "path": "server/microservices"},
    {"name": "task_prediction_service", "port": 5003, "path": "server/microservices"},
    {"name": "report_generation_service", "port": 5004, "path": "server/microservices"}
]

# Funzione per controllare se una porta è in uso
def is_service_running(port):
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == port:
            return True
    return False

# Funzione per riavviare un microservizio
def restart_service(service):
    service_name = service["name"]
    service_path = service["path"]
    service_file = os.path.join(service_path, f"{service_name}.py")

    print(f"🛑 {service_name} non è attivo. Riavvio in corso...")

    # Avvia il microservizio in background
    with open(os.path.join(service_path, f"{service_name}.log"), "w") as log_file:
        subprocess.Popen(["python", service_file], stdout=log_file, stderr=log_file)

    # Attendi e verifica di nuovo
    time.sleep(3)
    if is_service_running(service["port"]):
        print(f"✅ {service_name} riavviato con successo!")
    else:
        print(f"❌ ERRORE: {service_name} non è riuscito a riavviarsi. Controlla i log.")

# Loop di monitoraggio continuo
def monitor_services():
    while True:
        for service in MICROSERVICES:
            if not is_service_running(service["port"]):
                restart_service(service)
        time.sleep(5)  # Controlla ogni 5 secondi

if __name__ == "__main__":
    print("🚀 Monitoraggio microservizi avviato...")
    monitor_services()
