# Use a slim version of Python to minimize image size
FROM python:3.9-slim

# Install system dependencies and tools required to build nsjail
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    libprotobuf-dev \
    protobuf-compiler \
    libnl-route-3-dev \
    libcap-dev \
    pkg-config \
    flex \
    bison \
    && rm -rf /var/lib/apt/lists/*

# Clone and build nsjail from the source
RUN git clone https://github.com/google/nsjail.git /tmp/nsjail && \
    cd /tmp/nsjail && \
    make && \
    cp nsjail /usr/local/bin/ && \
    rm -rf /tmp/nsjail

# Set the working directory
WORKDIR /app

# Copy the project files into the container, including tests
COPY app/ /app

# Install Python dependencies from requirements.txt
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the required port for Flask
EXPOSE 8080

# Run the Flask application
CMD ["python", "main.py"]
