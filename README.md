# Fold-a-saurus


# Structure
Fold-a-saurus/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── app.py            # Core GUI setup (window, panes, etc.)
│   │   ├── theme.py          # Theme and configuration handling
│   │   ├── dragdrop.py       # Drag-and-drop logic and bindings
│   │   ├── search.py
│   │   └── utils.py
│   ├── configs/
│   │   ├── profile
│   │   ├── defaults/
│   │   │   └── default_gui.json
│   │   └── profile1/
│   │       └── gui.json
│   ├── database/
│   └── assets/
│       └── icons/
│           └── delete_icon.png
├── tests/
│   └── # Placeholder for now
├── LICENSE
├── pytest.ini
└── README.md


# Requirements
pip install moviepy