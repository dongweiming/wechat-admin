FROM python:3.6
RUN mkdir /web
WORKDIR /web
COPY models libs static templates uploads wechat-plugins views wechat *.py requirements.txt local_settings.py.tmpl wechat-plugins /web/
RUN pip install -r requirements.txt
EXPOSE 8100