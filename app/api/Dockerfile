FROM python:3.6.7

ENV FLASK_APP main.py

ENV FLASK_DEBUG=1

RUN mkdir /app

WORKDIR /app

VOLUME /app

#COPY main.py ./api.py

RUN pip3 install requests flask pymongo

ADD . /app

EXPOSE 5000
CMD [ "python" , "-m", "flask", "run", "--host", "0.0.0.0"]
#CMD FLASK_DEBUG=1 python -m flask run --host=0.0.0.0