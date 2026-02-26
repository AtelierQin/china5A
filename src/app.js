import attractions from './attractions.json' with { type: 'json' };

// Initialize State
const state = {
    visited: new Set(JSON.parse(localStorage.getItem('visited_5a')) || []),
    activeFilter: 'all',
    activeId: null,
    searchTerm: ''
};

// DOM Elements
const elements = {
    map: document.getElementById('map'),
    list: document.getElementById('attraction-list'),
    exploredCount: document.getElementById('explored-count'),
    progressPercent: document.getElementById('progress-percent'),
    modal: document.getElementById('detail-modal'),
    closeModal: document.getElementById('close-modal'),
    filterBtns: document.querySelectorAll('.filter-btn'),
    searchInput: document.getElementById('search-input'),
    // Modal Elements
    modalImg: document.getElementById('modal-img'),
    modalId: document.getElementById('modal-id'),
    modalTitle: document.getElementById('modal-title'),
    modalLocation: document.getElementById('modal-location'),
    modalDesc: document.getElementById('modal-desc'),
    markBtn: document.getElementById('mark-visited-btn'),
    // Data Elements
    exportBtn: document.getElementById('export-btn'),
    importBtn: document.getElementById('import-btn'),
    importInput: document.getElementById('import-input')
};

// Map Initialization
const map = L.map('map', {
    zoomControl: false,
    attributionControl: false,
    zoomSnap: 0.5
}).setView([35.8617, 104.1954], 4.5); // Center of China

L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 20
}).addTo(map);

// Add custom zoom control
L.control.zoom({
    position: 'bottomright'
}).addTo(map);

const markers = {};

// Helpers
const updateStats = () => {
    const visitedCount = state.visited.size;
    const total = attractions.length;
    const percent = total > 0 ? Math.round((visitedCount / total) * 100) : 0;

    elements.exploredCount.textContent = String(visitedCount).padStart(2, '0');
    document.getElementById('total-count').textContent = total;
    elements.progressPercent.textContent = `${percent}%`;
};

const saveState = () => {
    localStorage.setItem('visited_5a', JSON.stringify([...state.visited]));
    updateStats();
    renderList();
    updateMarkers();
};

// Filter Helper
const getFilteredAttractions = () => {
    return attractions.filter(attr => {
        // 1. Filter by Status
        const isVisited = state.visited.has(attr.id);
        let statusMatch = true;
        if (state.activeFilter === 'visited') statusMatch = isVisited;
        if (state.activeFilter === 'unvisited') statusMatch = !isVisited;

        // 2. Filter by Search
        let searchMatch = true;
        if (state.searchTerm) {
            const term = state.searchTerm.toLowerCase();
            const nameMatch = attr.name.toLowerCase().includes(term);
            const locMatch = attr.location.toLowerCase().includes(term);
            searchMatch = nameMatch || locMatch;
        }

        return statusMatch && searchMatch;
    });
};

// Render Functions
const createMarkerIcon = (isVisited) => {
    return L.divIcon({
        className: 'custom-marker',
        html: `<div class="marker-pin ${isVisited ? 'visited' : 'unvisited'}"></div>`,
        iconSize: [16, 16],
        iconAnchor: [8, 8]
    });
};

const updateMarkers = () => {
    const filteredList = getFilteredAttractions();
    const filteredIds = new Set(filteredList.map(a => a.id));

    attractions.forEach(attr => {
        if (markers[attr.id]) {
            const isVisited = state.visited.has(attr.id);
            const isVisible = filteredIds.has(attr.id);

            if (isVisible) {
                markers[attr.id].addTo(map);
                markers[attr.id].setIcon(createMarkerIcon(isVisited));
            } else {
                map.removeLayer(markers[attr.id]);
            }
        }
    });
};

