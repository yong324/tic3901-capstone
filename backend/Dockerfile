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

# Run the Flask app
CMD ["flask", "run","--host=0.0.0.0"]
