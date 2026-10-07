# Student Information System

A command line application to manage student records. It stores data in JSON and uses a modular, cloud-ready structure.

## Features
- Add, view (all or by ID), update, and delete students
- Fields: ID (auto), name, email, course, year level, GPA, created and updated timestamps
- JSON data storage with safe writes
- Search by name, course, email, or ID (menu option 7)
- CSV export (menu option 8)
- Input validation
- External configuration file
- File logging and error handling
- Unit tests

## Project structure
```
student-info-system/
├── src/
│   ├── models/student.py
│   ├── services/student_service.py
│   ├── utils/ (config, logger, validators)
│   └── main.py
├── data/students.json
├── config/config.json
├── logs/
├── tests/
├── README.md
├── requirements.txt
└── .gitignore
```

## Requirements
Python 3.8 or newer. No external packages.

## Run
```
git clone https://github.com/<your-username>/student-info-system.git
cd student-info-system
python src/main.py
```

## Test
```
python -m unittest discover tests
```

## Configuration
Edit `config/config.json`.

| Key | Purpose |
|-----|---------|
| data_file | Path to the JSON data file |
| export_dir | Folder for CSV exports |
| log_file | Path to the log file |
| log_level | DEBUG, INFO, WARNING, or ERROR |

## Design notes
- Models, services, and utilities are separate modules.
- The service writes to a temp file, then replaces the data file. This prevents corrupt data on a crash.
- A corrupt data file is backed up to `students.json.bak` and the app starts clean.

## Git workflow
- `main` holds stable code.
- Each feature uses a branch named `feature/<name>`.
- Changes merge through pull requests.


## Usage
Run python src/main.py and choose a menu option from 1 to 8.
