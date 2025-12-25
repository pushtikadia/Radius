const API_URL = '/api';
let map;

// --- DASHBOARD LOGIC ---
function loadDashboard() {
    if(!navigator.geolocation) return alert("Geolocation not supported.");

    navigator.geolocation.getCurrentPosition(async (position) => {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;

        // Initialize Map
        if(!map) {
            map = L.map('map').setView([lat, lon], 13);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
        }

        // Fetch Data
        const res = await fetch(`${API_URL}/nearby?lat=${lat}&lon=${lon}`);
        const data = await res.json();
        const list = document.getElementById('feed');
        list.innerHTML = '';

        data.forEach(post => {
            // Add Marker
            const color = post.type === 'REQUEST' ? 'red' : 'green';
            L.circleMarker([post.lat, post.lon], { color: color, radius: 10 })
             .addTo(map).bindPopup(`<b>${post.type}</b><br>${post.item}`);

            // Add List Item
            list.innerHTML += `
                <div class="card">
                    <div>
                        <span class="badge ${post.type}">${post.type}</span>
                        <b>${post.item}</b>
                    </div>
                    <small>${post.distance_km} km</small>
                </div>`;
        });
    });
}

// --- MOBILE LOGIC ---
function sendPost() {
    const type = document.getElementById('type').value;
    const item = document.getElementById('item').value;
    if(!item) return alert("Please enter an item.");

    navigator.geolocation.getCurrentPosition(async (position) => {
        const payload = {
            type: type,
            item: item,
            lat: position.coords.latitude,
            lon: position.coords.longitude
        };

        try {
            await fetch(`${API_URL}/posts`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            alert("Broadcast Sent!");
            document.getElementById('item').value = ''; // Clear input
        } catch(e) {
            alert("Error sending data.");
        }
    });
}