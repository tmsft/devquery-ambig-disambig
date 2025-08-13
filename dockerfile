FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gnupg \
    libnss3 \
    libxi6 \
    libxcursor1 \
    libxcomposite1 \
    libasound2 \
    libxdamage1 \
    libxrandr2 \
    libgbm-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && apt-get install -y google-chrome-stable

# Install matching ChromeDriver
RUN CHROMEDRIVER_VERSION=$(wget -qO- https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE) && \
    wget -O /tmp/chromedriver.zip "https://storage.googleapis.com/chrome-for-testing-public/${CHROMEDRIVER_VERSION}/linux64/chromedriver-linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver-linux64/chromedriver && \
    ln -s /usr/local/bin/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app
COPY . .

# Expose port for Streamlit
EXPOSE 8000

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8000", "--server.address=0.0.0.0"]
