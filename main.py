import os
import re
import datetime as dt
import sys

DEBUG = False
BASE_DIR = "base/"


def list_dir():
    try:
        return [f for f in os.listdir(BASE_DIR) if f.endswith(".yaml")]
    except FileNotFoundError:
        print(f"error {BASE_DIR} not found")
        return []


def get_all_files_names():
    a = [f for f in os.listdir(BASE_DIR) if f.endswith(".yaml")]
    for c in a:
        print(f"- {c}")


def get_dates():
    all_certs = list_dir()
    results = []

    for filename in all_certs:
        match = re.search(r"\d{8}", filename)

        if match:
            date_val = match.group()
            results.append(date_val)
            if DEBUG:
                print(f"[DEBUG] Found: {date_val} in {filename}")
        else:
            if DEBUG:
                print(f"[DEBUG] Skip: {filename} (date not found)")

    return results


def create_list_of_expired_certs():
    expired_certs = get_dates()
    valid_dates = []

    for x in expired_certs:
        try:
            d = dt.datetime.strptime(x, "%Y%m%d").date()
            valid_dates.append(d)
        except ValueError:
            try:
                d = dt.datetime.strptime(x, "%Y%d%m").date()
                valid_dates.append(d)
            except ValueError:
                print(f"String'{x}' not valid date")

    return valid_dates


def check_if_certificate_expired_to_now():
    certificates_dates = create_list_of_expired_certs()
    today = dt.date.today()
    for cert_date in certificates_dates:
        if cert_date < today:
            print("exprired")
        else:
            print("not expired")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "get_all":
            all_dates = get_all_files_names()
            print(all_dates)

        elif command == "check":
            check_if_certificate_expired_to_now()

        else:
            print(f"Unknown command: {command}")
            print("Available: get_all, check")
    else:
        print("Use: python3 check_cert.py [get_all | check]")
