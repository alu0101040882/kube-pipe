FROM python:3.9.7
WORKDIR /usr/src/app

COPY . .

RUN mv load.py app.py
RUN pip3 install -r requirements.txt

CMD ["python3", "app.py"]
