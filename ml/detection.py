import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder


class ThreatDetector:
    def __init__(self):
        self.model = RandomForestClassifier()
        self.label_encoder = LabelEncoder()
        self.trained = False
    
    def identify_attack_type(self, data, port):
        data = data.lower()
        
        # Dictionary of attack signatures and their types
        attack_signatures = {
            'sql_injection': ['select', 'union', 'insert', 'delete', 'update', 'drop', 'grant all privileges'],
            'brute_force': ['password', 'login', 'user', 'pass'],
            'directory_traversal': ['../','..\\', '/..','\..'],
            'command_injection': ['exec', '/bin/sh', '/bin/bash', 'cmd.exe'],
            'credential_stuffing': ['admin:admin', 'root:root', 'admin123', 'password123'],
            'reconnaissance': ['version()', 'show databases', 'phpinfo', '/wp-admin']
        }
        
        # Port-based initial classification
        port_services = {
            21: 'FTP Attack',
            22: 'SSH Attack',
            23: 'Telnet Attack',
            80: 'Web Attack',
            443: 'Web Attack (HTTPS)',
            3306: 'Database Attack'
        }
        
        base_type = port_services.get(port, 'Unknown Attack')
        
        # Look for specific attack patterns
        attack_types = []
        for attack_type, signatures in attack_signatures.items():
            if any(sig in data for sig in signatures):
                attack_types.append(attack_type)
        
        if not attack_types:
            return base_type
        
        # Convert technical attack types to more readable forms
        attack_type_mapping = {
            'sql_injection': 'SQL Injection',
            'brute_force': 'Brute Force',
            'directory_traversal': 'Directory Traversal',
            'command_injection': 'Command Injection',
            'credential_stuffing': 'Credential Stuffing',
            'reconnaissance': 'Reconnaissance'
        }
        
        readable_types = [attack_type_mapping.get(t, t) for t in attack_types]
        return f"{base_type}: {' + '.join(readable_types)}"
    
    def extract_features(self, attack_data):
        # Extract time-based features
        hour = int(attack_data['timestamp'].split()[1].split(':')[0])
        
        # Port-based features
        port = attack_data['port']
        
        # Data-based features
        data = attack_data['data'].lower()
        has_password = 1 if 'password' in data else 0
        has_admin = 1 if 'admin' in data else 0
        has_root = 1 if 'root' in data else 0
        data_length = len(data)
        
        # Combine all features into a single array
        features = [
            hour,
            port,
            has_password,
            has_admin,
            has_root,
            data_length
        ]
        
        return np.array(features)
    
    def train(self, attack_data):
        if len(attack_data) > 10:  # Only train when we have enough data
            X = []
            y = []
            
            for attack in attack_data:
                features = self.extract_features(attack)
                X.append(features)
                y.append(attack.get('threat_level', 'low'))
            
            X = np.array(X)  # Convert to numpy array
            self.label_encoder.fit(y)
            y_encoded = self.label_encoder.transform(y)
            
            self.model.fit(X, y_encoded)
            self.trained = True
    
    def predict(self, attack_data):
        # First identify the attack type
        attack_type = self.identify_attack_type(attack_data['data'], attack_data['port'])
        attack_data['attack_type'] = attack_type
        
        if not self.trained:
            # If not trained, use rule-based prediction
            data = attack_data['data'].lower()
            if 'root' in data or 'admin' in data:
                return 'high'
            elif 'password' in data:
                return 'medium'
            return 'low'
        
        features = self.extract_features(attack_data)
        features = features.reshape(1, -1)  # Reshape for single prediction
        prediction = self.model.predict(features)
        return self.label_encoder.inverse_transform(prediction)[0]


