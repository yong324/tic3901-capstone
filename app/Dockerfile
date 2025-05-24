# Use an official Python image
FROM python:3.9

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the Flask app code
COPY . .

# Expose the Flask app port
EXPOSE 5000

# Set the Flask app entry point
ENV FLASK_APP=run.py

# Run the Flask app
CMD ["flask", "run","--host=0.0.0.0"]
