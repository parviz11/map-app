FROM python:3.11

ENV DASH_DEBUG_MODE False
COPY . .
WORKDIR /app
RUN set -ex & \
    pip install -r requirements.txt
EXPOSE 8050
CMD ["gunicorn", "-b", "0.0.0.0:8050", "--reload", "app:server"]
