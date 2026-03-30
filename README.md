# China 5A Attractions Map (5A足迹)

A minimalist interactive map application to visualize and track your visits to China's top-tier (5A) tourist attractions.

## Overview

This project aims to convert the text-based list of China's 5A scenic spots into an intuitive map visualization. It features a "Mission Control" aesthetic inspired by Swiss Style design, focusing on data density and clarity.

### Key Features
- **Interactive Map**: Visualize exactly 359 official 5A attractions and 3 curated National Geographic lists (World 50, China 50, Destinations 225).
- **Progress Tracking**: Local storage-based tracking dynamically computed per active category.
- **Data Export/Import**: Export and import your visited spots data as JSON.
- **Data Filtering**: Search by name/province and filter by visited status.
- **Dynamic Image Solution**: Sophisticated SVG art placeholders for missing photos, integrated with a smart Wikipedia Image API fallback and local caching.

## Project Structure

```
├── data/                   # Processed JSON core maps (attractions, natgeo lists)
├── docs/                   # Documentation (PRD, Design System)
├── scripts/                # Python scripts for data extraction and geocoding
│   └── raw_data/           # Raw JSON/CSV inputs fetched from Wikidata
├── src/                    # Frontend source code (app.js, styles.css)
├── index.html              # Main application entry point
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Getting Started

### Prerequisites

- Python 3.x (for data scripts and local server)
- A modern web browser

### Running Locally

1.  Clone the repository.
2.  Start a local web server (required for fetching JSON data locally):

    ```bash
    python3 -m http.server
    ```

3.  Open `http://localhost:8000` in your browser.

## Data Pipeline

The project includes Python scripts in the `scripts/` directory to manage data:

1.  `update_data_source.py`: Fetches latest data from Wikipedia.
2.  `merge_final_data.py`: Merges coordinate data with Wiki data.
3.  `verify_data.py`: Validates the integrity of the final JSON dataset.

## Documentation

- [Product Requirement Document (PRD)](docs/PRD.md)
- [Design System (The Atelier)](docs/design_system.md)

## License

MIT
