# Humble Bundle Cataloger

A simple way to go from a Humble Bundle collection JSON to a website

## How To Use

- Install requirements with `pip install -r requirements.txt`
- Go to your humble bundle library: https://humblebundle.com/home/library
- Use your browser's Dev tools to inspect the network traffic, and find the one that is something like `https://www.humblebundle.com/api/v1/orders?all_tpkds=true`
- Take the response, and save it as `humble_catalog.json`
- Run `python3 process.py`
- Take `catalog.html` and `img` and publish it however you'd like