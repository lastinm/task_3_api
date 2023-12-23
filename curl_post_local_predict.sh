#!/bin/bash

# toxic
curl -X 'POST' 'http://127.0.0.1:8000/predict/' -H 'Content-Type: application/json' -d '{ "text": "Эта лодка дырявая калоша."}'

# non-toxic
#curl -X 'POST' 'http://127.0.0.1:8000/predict/' -H 'Content-Type: application/json' -d '{ "text": "Съешь еще спелых яблочек."}'
