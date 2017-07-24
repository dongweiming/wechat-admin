FROM python:3.6
RUN mkdir /web
WORKDIR /web
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8100