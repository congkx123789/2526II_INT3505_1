// Sync Stage with Server
async function fetchStage() {
    const res = await fetch('/api/admin/get-stage');
    const data = await res.json();
    updateUI(data.stage);
}

function updateUI(stage) {
    document.querySelectorAll('.stage-btn').forEach(b => {
        b.classList.toggle('active', b.dataset.stage === stage);
    });
}

document.querySelectorAll('.stage-btn').forEach(btn => {
    btn.onclick = async () => {
        const stage = btn.dataset.stage;
        await fetch('/api/admin/set-stage', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({stage})
        });
        updateUI(stage);
    };
});

async function sendV1() {
    const body = {
        amount: parseFloat(document.getElementById('v1_amount').value),
        order_id: document.getElementById('v1_order').value
    };
    executeRequest('/api/v1/payments', body);
}

async function sendV2() {
    const body = {
        amount: parseFloat(document.getElementById('v2_amount').value),
        currency: document.getElementById('v2_currency').value,
        payment_method: document.getElementById('v2_method').value,
        order_id: 'ORD_V2_MOCK'
    };
    executeRequest('/api/v2/payments', body);
}

async function executeRequest(url, body) {
    try {
        const startTime = performance.now();
        const res = await fetch(url, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(body)
        });
        const endTime = performance.now();

        // 1. Status
        const statusPill = `<span class="status-pill status-${res.status.toString()[0]}xx">${res.status} ${res.statusText}</span>`;
        document.getElementById('statusWrap').innerHTML = statusPill;

        // 2. Headers
        let headerContent = '';
        res.headers.forEach((v, k) => {
            const isLifecycle = ['deprecation', 'sunset', 'warning', 'link'].includes(k.toLowerCase());
            const className = isLifecycle ? 'header-highlight' : '';
            headerContent += `<div class="header-item"><span class="header-key">${k}</span>: <span class="header-val ${className}">${v}</span></div>`;
        });
        document.getElementById('headers').innerHTML = headerContent || '// No headers';

        // 3. Body
        const data = await res.text();
        try {
            document.getElementById('body').textContent = JSON.stringify(JSON.parse(data), null, 2);
        } catch {
            document.getElementById('body').textContent = data;
        }
    } catch (e) {
        document.getElementById('body').textContent = 'Error: ' + e.message;
    }
}

fetchStage();
