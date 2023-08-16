FROM python:3.9
ADD main.py .
COPY .env .
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["python", "-u", "./main.py"]
