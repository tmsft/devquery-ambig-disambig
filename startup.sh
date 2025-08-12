#!/bin/bash
apt-get update
apt-get install -y wget gnupg unzip

# Install Chrome
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list
apt-get update && apt-get install -y google-chrome-stable

# Install ChromeDriver
CHROME_VERSION=$(google-chrome --version | grep -oP "\d+\.\d+\.\d+")
DRIVER_VERSION=$(wget -qO- "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_${CHROME_VERSION%%.*}")
wget -O /tmp/chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/${DRIVER_VERSION}/linux64/chromedriver-linux64.zip"
unzip /tmp/chromedriver.zip -d /usr/local/bin/

# Run your Streamlit app
exec streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
