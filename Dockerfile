FROM python:latest

# Copy the current directory contents into the container at /app

COPY . /app

# Set the working directory to /app

WORKDIR /app

# Install dependencies

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# RUN [ "python", "-c", "import nltk; nltk.download('stopwords', download_dir='/usr/local/nltk_data')" ]

# Run app.py when the container launches

CMD ["python", "app.py"]