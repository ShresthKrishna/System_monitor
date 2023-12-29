import os
import platform
from email.message import EmailMessage

import psutil
import smtplib

def send_alert(subject, body):
    sender_email = "yourmail@mail.com"  # Replace with your sender email address
    receiver_email = "something@mail.com"  # Replace with your receiver email address
    password = "yourpassword"  # Replace with your email password or an app-specific password

    # Create a message object
    message = EmailMessage()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.set_content(body)

    try:
        # Connect to the SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            # Login to the email account
            server.login(sender_email, password)
            # Send the email
            server.send_message(message)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
def monitor_server():
    cpu_threshold = 20  # in percentage
    memory_threshold = 20  # in percentage
    disk_threshold = 20  # in percentage

    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    if cpu_usage > cpu_threshold:
        send_alert('CPU Alert', f'CPU usage exceeded {cpu_threshold}% - Currently at {cpu_usage}%')

    if memory_usage > memory_threshold:
        send_alert('Memory Alert', f'Memory usage exceeded {memory_threshold}% - Currently at {memory_usage}%')

    if disk_usage > disk_threshold:
        send_alert('Disk Alert', f'Disk usage exceeded {disk_threshold}% - Currently at {disk_usage}%')

def set_autostart_instructions():
    os_name = platform.system()

    if os_name == 'Windows':
        print("For Windows: Open Task Scheduler and create a task to run this script at startup.")
    elif os_name == 'Darwin':
        print("For macOS: Create a plist file in LaunchAgents to run this script at startup.")
    elif os_name == 'Linux':
        print("For Linux: Create a systemd service to run this script at startup.")
    else:
        print("Auto-start setup instructions not available for this operating system.")

def ask_permission():
    while True:
        response = input("Do you want to start server monitoring and set up auto-start? (yes/no): ").strip().lower()
        if response == 'yes':
            return True
        elif response == 'no':
            return False
        else:
            print("Please enter 'yes' or 'no'.")

def main():
    set_autostart_instructions()

    if ask_permission():
        print("Server monitoring started. Press Ctrl+C to stop.")
        try:
            while True:
                monitor_server()
        except KeyboardInterrupt:
            print("\nMonitoring stopped.")
    else:
        print("Monitoring not started. Exiting.")

if __name__ == "__main__":
    main()
