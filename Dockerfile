# If deploying to ARM architecture, use:
# FROM yosukeasanoflagellin/uwsgi-nginx-flask:python3.8.7
# RUN apt-get update && apt-get install -y bash nano

FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine
RUN apk --update add bash nano
ENV STATIC_URL /static
ENV STATIC_PATH /app/timelnr/static
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
