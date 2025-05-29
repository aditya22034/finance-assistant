# FROM python:3.10-slim

# WORKDIR /app
# COPY . .

# RUN pip install -r requirements.txt

# EXPOSE 8001
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8005"]

FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN echo "DEBUG: Listing app contents:" && ls -l /app
RUN which uvicorn

# Replace 800X below with the correct port per service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8005"]
