import datetime
import json
import os
import random
import socket
import threading

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

from attacks import simulate_attack
from ml.detection import ThreatDetector

app = Flask(__name__)
CORS(app)

class HoneyPot:
    def __init__(self, host='0.0.0.0', ports=[21, 22, 23, 80, 443, 3306]):
        self.host = host
        self.ports = ports
        self.attacks = []
        self.detector = ThreatDetector()
        self.load_attacks()
        # Train the detector with existing attacks if any
        if self.attacks:
            self.detector.train(self.attacks)
    
    def load_attacks(self):
        if os.path.exists('attacks.json'):
            with open('attacks.json', 'r') as f:
                self.attacks = json.load(f)
    
    def save_attacks(self):
        with open('attacks.json', 'w') as f:
            json.dump(self.attacks, f)

    def add_attack(self, attack_data):
        # Predict threat level using the detector
        threat_level = self.detector.predict(attack_data)
        attack_data['threat_level'] = threat_level
        
        self.attacks.append(attack_data)
        # Retrain the model with the new data
        if len(self.attacks) > 10:  # Only train when we have enough data
            self.detector.train(self.attacks)
        self.save_attacks()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/attacks', methods=['GET'])
def get_attacks():
    honeypot = HoneyPot()
    return jsonify(honeypot.attacks)

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.get_json()
    port = int(data.get('port', 22))
    intensity = data.get('intensity', 'medium')
    
    # Determine the number of attacks based on intensity
    attack_count = 1
    if intensity == 'medium':
        attack_count = 3
    elif intensity == 'high':
        attack_count = 5
    
    honeypot = HoneyPot()
    
    # Generate simulated attack data
    for _ in range(attack_count):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create fake attack data with different patterns based on port
        if port == 21:  # FTP
            payload = random.choice([
                "USER anonymous\r\nPASS anonymous@example.com",
                "USER admin\r\nPASS admin123",
                "USER root\r\nPASS toor",
                "SITE EXEC ../../../bin/sh"
            ])
        elif port == 22:  # SSH
            payload = random.choice([
                "SSH-2.0-OpenSSH_7.9\r\nroot:x:0:root",
                "SSH-2.0-PuTTY_Release_0.70\r\nadmin:admin123",
                "SSH-2.0-JSCH-0.1.54\r\nPassword: password123",
                "SSH-2.0-libssh2_1.4.3\r\nroot:password"
            ])
        elif port == 23:  # Telnet
            payload = random.choice([
                "login: admin\r\npassword: password123",
                "login: root\r\npassword: toor",
                "admin:admin\r\nPASSWORD:admin123",
                "root:system\r\npassword:manager"
            ])
        elif port == 80:  # HTTP
            payload = random.choice([
                "GET /wp-admin/admin-ajax.php HTTP/1.1",
                "POST /cgi-bin/../../../../bin/sh HTTP/1.1",
                "GET /?page=../../../etc/passwd HTTP/1.1",
                "POST /phpmyadmin/scripts/setup.php HTTP/1.1"
            ])
        elif port == 443:  # HTTPS
            payload = random.choice([
                "POST /api/login HTTP/1.1\r\n{\"username\":\"admin\"}",
                "GET /phpmyadmin/ HTTP/1.1",
                "GET /solr/admin/ HTTP/1.1",
                "POST /wp-login.php HTTP/1.1"
            ])
        elif port == 3306:  # MySQL
            payload = random.choice([
                "SELECT version()",
                "SHOW DATABASES",
                "SELECT * FROM mysql.user",
                "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%'"
            ])
        else:
            payload = "Generic attack payload"
        
        attack_data = {
            'timestamp': timestamp,
            'ip': f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}",
            'port': port,
            'data': payload
        }
        
        # Add attack and let the detector determine the threat level
        honeypot.add_attack(attack_data)
    
    return jsonify({"status": "success", "message": f"Simulated {attack_count} attacks on port {port}"})

@app.route('/reset', methods=['POST'])
def reset():
    try:
        # Remove the attacks.json file if it exists
        if os.path.exists('attacks.json'):
            os.remove('attacks.json')
        return jsonify({"status": "success", "message": "Simulation reset successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error resetting simulation: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
