import time
import json
import requests
import random
from datetime import datetime

#  CONFIGURATION 
LOG_FILE = "server_logs.txt"
WEBHOOK_URL = "https://n8napp.digitlab.app/webhook-test/9c3d94f1-76f9-4663-8044-70d53d47ed78"  # URL N8N
SIMULATION_MODE = True  # Mettre à False pour surveiller un vrai fichier

class NetworkSentinel:
    """
    Agent de supervision capable de détecter des anomalies dans les logs
    et de déclencher une alerte via Webhook (N8N).
    """

    def __init__(self, log_path, webhook_url):
        self.log_path = log_path
        self.webhook_url = webhook_url
        self.is_running = False

    def generate_fake_log(self):
        """Simule l'activité réseau pour la démonstration"""
        status_list = ["INFO", "WARNING", "SUCCESS", "CRITICAL"]
        messages = [
            "Connection stable",
            "Packet loss detected",
            "Latency high",
            "Database connection failed",
            "Firewall update complete"
        ]
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = random.choice(status_list)
        msg = random.choice(messages)
        
        # On force une erreur CRITICAL de temps en temps
        if random.random() < 0.2: 
            status = "CRITICAL"
            msg = "CORE_SWITCH_FAILURE: Port 8080 Unreachable"

        log_entry = f"[{timestamp}] [{status}] {msg}\n"
        
        with open(self.log_path, "a") as f:
            f.write(log_entry)
        
        return log_entry.strip()

    def send_alert(self, error_msg):
        """Envoie l'alerte à l'agent N8N"""
        payload = {
            "agent": "Network_Sentinel_V1",
            "alert_level": "HIGH",
            "timestamp": datetime.now().isoformat(),
            "error_message": error_msg,
            "recommended_action": "Check NOC Dashboard immediately"
        }
        
        try:
            # En mode démo sans URL valide, on affiche juste l'envoi
            if "ton-webhook" in self.webhook_url:
                print(f" [SIMULATION ENVOI] Alerte envoyée à N8N : {error_msg}")
            else:
                response = requests.post(self.webhook_url, json=payload)
                if response.status_code == 200:
                    print(f" Alerte reçue par N8N")
        except Exception as e:
            print(f" Erreur de connexion au Webhook: {e}")

    def start_monitoring(self):
        """Boucle principale de surveillance"""
        print(f" Démarrage de la surveillance sur {self.log_path}...")
        self.is_running = True
        
        # On se place à la fin du fichier pour ne lire que les nouveaux logs
        with open(self.log_path, "r") as f:
            f.seek(0, 2)
            
            while self.is_running:
                line = f.readline()
                
                if not line:
                    # Si pas de nouvelle ligne, on simule une activité
                    if SIMULATION_MODE:
                        new_log = self.generate_fake_log()
                        print(f"Log généré: {new_log}")
                        # Si le log généré est critique, on le traite au prochain tour de boucle
                        if "CRITICAL" in new_log:
                            # On force la lecture immédiate pour la démo
                            line = new_log
                        else:
                            time.sleep(1)
                            continue
                    else:
                        time.sleep(0.5)
                        continue

                if "CRITICAL" in line or "ERROR" in line:
                    print(f" ANOMALIE DÉTECTÉE : {line.strip()}")
                    self.send_alert(line.strip())

if __name__ == "__main__":
    # Instanciation de l'agent
    sentinel = NetworkSentinel(LOG_FILE, WEBHOOK_URL)
    
    # Création du fichier si inexistant
    with open(LOG_FILE, "w") as f:
        f.write("[INFO] System Start\n")
        
    try:
        sentinel.start_monitoring()
    except KeyboardInterrupt:
        print("\n Arrêt de la surveillance.")
