#!/bin/bash
app="timelnr"
docker build -t ${app} .
docker run -d -p 56730:80 \
  --name=${app} \
  -v $PWD:/app ${app}