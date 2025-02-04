# Gym Automatic Booking System (GABS)

## Why Did I Create GABS?

My gym allows class bookings only three days before the session starts, and with just 15 spots available, securing a place can be a frustrating experience. I found myself setting alarms three days in advance just to remind me to rush and book my slot.
Every time the alarm went off, I had to drop whatever I was doing, open the gym’s website, and quickly hit the booking button. For the most popular classes, all 15 spots would be gone in less than a minute! It felt like a race every time, and there were moments when my alarm went off while I was in the shower—you can imagine the frustration.
That’s when I came up with the idea of automating the booking process. I wanted a system that could handle it for me, running effortlessly on a cost-effective Raspberry Pi Zero W.
Now, when I’m with my gym buddies and I hear their alarms ringing for class bookings, I just smile—knowing that someone (or rather, something) is handling it for me. 😏

## Overview
Gym Automatic Booking System (GABS) is a Python-based automation tool that uses Selenium to book gym classes on the website of a popular gym in Bristol. It runs on a **Raspberry Pi Zero W** and can be scheduled using `crontab` for automatic execution.

## Features
- Automates the login process.
- Navigates to the gym's booking page.
- Finds a specific class by name and instructor.
- Books the class if available, or joins the waiting list if full.
- Logs all actions for easy debugging and tracking.

## Requirements
- **Raspberry Pi Zero W** (or another Linux-based machine)
- **Python 3**
- **Selenium**
- **Chromedriver**
- **Chromium Browser**

## Installation

1. **Install dependencies:**
   ```bash
   sudo apt update && sudo apt install -y python3 python3-pip chromium-chromedriver
   pip3 install selenium
   ```

2. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/GymAutomaticBookingSystem.git
   cd GymAutomaticBookingSystem
   ```

3. **Edit the script to include your credentials and desired class details.**

## Usage
Run the script manually using:
```bash
python3 gabs_improved.py myemail@example.com mypassword "Yoga Class" "John Doe"
```

Or automate it using `crontab`.

## Automating with Crontab
To schedule automatic execution, add the following entry to your crontab (`crontab -e`):

```bash
59 17 * * sun ~/Desktop/GymAutomaticBookingSystem/toRunOnSunday.sh >> ~/Desktop/GymAutomaticBookingSystem/GABS.log 2>&1
```

This will run the script every **Sunday at 17:59**.

### Example of `toRunOnSunday.sh`
```bash
#!/bin/bash
python3 ~/Desktop/GymAutomaticBookingSystem/gabs_improved.py ██████@gmail.com mypassword "Yoga Class" "John Doe"
```

Make sure the script is executable:
```bash
chmod +x ~/Desktop/GymAutomaticBookingSystem/toRunOnSunday.sh
```

## Logging
All logs are stored in `GABS.log` for debugging and tracking bookings.
```LOG
2025-02-02 17:59:03,844 - INFO - User ██████@gmail.com is trying to book ████████...
2025-02-02 18:00:30,503 - INFO - Found button for the day TUE, 04TH!
2025-02-02 18:00:47,300 - INFO - Found class ████████ with ████████!
2025-02-02 18:00:49,824 - INFO - Class Booked! :)
2025-02-02 18:00:50,371 - INFO - Time taken: 0:01:46
2025-02-02 18:54:04,321 - INFO - User ████████@live.it is trying to book ████████████████...
2025-02-02 18:55:30,299 - INFO - Found button for the day TUE, 04TH!
2025-02-02 18:55:50,254 - INFO - Found class ████████████████ With ████!
2025-02-02 18:55:53,529 - INFO - Class Booked! :)
2025-02-02 18:55:54,222 - INFO - Time taken: 0:01:49
```
## License
This project is licensed under the GPL-3.0 license.

---

### Notes
- Ensure the **Chromedriver** version matches your Chromium/Chrome version.
- If using a different gym website, update the script with the correct URLs and element selectors.
- Running on a Raspberry Pi Zero W may require additional optimization due to limited resources.

Happy automating! 🎉

