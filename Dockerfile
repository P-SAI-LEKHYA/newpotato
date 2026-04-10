FROM python:3.9-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install the required packages
# Note: we add tensorflow and pillow to requirements.txt if they aren't there, 
# but installing explicit versions is recommended.
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir tensorflow==2.15.0 pillow

# Copy the rest of the application
COPY . .

# Expose the API port
EXPOSE 8000

# Start the uvicorn server
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
