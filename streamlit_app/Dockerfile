FROM python:3.10

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN echo "DEBUG: Listing app contents:" && ls -l /app
RUN which uvicorn


CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
