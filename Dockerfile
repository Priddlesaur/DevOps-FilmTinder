FROM python:3.13-alpine

# Set the working directory to /usr/src/app
WORKDIR /usr/src/app

# Copy and install requirements
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all other necessary files
COPY . .

# Expose port 5000 for the API
EXPOSE 5000/tcp

# First run migrations then run the app
CMD alembic upgrade head && python dataset.py && uvicorn main:app --host 0.0.0.0 --port 5000
