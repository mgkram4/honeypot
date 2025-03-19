# Honeypot AI - Your First Cybersecurity Project

## What is a Honeypot?

A honeypot is like a trap for hackers! It's a computer system that looks real but is actually set up to detect and study hacking attempts. Think of it like leaving a jar of honey out to see what kinds of bugs you attract - but for computer attackers!

## What This Project Does

This project creates a fake computer system that:
1. Looks attractive to hackers
2. Records what the hackers try to do
3. Uses smart technology to figure out how dangerous each attack is
4. Shows you all the attacks on a cool dashboard

## Getting Started

### What You'll Need
- A computer with Python installed (version 3.6 or newer)
- Basic understanding of how to use the command line

### How to Install

1. Download this project to your computer:
   ```
   git clone https://github.com/yourusername/honeypot-ai.git
   cd honeypot-ai
   ```

2. Install the programs this project needs:
   ```
   pip install flask scikit-learn pandas flask-cors
   ```

3. Start the honeypot:
   ```
   python main.py
   ```

4. Open your web browser and go to: `http://localhost:5000`

## How to Use the Dashboard

The dashboard is your control center! Here's what you can do:

### Simulate Attacks
You can create fake attacks to see how the system works:
1. Choose a port (like SSH or HTTP)
2. Choose how strong the attack should be
3. Click "Simulate Attack" button

### Monitor Attacks
The dashboard shows you:
- Recent attacks with color coding (red = dangerous, yellow = medium, green = safe)
- Information about each attack (where it came from, what it tried to do)

### Reset Everything
If you want to start over, just click the "Reset Simulation" button.

## Understanding the Parts

### Ports
The honeypot watches these network ports:
- Port 21: FTP (for file transfers)
- Port 22: SSH (for remote control)
- Port 23: Telnet (old-school remote control)
- Port 80: HTTP (regular websites)
- Port 443: HTTPS (secure websites)
- Port 3306: MySQL (databases)

### Attack Types
The system can detect:
- SQL Injection: Trying to hack databases
- Brute Force: Trying many passwords to break in
- Directory Traversal: Trying to access files they shouldn't
- Command Injection: Trying to run commands on your computer
- Credential Stuffing: Using stolen usernames and passwords
- Reconnaissance: Just looking around to find weaknesses

### Threat Levels
Each attack gets a danger level:
- High (Red): Very dangerous attacks
- Medium (Yellow): Somewhat dangerous attacks
- Low (Green): Not very dangerous attacks

## How It Works Behind the Scenes

This project uses:
1. **Machine Learning**: The system learns over time what dangerous attacks look like
2. **Web Dashboard**: Shows you the attacks in real-time
3. **Attack Simulation**: So you can test the system safely

## Learning More

Want to learn more about cybersecurity? Check out these resources:
- [Cybersecurity Basics on Khan Academy](https://www.khanacademy.org/computing/computers-and-internet/xcae6f4a7ff015e7d:online-data-security)
- [CyberPatriot Youth Program](https://www.uscyberpatriot.org/)
- [Code.org's Cybersecurity Lessons](https://code.org/cybersecurity)

## Important Safety Note

This project is for learning only! Never use these tools to hack real systems - that's illegal and can get you in big trouble. Always practice cybersecurity ethically!

---

## Glossary of Terms

- **Honeypot**: A computer trap set to detect hackers
- **Port**: A connection point where computers talk to each other
- **SQL Injection**: A trick to hack databases using special commands
- **Brute Force**: Trying lots of passwords until one works
- **Machine Learning**: Teaching computers to learn patterns and make decisions
- **Dashboard**: A visual display that shows information
- **Simulation**: Creating fake events to test how something works