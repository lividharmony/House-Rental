# Use the official Python base image
FROM python:3.10.7-slim

# Set the working directory
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port the app will run on
EXPOSE 8000

ENV PYTHONUNBUFFERED 1

# Run the application
CMD ["python", "bot.py", "runserver", "0.0.0.0:8000"]

