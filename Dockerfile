FROM python:3.10-slim

WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app/

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt && \
    pip install jupyter notebook ipykernel

# Install package in development mode
RUN pip install -e .

# Create results directory
RUN mkdir -p results

# Expose Jupyter port (optional)
EXPOSE 8888

# Default command
CMD ["python", "vqc_iris.py"]

# Alternative: Start Jupyter
# CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root", "--no-browser"]
