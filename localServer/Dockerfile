# Use the official Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the Python script
COPY tcpBridge.py .

# Expose the necessary ports
EXPOSE 5760 5761

# Run the Python script
CMD ["python", "tcpBridge.py"]