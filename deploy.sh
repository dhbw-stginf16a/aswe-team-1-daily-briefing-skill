#!/bin/bash

tar -cf deploy.tar Pipfile Pipfile.lock app.py openapi api

echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
docker build -t asweteam1/briefing-skill:latest -t asweteam1/briefing-skill:$TRAVIS_TAG --label version="$TRAVIS_TAG" .
docker push asweteam1/briefing-skill:latest
docker push asweteam1/briefing-skill:$TRAVIS_TAG
