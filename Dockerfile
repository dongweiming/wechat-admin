FROM python:3.6
RUN mkdir /web
WORKDIR /web
COPY models libs static templates uploads wechat-plugins views wechat *.py requirements.txt /web/
RUN pip install -r requirements.txt
EXPOSE 8100