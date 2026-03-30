import attractions5a from '../data/attractions.json' with { type: 'json' };
import natgeoWorld from '../data/natgeo_world.json' with { type: 'json' };
import natgeoChina from '../data/natgeo_china.json' with { type: 'json' };
import natgeo225 from '../data/natgeo_225.json' with { type: 'json' };

const attractions = [...attractions5a, ...natgeoWorld, ...natgeoChina, ...natgeo225];

// Initialize State
const state = {
    visited: new Set(JSON.parse(localStorage.getItem('visited_5a')) || []),
    activeFilter: 'all',
    activeCategory: 'all',
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
    categoryBtns: document.querySelectorAll('.category-btn'),
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
// Toast Notification Helper
const showToast = (message, type = 'success') => {
    const container = document.getElementById('toast-container');
    if (!container) return;
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = message;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.add('hiding');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
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
    // 1. Filter attractions based on active category
    let currentAttractions = attractions;
    if (state.activeCategory !== 'all') {
        currentAttractions = attractions.filter(attr => (attr.category || '5A') === state.activeCategory);
    }
    
    // 2. Count visited within that category subset
    let visitedCount = 0;
    currentAttractions.forEach(attr => {
        if (state.visited.has(attr.id)) {
            visitedCount++;
        }
    });

    const total = currentAttractions.length;
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

        // 2. Filter by Category
        let categoryMatch = true;
        const attrCategory = attr.category || '5A';
        
        if (state.activeCategory !== 'all') {
            categoryMatch = attrCategory === state.activeCategory;
        }

        // 3. Filter by Search
        let searchMatch = true;
        if (state.searchTerm) {
            const term = state.searchTerm.toLowerCase();
            const nameMatch = attr.name.toLowerCase().includes(term);
            const locMatch = attr.location.toLowerCase().includes(term);
            searchMatch = nameMatch || locMatch;
        }

        return statusMatch && categoryMatch && searchMatch;
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

            let badgeLabel = '';
            if (attr.category === 'natgeo_world') badgeLabel = 'WORLD 50';
            else if (attr.category === 'natgeo_china') badgeLabel = 'CHINA 50';
            else if (attr.category === 'natgeo_225') badgeLabel = 'DESTINATIONS 225';
            
            const badgeIndicator = badgeLabel ? `<span class="category-badge badge-natgeo" style="margin-right: 6px;">${badgeLabel}</span>` : '';
            
            const idDisplay = typeof attr.id === 'number' ? `<span class="preview-id">${String(attr.id).padStart(2, '0')}</span>` : '';
            const tooltipContent = `
                <div class="preview-card">
                    ${idDisplay}
                    ${badgeIndicator}
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
        
        const idDisplay = typeof attr.id === 'number' ? `<span style="font-family: var(--font-mono); color: var(--text-secondary); margin-right: 8px;">${String(attr.id).padStart(2, '0')}</span>` : '';
        const el = document.createElement('div');
        el.className = `list-item ${isVisited ? 'visited' : ''}`;
        el.innerHTML = `
            <div class="item-info">
                <span class="item-name">
                    ${idDisplay}${attr.name}
                </span>
                <div class="item-location">${attr.location}</div>
            </div>
            <div class="item-status"></div>
        `;
        el.onclick = () => {
            map.flyTo([attr.lat, attr.lng], 10, { duration: 1.5 });
            
            // Allow user to see map flight by keeping modal closed from list, 
            // but highlight tooltip to identify the spot
            if (elements.modal.open) {
                elements.modal.close();
            }
            if (markers[attr.id]) {
                setTimeout(() => {
                    markers[attr.id].openTooltip();
                }, 100);
            }
        };
        elements.list.appendChild(el);
    });
};

// =============================================
// IMAGE UTILITIES
// =============================================

// Deterministic color index from attraction name
const hashString = (str) => {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
        hash = ((hash << 5) - hash) + str.charCodeAt(i);
        hash |= 0;
    }
    return Math.abs(hash);
};

const PLACEHOLDER_PALETTES = [
    { from: '#0d1117', to: '#161b22', accent: '#30363d', text: '#388bfd' },  // blue
    { from: '#0f0e17', to: '#1a1828', accent: '#2d2b45', text: '#a855f7' },  // purple
    { from: '#0d1a0e', to: '#1a281c', accent: '#243524', text: '#10b981' },  // emerald
    { from: '#1a0d0d', to: '#281515', accent: '#3d2020', text: '#ef4444' },  // red
    { from: '#1a130d', to: '#281d12', accent: '#3d2e1a', text: '#f59e0b' },  // amber
    { from: '#0d1a1a', to: '#122828', accent: '#1a3d3d', text: '#06b6d4' },  // cyan
    { from: '#171017', to: '#261a26', accent: '#3a2a3a', text: '#ec4899' },  // pink
    { from: '#0a0f1a', to: '#0f1728', accent: '#1a2540', text: '#6366f1' },  // indigo
];

const generatePlaceholderSVG = (attr) => {
    const p = PLACEHOLDER_PALETTES[hashString(attr.name) % PLACEHOLDER_PALETTES.length];
    const province = (attr.location || '').split('·')[0].split(' ')[0];
    const name = attr.name.length > 10 ? attr.name.substring(0, 10) + '…' : attr.name;

    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="${p.from}"/>
      <stop offset="100%" stop-color="${p.to}"/>
    </linearGradient>
    <linearGradient id="line" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="${p.text}" stop-opacity="0"/>
      <stop offset="50%" stop-color="${p.text}" stop-opacity="0.7"/>
      <stop offset="100%" stop-color="${p.text}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect width="800" height="600" fill="url(#bg)"/>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="${p.accent}" stroke-width="0.8"/>
  </pattern>
  <rect width="800" height="600" fill="url(#grid)" opacity="0.5"/>
  <circle cx="400" cy="300" r="200" fill="none" stroke="${p.text}" stroke-width="0.5" opacity="0.12"/>
  <circle cx="400" cy="300" r="150" fill="none" stroke="${p.text}" stroke-width="0.5" opacity="0.08"/>
  <line x1="40" y1="40" x2="88" y2="40" stroke="${p.text}" stroke-width="1.5" opacity="0.35"/>
  <line x1="40" y1="40" x2="40" y2="88" stroke="${p.text}" stroke-width="1.5" opacity="0.35"/>
  <line x1="760" y1="40" x2="712" y2="40" stroke="${p.text}" stroke-width="1.5" opacity="0.35"/>
  <line x1="760" y1="40" x2="760" y2="88" stroke="${p.text}" stroke-width="1.5" opacity="0.35"/>
  <line x1="40" y1="560" x2="88" y2="560" stroke="${p.text}" stroke-width="1.5" opacity="0.35"/>
  <line x1="40" y1="560" x2="40" y2="512" stroke="${p.text}" stroke-width="1.5" opacity="0.35"/>
  <line x1="760" y1="560" x2="712" y2="560" stroke="${p.text}" stroke-width="1.5" opacity="0.35"/>
  <line x1="760" y1="560" x2="760" y2="512" stroke="${p.text}" stroke-width="1.5" opacity="0.35"/>
  <text x="400" y="258" font-family="'JetBrains Mono',monospace" font-size="11" fill="${p.text}" text-anchor="middle" opacity="0.55" letter-spacing="5">${province}</text>
  <rect x="160" y="272" width="480" height="1" fill="url(#line)"/>
  <text x="400" y="320" font-family="'PingFang SC','Noto Serif SC',serif" font-size="30" fill="#ffffff" text-anchor="middle" font-weight="600" opacity="0.88">${name}</text>
  <rect x="160" y="335" width="480" height="1" fill="url(#line)" opacity="0.4"/>
  <text x="400" y="362" font-family="'JetBrains Mono',monospace" font-size="9" fill="${p.text}" text-anchor="middle" opacity="0.35" letter-spacing="3">PHOTO UNAVAILABLE</text>
</svg>`;
    return 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(svg);
};

// ---- Image Cache (localStorage) ----
const IMAGE_CACHE_KEY = 'china5a_img_cache_v1';
let imageCache = {};
try {
    imageCache = JSON.parse(localStorage.getItem(IMAGE_CACHE_KEY) || '{}');
} catch (_) { imageCache = {}; }

const saveImageCache = () => {
    try {
        localStorage.setItem(IMAGE_CACHE_KEY, JSON.stringify(imageCache));
    } catch (e) {
        // Storage full — wipe and start fresh
        localStorage.removeItem(IMAGE_CACHE_KEY);
        imageCache = {};
    }
};

// ---- Wikipedia search with smart suffix stripping ----
const STRIP_SUFFIXES = [
    '文化旅游景区', '生态文化旅游区', '旅游风景区', '旅游景区', '旅游区',
    '风景名胜区', '风景区', '景观', '景区', '公园', '博物院', '博物馆',
    '纪念馆', '遗址', '游览区', '观光区'
];

const getSearchTerms = (name) => {
    const base = name.split(',')[0].trim();
    const terms = [base];
    for (const suffix of STRIP_SUFFIXES) {
        if (base.endsWith(suffix)) {
            const stripped = base.slice(0, -suffix.length);
            if (stripped.length >= 2) terms.push(stripped);
            break;
        }
    }
    return [...new Set(terms)];
};

const fetchWikiImageUrl = async (searchTerm) => {
    const tryWiki = async (lang) => {
        const url = `https://${lang}.wikipedia.org/w/api.php?action=query&titles=${encodeURIComponent(searchTerm)}&prop=pageimages&format=json&pithumbsize=800&origin=*`;
        const res = await fetch(url);
        const data = await res.json();
        const pages = data?.query?.pages;
        if (pages) {
            const page = pages[Object.keys(pages)[0]];
            if (page && page.thumbnail) return page.thumbnail.source;
        }
        return null;
    };
    return (await tryWiki('zh')) || (await tryWiki('en'));
};

// Modal Logic
const openModal = (attr) => {
    state.activeId = attr.id;

    // Reset handlers
    elements.modalImg.onerror = null;
    elements.modalImg.onload = null;
    elements.modalImg.classList.remove('img-loading', 'img-revealing');

    const cacheKey = String(attr.id);
    const isPlaceholder = !attr.image || attr.image.includes('placehold.co');

    if (!isPlaceholder) {
        // --- Has a pre-set real image URL ---
        elements.modalImg.src = attr.image;
        elements.modalImg.onerror = () => {
            elements.modalImg.onerror = null;
            elements.modalImg.src = generatePlaceholderSVG(attr);
        };
    } else if (imageCache[cacheKey]) {
        // --- Cache hit: use stored wiki URL immediately ---
        elements.modalImg.src = imageCache[cacheKey];
        elements.modalImg.onerror = () => {
            // Cached URL went stale
            elements.modalImg.onerror = null;
            delete imageCache[cacheKey];
            saveImageCache();
            elements.modalImg.src = generatePlaceholderSVG(attr);
        };
    } else {
        // --- No image & no cache: show SVG art instantly, fetch wiki in background ---
        elements.modalImg.src = generatePlaceholderSVG(attr);

        const searchTerms = getSearchTerms(attr.name);
        (async () => {
            for (const term of searchTerms) {
                try {
                    const imgUrl = await fetchWikiImageUrl(term);
                    if (imgUrl) {
                        // Only update if user hasn't moved to another attraction
                        if (state.activeId !== attr.id) return;
                        elements.modalImg.classList.add('img-revealing');
                        elements.modalImg.src = imgUrl;
                        elements.modalImg.onload = () => {
                            elements.modalImg.classList.remove('img-revealing');
                        };
                        // Persist to cache
                        imageCache[cacheKey] = imgUrl;
                        saveImageCache();
                        return;
                    }
                } catch (_) { /* network error, try next term */ }
            }
            // All terms exhausted — SVG placeholder stays, no further action
        })();
    }

    elements.modalId.textContent = typeof attr.id === 'number' ? String(attr.id).padStart(2, '0') : '';
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

// Close modal when clicking outside of it (on the backdrop)
elements.modal.addEventListener('click', (e) => {
    if (e.target === elements.modal) {
        elements.modal.close();
    }
});

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
                showToast(`SUCCESSFULLY IMPORTED DATA! TOTAL VISITED: ${state.visited.size}`, 'success');
            } else {
                showToast('INVALID DATA FORMAT: MISSING "VISITED" ARRAY.', 'error');
            }
        } catch (err) {
            console.error(err);
            showToast('ERROR PARSING JSON FILE.', 'error');
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

if (elements.categoryBtns) {
    elements.categoryBtns.forEach(btn => {
        btn.onclick = (e) => {
            elements.categoryBtns.forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            state.activeCategory = e.target.dataset.category;
            renderList();
            updateMarkers();
            updateStats();
        };
    });
}

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
