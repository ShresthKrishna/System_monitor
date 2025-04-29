# 📈 Real-Time System Resource Monitor

A lightweight Python application to monitor system resources (CPU, Memory, and Disk usage) in real-time. It sends email alerts and console warnings when usage exceeds customizable thresholds.

---

## ✨ Features

- **Real-Time Monitoring**  
  Continuously tracks CPU, Memory, and Disk usage.
- **Threshold Alerts**  
  Sends immediate **email notifications** and **console alerts** when resource usage crosses user-defined limits.
- **Customizable Settings**  
  Adjust CPU, Memory, and Disk thresholds according to your needs.
- **Cross-Platform Compatibility**  
  Works on **Windows**, **macOS**, and **Linux** systems.
- **Manual Auto-Start Guidance**  
  Provides instructions to set up auto-start manually on system boot.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/ShresthKrishna/System_monitor.git
cd System_monitor
```

---

### 2. Install Dependencies

Install the required libraries:

```bash
pip install -r requirements.txt
```

---

### 3. Configure Email Settings

Create a `config.json` file in the project directory with the following structure:

```json
{
    "sender_email": "your_email@gmail.com",
    "receiver_email": "receiver_email@gmail.com",
    "password": "your_app_password"
}
```

⚡ **Important:**  
- `sender_email`: Your Gmail account address.  
- `receiver_email`: The address where alerts should be sent.  
- `password`: **App Password** (NOT your Gmail login password).

---

### 📧 How to Create a Gmail App Password (Required)

Since Google does not allow direct login with your Gmail password for external apps, you need to create an **App Password**:

1. Go to [Google Account Settings](https://myaccount.google.com/).  
2. Navigate to **Security** → **Signing in to Google** → **App passwords**.  
3. You might have to enable **2-Step Verification** first if you haven't already.  
4. Select **App** → *Mail*, **Device** → *Other (custom name)* → Type "ResourceMonitor" → Click **Generate**.  
5. Copy the **16-character App Password** and paste it into your `config.json` under the `"password"` field.

> Without this, email alerts will not work due to Google's security settings.

---

### 4. Run the Script

```bash
python resource_monitor.py
```

- You will be prompted to customize thresholds (or press Enter to use default 80%).  
- The monitoring will start automatically and send alerts if thresholds are exceeded.

---

## 📸 Screenshot Example

| Email Alert Example |
|:-------------------:|
| ![Sample Email Alert](screenshots/sample_email_alert.png) |

---

## ⚙️ Auto-Start Setup (Manual)

After starting the script, it will print **manual setup instructions** based on your OS.

The script **does not automatically configure auto-start**, but here’s how you can do it yourself:

---

### ➡️ Linux (Create a `systemd` Service)

Create a new file:

```bash
sudo nano /etc/systemd/system/resource_monitor.service
```

Paste:

```ini
[Unit]
Description=Resource Monitor Script
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /path/to/your/project/resource_monitor.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:

```bash
sudo systemctl daemon-reload
sudo systemctl enable resource_monitor
sudo systemctl start resource_monitor
```

---

### ➡️ macOS (Create a LaunchAgent `.plist` file)

Create a file at:

```bash
~/Library/LaunchAgents/com.shresth.resource_monitor.plist
```

Paste:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.shresth.resource_monitor</string>

    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/your/project/resource_monitor.py</string>
    </array>

    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

Then load it:

```bash
launchctl load ~/Library/LaunchAgents/com.shresth.resource_monitor.plist
```

---

### ➡️ Windows (Use Task Scheduler)

Steps:

1. Open **Task Scheduler** → Create **Basic Task**.  
2. Name it: `Resource Monitor`.  
3. Trigger: **At startup**.  
4. Action: **Start a program**.  
   - Program/script: `python.exe`  
   - Add arguments: `C:\path\to\your\project\resource_monitor.py`  
5. Finish setup.

✅ Your script will now start with your computer!

---

## 📂 Project Structure

```
System_monitor/
├── README.md
├── resource_monitor.py
├── requirements.txt
├── LICENSE
├── config.json   (keep private, do not upload to GitHub)
└── screenshots/
    └── sample_email_alert.png
```

---

## 🙌 Contributing

Contributions are welcome!  
Feel free to **fork** this repository, improve it, and create a **Pull Request**.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 👨‍💻 Author

**Shresth Krishna**  
[GitHub Profile](https://github.com/ShresthKrishna)

