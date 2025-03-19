import numpy as np  # For numerical operations and array handling
from sklearn.ensemble import \
    RandomForestClassifier  # ML algorithm for classification
from sklearn.preprocessing import \
    LabelEncoder  # For encoding categorical labels


class ThreatDetector:
    def __init__(self):
        """Initialize the threat detection model"""
        self.model = RandomForestClassifier()  # Random forest classifier for threat detection
        self.label_encoder = LabelEncoder()  # Encoder to convert text labels to numbers for ML
        self.trained = False  # Flag to track if the model has been trained
    
    def identify_attack_type(self, data, port):
        """Classify attack type based on payload content and port"""
        data = data.lower()  # Convert to lowercase for case-insensitive matching
        
        # Dictionary mapping attack signatures to their respective attack types
        attack_signatures = {
            'sql_injection': ['select', 'union', 'insert', 'delete', 'update', 'drop', 'grant all privileges'],  # SQL command patterns
            'brute_force': ['password', 'login', 'user', 'pass'],  # Authentication attempt patterns
            'directory_traversal': ['../','..\\', '/..','\..'],  # Path traversal patterns
            'command_injection': ['exec', '/bin/sh', '/bin/bash', 'cmd.exe'],  # Shell command patterns
            'credential_stuffing': ['admin:admin', 'root:root', 'admin123', 'password123'],  # Common credential patterns
            'reconnaissance': ['version()', 'show databases', 'phpinfo', '/wp-admin']  # Information gathering patterns
        }
        
        # Map ports to service types for initial attack classification
        port_services = {
            21: 'FTP Attack',  # File Transfer Protocol
            22: 'SSH Attack',  # Secure Shell
            23: 'Telnet Attack',  # Telnet protocol
            80: 'Web Attack',  # HTTP web service
            443: 'Web Attack (HTTPS)',  # HTTPS secure web service
            3306: 'Database Attack'  # MySQL database
        }
        
        # Get the base attack type based on the targeted port
        base_type = port_services.get(port, 'Unknown Attack')
        
        # Check for specific attack patterns in the payload
        attack_types = []
        for attack_type, signatures in attack_signatures.items():
            if any(sig in data for sig in signatures):
                attack_types.append(attack_type)
        
        # Return just the base type if no specific patterns found
        if not attack_types:
            return base_type
        
        # Map technical attack types to more human-readable descriptions
        attack_type_mapping = {
            'sql_injection': 'SQL Injection',
            'brute_force': 'Brute Force',
            'directory_traversal': 'Directory Traversal',
            'command_injection': 'Command Injection',
            'credential_stuffing': 'Credential Stuffing',
            'reconnaissance': 'Reconnaissance'
        }
        
        # Convert technical terms to readable forms
        readable_types = [attack_type_mapping.get(t, t) for t in attack_types]
        # Return combined attack classification
        return f"{base_type}: {' + '.join(readable_types)}"
    
    def extract_features(self, attack_data):
        """Convert attack data into numerical features for ML model"""
        # Extract time-based features (hour of attack)
        hour = int(attack_data['timestamp'].split()[1].split(':')[0])
        
        # Port number as a feature
        port = attack_data['port']
        
        # Extract text-based features from payload
        data = attack_data['data'].lower()
        has_password = 1 if 'password' in data else 0  # Flag for password-related content
        has_admin = 1 if 'admin' in data else 0  # Flag for admin-related content
        has_root = 1 if 'root' in data else 0  # Flag for root access attempts
        data_length = len(data)  # Length of payload can indicate complexity
        
        # Combine all features into a single array for the ML model
        features = [
            hour,
            port,
            has_password,
            has_admin,
            has_root,
            data_length
        ]
        
        return np.array(features)  # Return as numpy array
    
    def train(self, attack_data):
        """Train the ML model with attack data"""
        if len(attack_data) > 10:  # Only train when we have enough data
            X = []  # Feature vectors
            y = []  # Target labels (threat levels)
            
            # Process each attack to extract features and labels
            for attack in attack_data:
                features = self.extract_features(attack)
                X.append(features)
                y.append(attack.get('threat_level', 'low'))  # Default to 'low' if not specified
            
            X = np.array(X)  # Convert feature list to numpy array
            self.label_encoder.fit(y)  # Train label encoder on threat levels
            y_encoded = self.label_encoder.transform(y)  # Convert text labels to numbers
            
            # Train the random forest model
            self.model.fit(X, y_encoded)
            self.trained = True  # Mark model as trained
    
    def predict(self, attack_data):
        """Predict threat level for a new attack"""
        # First classify the attack type based on content
        attack_type = self.identify_attack_type(attack_data['data'], attack_data['port'])
        attack_data['attack_type'] = attack_type  # Add classification to attack data
        
        if not self.trained:
            # If model isn't trained yet, use rule-based prediction
            data = attack_data['data'].lower()
            if 'root' in data or 'admin' in data:
                return 'high'  # Admin/root access attempts are high risk
            elif 'password' in data:
                return 'medium'  # Password attempts are medium risk
            return 'low'  # Default to low risk
        
        # Use trained ML model for prediction
        features = self.extract_features(attack_data)
        features = features.reshape(1, -1)  # Reshape for single sample prediction
        prediction = self.model.predict(features)  # Get numeric prediction
        return self.label_encoder.inverse_transform(prediction)[0]  # Convert back to text label


