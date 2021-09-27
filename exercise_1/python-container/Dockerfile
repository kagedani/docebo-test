FROM python:3.8
COPY code /docebo/code
COPY requirements.txt /docebo
WORKDIR /docebo
RUN python3 -m pip install -r requirements.txt
WORKDIR /docebo/code
ENTRYPOINT ["python3", "main.py"]