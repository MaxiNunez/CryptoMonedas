#!/bin/bash
docker build -t="cryptongo-api" .
docker run -it --rm --link=mongo-crypto:mongo-crypto -p 5000:5000 -v "$(pwd):/app" cryptongo-api
