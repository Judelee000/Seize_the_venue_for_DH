DH Sports Facility Auto-Booking Script (Sniper) An automated Python script designed to quickly and efficiently book sports facilities at DH. Powered by Playwright for high-speed web automation and ddddocr for AI-based CAPTCHA solving, this script includes a precise "sniping" mechanism that waits for the exact opening time before firing the request.

Features Automated Workflow: Handles login, navigation, venue selection, and date input automatically. Precision Sniping: Built-in timer loop waits for the exact opening time with millisecond precision before querying the database. AI CAPTCHA Auto-Solver: Uses ddddocr to recognize CAPTCHA images automatically. Robust Retry Mechanism: Automatically filters out Chinese misinterpretations and confusing characters (like 0 and O). If a CAPTCHA is unreadable or doesn't meet the strict 5-character length, it clicks "Refresh" and retries instantly. Centralized Configuration: All variables are grouped at the top of the script for easy modification.

Prerequisites Make sure you have Python 3.8+ installed on your system. You will need to install the following Python packages: playwright, ddddocr. Install the Chromium browser binary required by Playwright by running: playwright install chromium. pip install playwright ddddocr, playwright install chromium

Configuration Before running the script, open the Python file and modify the Settings Area at the very top of the code to match your needs. By default, the script is in Testing Mode. The final submission button is commented out to prevent accidental bookings. When you are ready to actually book a facility, scroll to the bottom of the script and remove the '#' from the last line.

Usage

Open your terminal or command prompt.
Navigate to the directory where your script is located.
Start the script a few minutes before the target opening time.
Run the script: python your_script_name.py. The browser will open (Headless mode is disabled for visibility), prepare everything, and wait in a standby loop. Once the system clock hits the OPEN_TIME, it will instantly fire the query, solve the CAPTCHA, and submit your application.
Disclaimer This script is for educational and testing purposes only. Please use it responsibly. Do not abuse the university's booking system or overload their servers with excessive requests.