# Humble Bundle Cataloger

A simple way to go from a Humble Bundle collection JSON to a website. See it in action on my [own catalog](https://marianosimone.com/catalog)

## How To Use
### Setup
- Install requirements with `pip install -r requirements.txt`
- If you are planning on contributing, run `pre-commit install`
- If you want to highlight any entries, create a `recommended.txt` file and put the names of the items
- If you discover any data duplication, take a look at `name_fixes.py`, and contribute them to the project!
- If you discover any non-games showing up as games, add them to `type_fixes.py`, and contribute them to the project!

### Create & Update your catalog
- Go to your humble bundle library: https://humblebundle.com/home/library
- Use your browser's Dev tools to inspect the network traffic, and find the one that is something like `https://www.humblebundle.com/api/v1/orders?all_tpkds=true`
- Take the response, and save it as `humble_catalog.json`
- Run `python3 catalog.py` (optionally with `--all` if you want to include entries that you no longer have available)
- Take `catalog.html` and `img` and publish it however you'd like
