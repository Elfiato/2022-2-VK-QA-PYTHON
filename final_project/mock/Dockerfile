FROM python:3.10

ADD requirements.txt /requirements.txt
RUN pip3.10 install -r /requirements.txt

COPY code code

WORKDIR code
EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["mock.py"]
