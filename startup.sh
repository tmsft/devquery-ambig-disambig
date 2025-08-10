#!/bin/bash
apt-get update
apt-get install -y wget unzip curl

# Install Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get install -y ./google-chrome-stable_current_amd64.deb

# Install ChromeDriver
CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip
unzip chromedriver_linux64.zip -d /usr/local/bin/
chmod +x /usr/local/bin/chromedriver

# Start Streamlit app
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
