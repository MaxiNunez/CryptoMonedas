#!/bin/bash
docker build -t="cryptongo-agent" .
docker run -it --link=mongo-crypto:mongo-crypto cryptongo-agent