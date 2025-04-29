"""
System Resource Monitor
Author: Shresth Krishna
Description: Monitors CPU, Memory, and Disk usage. Sends email and console alerts when thresholds are exceeded.
"""

import os
import platform
import psutil
import smtplib
import time
import json
from email.message import EmailMessage
from colorama import Fore, Style

# ---------------------------- CONFIGURATIONS ------------------------------- #
CPU_THRESHOLD = 80  # Default CPU usage threshold (%)
MEMORY_THRESHOLD = 80  # Default Memory usage threshold (%)
DISK_THRESHOLD = 80  # Default Disk usage threshold (%)
CHECK_INTERVAL = 5  # Seconds between checks

# Email setup (loaded from config.json)
sender_email = ""
receiver_email = ""
password = ""

# ---------------------------- EMAIL ALERT FUNCTION ------------------------------- #
def send_alert(subject, body):
    """
    Sends an email alert with the given subject and body.
    """
    global sender_email, receiver_email, password

    message = EmailMessage()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.set_content(body)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(message)
        print(Fore.GREEN + "[INFO] Email sent successfully!" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[ERROR] Failed to send email: {e}" + Style.RESET_ALL)

# ---------------------------- LOAD EMAIL CONFIG ------------------------------- #
def load_email_credentials():
    """
    Loads sender, receiver, and password from config.json
    """
    try:
        with open("config.json", "r") as file:
            config = json.load(file)
        return config["sender_email"], config["receiver_email"], config["password"]
    except Exception as e:
        print(Fore.RED + f"[ERROR] Failed to load email credentials: {e}" + Style.RESET_ALL)
        exit(1)

# ---------------------------- MONITOR FUNCTION ------------------------------- #
def monitor_server():
    """
    Monitors CPU, Memory, and Disk usage and triggers alerts if thresholds are exceeded.
    """
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
    except Exception as e:
        print(Fore.RED + f"[ERROR] Failed to read system resource usage: {e}" + Style.RESET_ALL)
        return

    if cpu_usage > CPU_THRESHOLD:
        alert_message = f"CPU usage exceeded {CPU_THRESHOLD}% - Currently at {cpu_usage}%"
        print(Fore.RED + "[ALERT] " + alert_message + Style.RESET_ALL)
        send_alert('CPU Alert', alert_message)

    if memory_usage > MEMORY_THRESHOLD:
        alert_message = f"Memory usage exceeded {MEMORY_THRESHOLD}% - Currently at {memory_usage}%"
        print(Fore.RED + "[ALERT] " + alert_message + Style.RESET_ALL)
        send_alert('Memory Alert', alert_message)

    if disk_usage > DISK_THRESHOLD:
        alert_message = f"Disk usage exceeded {DISK_THRESHOLD}% - Currently at {disk_usage}%"
        print(Fore.RED + "[ALERT] " + alert_message + Style.RESET_ALL)
        send_alert('Disk Alert', alert_message)

# ---------------------------- AUTO-START INSTRUCTIONS ------------------------------- #
def set_autostart_instructions():
    """
    Prints OS-specific instructions to set up the script to run at startup.
    """
    os_name = platform.system()

    print(Fore.CYAN + "\nAuto-start Setup Instructions:" + Style.RESET_ALL)
    if os_name == 'Windows':
        print("- For Windows: Use Task Scheduler to run this script at startup.")
    elif os_name == 'Darwin':
        print("- For macOS: Create a LaunchAgents plist file.")
    elif os_name == 'Linux':
        print("- For Linux: Create a systemd service.")
    else:
        print("- OS not recognized for auto-start instructions.")

# ---------------------------- ASK PERMISSION FUNCTION ------------------------------- #
def ask_permission():
    """
    Asks the user if they want to start monitoring.
    """
    while True:
        response = input("\nDo you want to start system monitoring? (yes/no): ").strip().lower()
        if response == 'yes':
            return True
        elif response == 'no':
            return False
        else:
            print("Please enter 'yes' or 'no'.")

# ---------------------------- CUSTOMIZE THRESHOLDS FUNCTION ------------------------------- #
def get_threshold(prompt, default):
    """
    Asks the user to enter a custom threshold or keeps the default.
    """
    try:
        value = input(f"{prompt} (Press Enter to keep default {default}%): ").strip()
        return int(value) if value else default
    except ValueError:
        print("Invalid input. Keeping default.")
        return default

# ---------------------------- MAIN FUNCTION ------------------------------- #
def main():
    """
    Main function to set up and start the monitoring process.
    """
    global CPU_THRESHOLD, MEMORY_THRESHOLD, DISK_THRESHOLD
    global sender_email, receiver_email, password

    print(Fore.CYAN + "\nSystem Resource Monitor Started." + Style.RESET_ALL)

    # Email setup
    sender_email, receiver_email, password = load_email_credentials()

    # Set thresholds
    CPU_THRESHOLD = get_threshold("Set CPU usage threshold", CPU_THRESHOLD)
    MEMORY_THRESHOLD = get_threshold("Set Memory usage threshold", MEMORY_THRESHOLD)
    DISK_THRESHOLD = get_threshold("Set Disk usage threshold", DISK_THRESHOLD)

    # Auto-start setup instructions
    set_autostart_instructions()

    if ask_permission():
        print(Fore.GREEN + "\nMonitoring started. Press Ctrl+C to stop.\n" + Style.RESET_ALL)
        try:
            while True:
                monitor_server()
                time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\n\nMonitoring stopped manually." + Style.RESET_ALL)
    else:
        print(Fore.YELLOW + "\nMonitoring not started. Exiting." + Style.RESET_ALL)

# ---------------------------- RUN SCRIPT ------------------------------- #
if __name__ == "__main__":
    main()
