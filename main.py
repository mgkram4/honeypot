# Import standard Python libraries
import datetime  # For timestamp creation
import json  # For working with JSON data
import os  # For file operations
import random  # For generating random values
import socket  # For network socket operations
import threading  # For concurrent processing

# Import Flask and related libraries for web application
from flask import (Flask, jsonify,  # Flask web framework components
                   render_template, request)
from flask_cors import CORS  # Cross-Origin Resource Sharing support

# Import custom modules
from attacks import simulate_attack  # Module for attack simulation
from ml.detection import ThreatDetector  # ML-based threat detection module

# Initialize Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

class HoneyPot:
    def __init__(self, host='0.0.0.0', ports=[21, 22, 23, 80, 443, 3306]):
        """Initialize the honeypot with default settings"""
        self.host = host  # IP address to bind to (0.0.0.0 means all interfaces)
        self.ports = ports  # Common ports to monitor (FTP, SSH, Telnet, HTTP, HTTPS, MySQL)
        self.attacks = []  # List to store attack information
        self.detector = ThreatDetector()  # Initialize the threat detection model
        self.load_attacks()  # Load previously recorded attacks from disk
        # Train the threat detector if we have existing attack data
        if self.attacks:
            self.detector.train(self.attacks)
    
    def load_attacks(self):
        """Load previously recorded attacks from file"""
        if os.path.exists('attacks.json'):
            with open('attacks.json', 'r') as f:
                self.attacks = json.load(f)
    
    def save_attacks(self):
        """Save current attack data to file"""
        with open('attacks.json', 'w') as f:
            json.dump(self.attacks, f)

    def add_attack(self, attack_data):
        """Process and store a new attack"""
        # Use the ML model to determine threat level
        threat_level = self.detector.predict(attack_data)
        attack_data['threat_level'] = threat_level
        
        # Add the attack to our records
        self.attacks.append(attack_data)
        # Retrain the model when we have enough data
        if len(self.attacks) > 10:  # Only train with sufficient data points
            self.detector.train(self.attacks)
        self.save_attacks()  # Save updated attack data to disk

# Define Flask route for the homepage
@app.route('/')
def index():
    """Render the main dashboard page"""
    return render_template("index.html")

# API endpoint to retrieve all attacks
@app.route('/attacks', methods=['GET'])
def get_attacks():
    """Return all recorded attacks as JSON"""
    honeypot = HoneyPot()  # Initialize honeypot to load attack data
    return jsonify(honeypot.attacks)  # Return attacks as JSON response

# API endpoint to simulate attacks
@app.route('/simulate', methods=['POST'])
def simulate():
    """Generate and record simulated attacks"""
    # Parse request parameters
    data = request.get_json()
    port = int(data.get('port', 22))  # Default to SSH if not specified
    intensity = data.get('intensity', 'medium')  # Default to medium intensity
    
    # Determine number of attacks based on intensity level
    attack_count = 1  # Default for 'low' intensity
    if intensity == 'medium':
        attack_count = 3
    elif intensity == 'high':
        attack_count = 5
    
    # Initialize honeypot
    honeypot = HoneyPot()
    
    # Generate the specified number of simulated attacks
    for _ in range(attack_count):
        # Create current timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Generate realistic attack payload based on the targeted port
        if port == 21:  # FTP
            payload = random.choice([
                "USER anonymous\r\nPASS anonymous@example.com",  # Anonymous login attempt
                "USER admin\r\nPASS admin123",  # Default credential attempt
                "USER root\r\nPASS toor",  # Root access attempt
                "SITE EXEC ../../../bin/sh"  # Command injection attempt
            ])
        elif port == 22:  # SSH
            payload = random.choice([
                "SSH-2.0-OpenSSH_7.9\r\nroot:x:0:root",  # SSH handshake with password file attempt
                "SSH-2.0-PuTTY_Release_0.70\r\nadmin:admin123",  # PuTTY client login attempt
                "SSH-2.0-JSCH-0.1.54\r\nPassword: password123",  # Java SSH client attempt
                "SSH-2.0-libssh2_1.4.3\r\nroot:password"  # Root login attempt
            ])
        elif port == 23:  # Telnet
            payload = random.choice([
                "login: admin\r\npassword: password123",  # Admin login attempt
                "login: root\r\npassword: toor",  # Root login attempt
                "admin:admin\r\nPASSWORD:admin123",  # Common credential attempt
                "root:system\r\npassword:manager"  # Legacy system credential attempt
            ])
        elif port == 80:  # HTTP
            payload = random.choice([
                "GET /wp-admin/admin-ajax.php HTTP/1.1",  # WordPress admin access attempt
                "POST /cgi-bin/../../../../bin/sh HTTP/1.1",  # Path traversal attack
                "GET /?page=../../../etc/passwd HTTP/1.1",  # LFI attempt to read password file
                "POST /phpmyadmin/scripts/setup.php HTTP/1.1"  # PHPMyAdmin vulnerability probe
            ])
        elif port == 443:  # HTTPS
            payload = random.choice([
                "POST /api/login HTTP/1.1\r\n{\"username\":\"admin\"}",  # API login attempt
                "GET /phpmyadmin/ HTTP/1.1",  # Database admin portal probe
                "GET /solr/admin/ HTTP/1.1",  # Solr admin interface probe
                "POST /wp-login.php HTTP/1.1"  # WordPress login attempt
            ])
        elif port == 3306:  # MySQL
            payload = random.choice([
                "SELECT version()",  # Version fingerprinting
                "SHOW DATABASES",  # Database enumeration attempt
                "SELECT * FROM mysql.user",  # User table access attempt
                "GRANT ALL PRIVILEGES ON *.* TO 'root'@'%'"  # Privilege escalation attempt
            ])
        else:
            payload = "Generic attack payload"  # Fallback for other ports
        
        # Create complete attack record
        attack_data = {
            'timestamp': timestamp,  # When the attack occurred
            'ip': f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}",  # Generate random source IP
            'port': port,  # Targeted port
            'data': payload  # Attack payload
        }
        
        # Record the attack in the honeypot
        honeypot.add_attack(attack_data)
    
    # Return success response with attack count
    return jsonify({"status": "success", "message": f"Simulated {attack_count} attacks on port {port}"})

# API endpoint to reset all attack data
@app.route('/reset', methods=['POST'])
def reset():
    """Clear all recorded attack data"""
    try:
        # Remove the attacks.json file if it exists
        if os.path.exists('attacks.json'):
            os.remove('attacks.json')
        return jsonify({"status": "success", "message": "Simulation reset successfully"})
    except Exception as e:
        # Return error if something goes wrong
        return jsonify({"status": "error", "message": f"Error resetting simulation: {str(e)}"}), 500

# Run the application if this script is executed directly
if __name__ == "__main__":
    app.run(debug=True, port=5000)  # Start Flask server in debug mode on port 5000
