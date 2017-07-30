FROM python:3.6
RUN mkdir /web
WORKDIR /root
COPY models libs static templates views wechat *.py requirements.txt local_settings.py.tmpl /web/
RUN pip install -r /web/requirements.txt
WORKDIR /web
EXPOSE 8100