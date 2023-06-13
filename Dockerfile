# Base image
FROM python:3.10.10

# Set working directory
WORKDIR /app

# Copy files
COPY main.py /app
COPY requirements.txt /app
COPY source /app/source
COPY .env /app
# Install dependencies
RUN pip install -r requirements.txt

# Run the application
EXPOSE 8005
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8005"]