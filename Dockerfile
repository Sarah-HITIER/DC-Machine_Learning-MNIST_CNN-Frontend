# Use the official lightweight Python image.
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# RUN apt-get update && apt-get install build-essential -y \
#     && apt-get clean

# RUN apt-get update && apt-get install -y \
#     libgl1-mesa-glx \
#     libglib2.0-0 \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# Install the required Python packages
# RUN pip install --no-cache-dir numpy
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire frontend directory into the container
COPY . .

# Expose the port that Streamlit runs on
EXPOSE 8501

# Command to run Streamlit app
CMD ["streamlit", "run", "src/app/main.py"]
