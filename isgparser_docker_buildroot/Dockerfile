FROM python:3
ADD selib /data/selib
ADD isgparser.py /data
ADD config.cfg.template /data
ADD requirements.txt /data
WORKDIR /data
RUN pip install -r requirements.txt && mv config.cfg.template config.cfg
CMD python /data/isgparser.py
