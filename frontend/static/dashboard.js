// /frontend/static/dashboard.js
function runScan() {
    fetch('/api/scan', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                document.getElementById('result').innerText = `❌ Error: ${data.error}`;
                document.getElementById('scan-status').innerText = '';
            } else {
                document.getElementById('result').innerText = JSON.stringify(data.result, null, 2);
                document.getElementById('scan-status').innerText = data.status || 'Scan completed successfully.';
            }
        })
        .catch(err => {
            alert("Error: " + err);
            document.getElementById('scan-status').innerText = '';
        });
}
