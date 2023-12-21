FROM python:3.9-slim-bullseye

# streamlit port
EXPOSE 8501

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["streamlit", "run", "App.py", "--browser.gatherUsageStats", "false"]
