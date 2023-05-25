FROM python:3.11.3-bullseye

WORKDIR /app

COPY requirements.txt .

RUN pip install torch
RUN pip install -r requirements.txt

COPY . .

ENV STATIC_URL /static
ENV STATIC_PATH /app/static
ENV FLASK_APP /app/app.py

EXPOSE 5000
ENTRYPOINT ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]