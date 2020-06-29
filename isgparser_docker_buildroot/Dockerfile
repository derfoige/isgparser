FROM python:3
ADD selib /data/selib
ADD isgparser.py /data
ADD config.cfg /data
ADD requirements.txt /data
WORKDIR /data
RUN pip install -r requirements.txt
CMD python /data/isgparser.py