const initMarkers = () => {
    attractions.forEach(attr => {
        // Ensure lat/lng are valid
        if (attr.lat && attr.lng) {
            const marker = L.marker([attr.lat, attr.lng], {
                icon: createMarkerIcon(state.visited.has(attr.id))
            }).addTo(map);

            const tooltipContent = `
                <div class="preview-card">
                    <span class="preview-id">${String(attr.id).padStart(2, '0')}</span>
                    <span class="preview-name">${attr.name}</span>
                </div>
            `;

            marker.bindTooltip(tooltipContent, {
                direction: 'top',
                offset: [0, -10],
                className: 'custom-tooltip'
            });

            marker.on('click', () => openModal(attr));
            markers[attr.id] = marker;
        }
    });
    // Immediately update visibility based on initial state
    updateMarkers();
};

const renderList = () => {
    elements.list.innerHTML = '';

    const filtered = getFilteredAttractions();

    if (filtered.length === 0) {
        elements.list.innerHTML = '<div style="padding: 24px; text-align: center; color: #888;">NO RESULTS FOUND / 未找到结果</div>';
        return;
    }

    filtered.forEach(attr => {
        const isVisited = state.visited.has(attr.id);
        const el = document.createElement('div');
        el.className = `list-item ${isVisited ? 'visited' : ''}`;
        el.innerHTML = `
            <div class="item-info">
                <span class="item-name"><span style="font-family: var(--font-mono); color: var(--text-secondary); margin-right: 8px;">${String(attr.id).padStart(2, '0')}</span>${attr.name}</span>
                <span class="item-location">${attr.location}</span>
            </div>
            <div class="item-status"></div>
        `;
        el.onclick = () => {
            map.flyTo([attr.lat, attr.lng], 10);
            openModal(attr);
        };
        elements.list.appendChild(el);
    });
};

// Modal Logic
const openModal = (attr) => {
    state.activeId = attr.id;
    elements.modalImg.src = attr.image;
    elements.modalId.textContent = String(attr.id).padStart(2, '0');
    elements.modalTitle.textContent = attr.name;
    elements.modalLocation.textContent = attr.location;
    elements.modalDesc.textContent = attr.description;

    updateModalButton();
    elements.modal.showModal();
};

const updateModalButton = () => {
    const isVisited = state.visited.has(state.activeId);
    if (isVisited) {
        elements.markBtn.textContent = "VISITED / 已打卡";
        elements.markBtn.classList.add('visited');
    } else {
        elements.markBtn.textContent = "MARK AS VISITED / 打卡";
        elements.markBtn.classList.remove('visited');
    }
};

const toggleVisited = () => {
    if (state.activeId === null) return;

    if (state.visited.has(state.activeId)) {
        state.visited.delete(state.activeId);
    } else {
        state.visited.add(state.activeId);
    }

    saveState();
    updateModalButton();
};

// Event Listeners
elements.closeModal.onclick = () => elements.modal.close();
elements.markBtn.onclick = toggleVisited;

// Data Export/Import
const exportData = () => {
    const data = {
        visited: [...state.visited],
        timestamp: new Date().toISOString()
    };
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `china5a-data-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
};

const importData = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
        try {
            const data = JSON.parse(e.target.result);
            if (Array.isArray(data.visited)) {
                // Merge strategy: Union
                data.visited.forEach(id => state.visited.add(id));
                saveState();
                alert(`Successfully imported data! Total visited: ${state.visited.size}`);
            } else {
                alert('Invalid data format: Missing "visited" array.');
            }
        } catch (err) {
            console.error(err);
            alert('Error parsing JSON file.');
        }
        // Reset input
        event.target.value = '';
    };
    reader.readAsText(file);
};

elements.exportBtn.onclick = exportData;
elements.importBtn.onclick = () => elements.importInput.click();
elements.importInput.onchange = importData;

elements.filterBtns.forEach(btn => {
    btn.onclick = (e) => {
        elements.filterBtns.forEach(b => b.classList.remove('active'));
        e.target.classList.add('active');
        state.activeFilter = e.target.dataset.filter;
        renderList();
        updateMarkers();
    };
});

// Search Listener
if (elements.searchInput) {
    elements.searchInput.addEventListener('input', (e) => {
        state.searchTerm = e.target.value.trim();
        renderList();
        updateMarkers();
    });
}

// Init
initMarkers();
renderList();
updateStats();
