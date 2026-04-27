# 🕌 Prayer Time Live CLI

A lightweight Python CLI tool that displays real-time Islamic prayer times for a selected city using the AlAdhan API.

---

## Features

- Fetches daily prayer times from API
- Live countdown to next prayer
- Auto refresh at midnight
- Terminal-based UI with colors
- No external dependencies (pure Python)

---

## Default Configuration

- City: Amman
- Country: Jordan
- Method: 1 (AlAdhan calculation method)

You can edit these values in the script:

```python
CITY = "Amman"
COUNTRY = "Jordan"
METHOD = 1
```

---

## How to Run

1. Clone repository
```bash
git clone git@github.com:sw-hx/usefull-scripts.git
cd usefull-scripts
```

2. Run script
```bash
python3 prayer_time_live.py
```

---

## Requirements
- Python 3.8+
- Internet connection (for API)
> No pip packages required.

---

## API Used
AlAdhan Prayer Times API
https://aladhan.com/prayer-times-api
