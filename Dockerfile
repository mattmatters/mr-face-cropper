FROM python:3.6.3
WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y build-essential \
  cmake \
  pkg-config \
  libx11-dev \
  libatlas-base-dev \
  libgtk-3-dev \
  libboost-python-dev \
  libopencv-dev \
  python-opencv

RUN wget https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_alt2.xml

# Pip stuff
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD FLASK_APP=app.py FLASK_DEBUG=1 python app.py
