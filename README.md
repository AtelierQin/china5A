# China 5A Attractions Map (5A足迹)

A minimalist interactive map application to visualize and track your visits to China's top-tier (5A) tourist attractions.

## Overview

This project aims to convert the text-based list of China's 5A scenic spots into an intuitive map visualization. It features a "Mission Control" aesthetic inspired by Swiss Style design, focusing on data density and clarity.

### Key Features
- **Interactive Map**: Visualize all 300+ 5A attractions on a map.
- **Progress Tracking**: Local storage-based tracking of visited locations. (Planned)
- **Data Filtering**: Filter by province or status.

## Project Structure

```
├── docs/                   # Documentation (PRD, Design System)
├── scripts/                # Python scripts for data scraping and processing
├── src/                    # Source code (assets, data)
├── index.html              # Main application entry point
├── data_5a.json            # Processed attraction data
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
