// Global variable to store the threat chart instance
let threatChart = null;

/**
 * Fetch attack data from the server and update the dashboard UI
 */
function updateDashboard() {
    // Make API request to get all attacks from the server
    fetch('http://localhost:5000/attacks')
        .then(response => response.json())  // Parse JSON response
        .then(attacks => {
            // Update the dashboard UI with attack data
            updateAttackAnalysis(attacks);
        })
        .catch(error => console.error('Error:', error));  // Log any errors
}

/**
 * Update the attack analysis section of the dashboard with recent attacks
 * @param {Array} attacks - List of attack data from the server
 */
function updateAttackAnalysis(attacks) {
    // Get the container element for recent attacks
    const recentAttacks = document.getElementById('recent-attacks');
    // Take the last 10 attacks and reverse for chronological display (newest first)
    const latest = attacks.slice(-10).reverse(); 
    
    // Generate HTML for each attack and insert into the container
    recentAttacks.innerHTML = latest.map(attack => `
        <div class="attack-entry ${attack.threat_level}">
            <div class="attack-time">${attack.timestamp}</div>
            <div class="attack-info">
                <h3>${attack.attack_type}</h3>
                <div class="attack-meta">
                    <span><strong>IP:</strong> ${attack.ip}</span>
                    <span><strong>Port:</strong> ${attack.port}</span>
                    <span><strong>Threat Level:</strong> ${attack.threat_level}</span>
                </div>
                <div class="attack-payload">
                    <strong>Payload:</strong><br>
                    ${attack.data}
                </div>
            </div>
        </div>
    `).join('');  // Join all HTML strings together
}

/**
 * Initiate an attack simulation by sending parameters to the server
 */
function simulateAttack() {
    // Get references to UI elements
    const portSelect = document.getElementById('sim-port');
    const intensitySelect = document.getElementById('sim-intensity');
    const statusDiv = document.getElementById('sim-status');
    const simButton = document.getElementById('sim-button');
    
    // Get selected values from UI
    const port = portSelect.value;
    const intensity = intensitySelect.value;
    
    // Disable button during API call to prevent multiple requests
    simButton.disabled = true;
    // Update status message
    statusDiv.textContent = `Simulating ${intensity} attack on port ${port}...`;
    
    // Send simulation request to server
    fetch('http://localhost:5000/simulate', {
        method: 'POST',  // HTTP POST method
        headers: {
            'Content-Type': 'application/json',  // Send JSON data
        },
        body: JSON.stringify({  // Convert data to JSON string
            port: parseInt(port),  // Convert port to number
            intensity: intensity
        })
    })
    .then(response => response.json())  // Parse JSON response
    .then(data => {
        // Display success message
        statusDiv.textContent = data.message;
        // Refresh dashboard with new attack data
        updateDashboard();
    })
    .catch(error => {
        // Handle and display errors
        console.error('Error:', error);
        statusDiv.textContent = `Error simulating attack: ${error}`;
    })
    .finally(() => {
        // Re-enable the button regardless of success/failure
        simButton.disabled = false;
    });
}

/**
 * Reset the simulation by clearing all attack data
 */
function resetSimulation() {
    // Get references to UI elements
    const statusDiv = document.getElementById('sim-status');
    const resetButton = document.getElementById('reset-button');
    
    // Disable button during API call
    resetButton.disabled = true;
    // Update status message
    statusDiv.textContent = 'Resetting simulation...';
    
    // Send reset request to server
    fetch('http://localhost:5000/reset', {
        method: 'POST'  // HTTP POST method
    })
    .then(response => response.json())  // Parse JSON response
    .then(data => {
        // Display success message
        statusDiv.textContent = data.message;
        // Refresh dashboard with cleared data
        updateDashboard();
    })
    .catch(error => {
        // Handle and display errors
        console.error('Error:', error);
        statusDiv.textContent = `Error resetting simulation: ${error}`;
    })
    .finally(() => {
        // Re-enable the button regardless of success/failure
        resetButton.disabled = false;
    });
}

// Initialize event listeners when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get button references
    const simButton = document.getElementById('sim-button');
    const resetButton = document.getElementById('reset-button');
    
    // Set up click handler for simulation button
    if (simButton) {
        simButton.addEventListener('click', simulateAttack);
    }
    
    // Set up click handler for reset button
    if (resetButton) {
        resetButton.addEventListener('click', resetSimulation);
    }
    
    // Initial dashboard update when page loads
    updateDashboard();
});

// Set up automatic refresh of dashboard every 5 seconds
setInterval(updateDashboard, 5000);
