// /frontend/static/dashboard.js
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('scan-form');
    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            runScan();
        });
    }
});

function runScan() {
    const targetEl = document.getElementById('target');
    const portsEl = document.getElementById('ports');
    const threadsEl = document.getElementById('threads');
    const bannerEl = document.getElementById('banner');
    const udpEl = document.getElementById('udp');

    if (!targetEl || !portsEl || !threadsEl || !bannerEl || !udpEl) {
        alert("Missing input elements in DOM!");
        return;
    }

    const target = targetEl.value;
    const ports = portsEl.value;
    const threads = parseInt(threadsEl.value);
    const banner = bannerEl.checked;
    const udp = udpEl.checked;

    document.getElementById('scan-status').innerText = '🔍 Scanning...';
    const container = document.getElementById('scan-results');
    container.innerHTML = '';

    fetch('/api/scan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target, ports, threads, banner, udp })
    })
    .then(res => res.json())
    .then(data => {
        const exportBtn = document.getElementById('export-btn');

        if (data.analysis) {
            const analysisEl = document.createElement('div');
            analysisEl.className = 'analysis';
            analysisEl.innerHTML = '<h3>🧠 扫描结果分析报告</h3><pre id="analysis-text">' + data.analysis + '</pre>';
            container.appendChild(analysisEl); // 使用container而不是未定义的 resultsEl

            exportBtn.style.display = 'inline-block';

            exportBtn.onclick = function () {
                const blob = new Blob([data.analysis], { type: 'text/plain' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = '分析报告.txt';
                a.click();
                URL.revokeObjectURL(url);
            };
        } else {
            exportBtn.style.display = 'none';
        }

        if (data.warning) {
            alert(data.warning);
        }

        if (data.error) {
            document.getElementById('scan-status').innerText = `❌ Error: ${data.error}`;
            return;
        }

        if (!data.result || data.result.length === 0) {
            document.getElementById('scan-status').innerText = 'No results found.';
            return;
        }

        const grouped = {};
        for (const entry of data.result) {
            if (!grouped[entry.ip]) grouped[entry.ip] = [];
            grouped[entry.ip].push(entry);
        }

        for (const [ip, ports] of Object.entries(grouped)) {
            const card = document.createElement('div');
            card.className = 'result-card';

            const title = document.createElement('h3');
            title.innerText = `Target IP: ${ip}`;
            card.appendChild(title);

            const table = document.createElement('table');
            table.className = 'result-table';
            table.innerHTML = `
                <thead>
                    <tr><th>Port</th><th>Status</th><th>Protocol</th><th>Service</th><th>Banner</th></tr>
                </thead>
                <tbody>
                    ${ports.map(p => `
                        <tr>
                            <td>${p.port}</td>
                            <td>${p.status}</td>
                            <td>${p.protocol}</td>
                            <td>${p.service || ''}</td>
                            <td>${p.banner || ''}</td>
                        </tr>
                    `).join('')}
                </tbody>
            `;

            card.appendChild(table);
            container.appendChild(card);
        }

        document.getElementById('scan-status').innerText = data.status || '✅ Scan completed.';
    })
    .catch(err => {
        document.getElementById('scan-status').innerText = '❌ Request failed';
        alert("Error: " + err);
    });
}
