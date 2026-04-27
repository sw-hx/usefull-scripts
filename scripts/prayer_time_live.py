
import json
import os
import time
import urllib.request
from datetime import datetime

# =========================
# Configuration
# =========================

CITY = "Amman"
COUNTRY = "Jordan"
METHOD = 1

PRAYERS_TO_SHOW = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]

# ANSI Colors
GREEN = "\033[0;32m"
BLUE = "\033[1;97m"
YELLOW = "\033[1;33m"
RED = "\033[0;31m"
CYAN = "\033[0;36m"
BOLD = "\033[1m"
NC = "\033[0m"
BRIGHT_BLUE = "\033[1;34m"


# =========================
# Helpers
# =========================

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def fetch_prayer_times():
    today_api = datetime.now().strftime("%d-%m-%Y")
    today_iso = datetime.now().strftime("%Y-%m-%d")

    url = (
        f"https://api.aladhan.com/v1/timingsByCity/"
        f"{today_api}?city={CITY}&country={COUNTRY}&method={METHOD}"
    )

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
    except Exception as e:
        print(f"{RED}Error fetching data: {e}{NC}")
        exit(1)

    timings = data["data"]["timings"]

    prayers = {}
    for prayer in PRAYERS_TO_SHOW:
        # Sometimes API returns: "04:15 (+03)"
        clean_time = timings[prayer].split()[0]
        prayers[prayer] = clean_time

    return prayers, today_iso


def prayer_to_epoch(date_str, prayer_time):
    dt = datetime.strptime(
        f"{date_str} {prayer_time}",
        "%Y-%m-%d %H:%M"
    )
    return int(dt.timestamp())


def format_remaining(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60

    return f"{GREEN}{hours:02d}h {minutes:02d}m {secs:02d}s{NC}"


# =========================
# Main
# =========================

def main():
    prayers, last_fetch_date = fetch_prayer_times()

    while True:
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Refresh only when new day starts
        if current_date != last_fetch_date:
            prayers, last_fetch_date = fetch_prayer_times()

        now = int(time.time())

        clear_screen()

        print(f"{CYAN}================================================{NC}")
        print(
            f" 🕌  {BOLD}{YELLOW}PRAYER TIMES - "
            f"{CITY.upper()}, {COUNTRY.upper()}{NC}  🕌"
        )
        print(
            f"     {BLUE}Date: {current_date} | "
            f"Time: {datetime.now().strftime('%H:%M:%S')}{NC}"
        )
        print(f"{CYAN}================================================{NC}")

        print(
            f"{BOLD}{BRIGHT_BLUE}"
            f"{'PRAYER':<12} | {'TIME':<8} | {'REMAINING':<20}"
            f"{NC}"
        )
        print(f"{CYAN}-------------|----------|------------------------{NC}")

        next_prayer_found = False

        for prayer, prayer_time in prayers.items():
            prayer_epoch = prayer_to_epoch(current_date, prayer_time)

            if prayer_epoch > now and not next_prayer_found:
                # Next upcoming prayer
                diff = prayer_epoch - now
                remaining = format_remaining(diff)
                prayer_name = f"{YELLOW}{prayer:<11}{NC}"
                next_prayer_found = True

            elif prayer_epoch <= now:
                # Passed
                remaining = f"{RED}-- Passed --{NC}"
                prayer_name = f"{prayer:<11}"

            else:
                # Future but not next
                remaining = "Upcoming"
                prayer_name = f"{prayer:<11}"

            print(
                f" {prayer_name:<12} | "
                f"{prayer_time:<8} | "
                f"{remaining}"
            )

        print(f"{CYAN}================================================{NC}")
        print("Press CTRL+C to exit.")

        time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Exiting...{NC}")

