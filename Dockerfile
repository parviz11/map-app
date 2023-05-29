FROM python:3.11

ENV DASH_DEBUG_MODE False
RUN apt-get update
RUN apt-get install nano
 
RUN mkdir wd
WORKDIR wd
COPY requirements.txt .
RUN pip3 install -r requirements.txt
  
COPY . .
  
 CMD [ "gunicorn", "--workers=5", "--threads=1", "-b 0.0.0.0:80", "app:server"]
