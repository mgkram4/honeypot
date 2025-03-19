let threatChart = null;

function updateDashboard() {
    fetch('http://localhost:5000/attacks')
        .then(response => response.json())
        .then(attacks => {
            updateAttackAnalysis(attacks);
        })
        .catch(error => console.error('Error:', error));
}

function updateAttackAnalysis(attacks) {
    const recentAttacks = document.getElementById('recent-attacks');
    const latest = attacks.slice(-10).reverse(); // Show last 10 attacks
    
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
    `).join('');
}

function simulateAttack() {
    const portSelect = document.getElementById('sim-port');
    const intensitySelect = document.getElementById('sim-intensity');
    const statusDiv = document.getElementById('sim-status');
    const simButton = document.getElementById('sim-button');
    
    const port = portSelect.value;
    const intensity = intensitySelect.value;
    
    simButton.disabled = true;
    statusDiv.textContent = `Simulating ${intensity} attack on port ${port}...`;
    
    fetch('http://localhost:5000/simulate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            port: parseInt(port),
            intensity: intensity
        })
    })
    .then(response => response.json())
    .then(data => {
        statusDiv.textContent = data.message;
        updateDashboard();
    })
    .catch(error => {
        console.error('Error:', error);
        statusDiv.textContent = `Error simulating attack: ${error}`;
    })
    .finally(() => {
        simButton.disabled = false;
    });
}

function resetSimulation() {
    const statusDiv = document.getElementById('sim-status');
    const resetButton = document.getElementById('reset-button');
    
    resetButton.disabled = true;
    statusDiv.textContent = 'Resetting simulation...';
    
    fetch('http://localhost:5000/reset', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        statusDiv.textContent = data.message;
        updateDashboard();
    })
    .catch(error => {
        console.error('Error:', error);
        statusDiv.textContent = `Error resetting simulation: ${error}`;
    })
    .finally(() => {
        resetButton.disabled = false;
    });
}

// Initialize when the page loads
document.addEventListener('DOMContentLoaded', function() {
    const simButton = document.getElementById('sim-button');
    const resetButton = document.getElementById('reset-button');
    
    if (simButton) {
        simButton.addEventListener('click', simulateAttack);
    }
    
    if (resetButton) {
        resetButton.addEventListener('click', resetSimulation);
    }
    
    // Initial update
    updateDashboard();
});

// Update dashboard every 5 seconds
setInterval(updateDashboard, 5000);
