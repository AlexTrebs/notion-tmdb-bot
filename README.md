A Python script to find rows in a Notion database where certain properties are empty, fetch metadata from The Movie Database (TMDB), and fill those properties automatically.

## Features

* Queries Notion for pages missing data in one or more fields
* Searches TMDB for movie or TV show details (including credits)
* Populates Notion properties like Poster URL, Genre, Director, Studio, etc.
* Handles new fields dynamically—just add them to your config map
* Caches TMDB requests and parallelizes updates for performance

## Prerequisites

* Python 3.8 or newer
* A terminal / command prompt
* Access to your Notion workspace
* A TMDB account with an API v4 Read Access Token

## Installation
Clone this repo and cd into it

```bash
pip install -r requirements.txt
```
## Environment Variables
Create a file named `.env` in the project root and define the following variables.

### TMDB_TOKEN
Your TMDB API v4 Read Access Token. How to get it:

1. Sign in at https://www.themoviedb.org/
2. Go to your account settings → API
3. Under “API v4 (Read Access Token)” click Create or Retrieve
4. Copy the generated token (starts with eyJ…)

### NOTION_TOKEN
A Notion integration token with access to your database. How to get it:

1. Visit https://www.notion.so/my-integrations and click New integration
2. Give it a name and select the workspace
3. Click Submit and copy the Internal Integration Token

** Make sure to add your workspace to your integrations **

### NOTION_DB
The ID of the database you want to update. How to get it:

1. Open your database in Notion
2. Click ••• → Copy link
3. The URL will look like
```
https://www.notion.so/My-DB-Name-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx?v=yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
```
or
```
https://www.notion.so/<long_hash_1>?v=<long_hash_2>
```
4. Extract the 32-character string after your name (the part marked `xxxxxxxx…` or `<long_hash_1>`)
5. Add dashes in the 8-4-4-4-12 pattern if needed:
```
xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

### NOTION_DB_TITLE (optional)
The name of your title property in Notion (defaults to `Name`).


### NOTION_EMPTY_PROPERTY_MAP
A JSON object mapping each Notion property name to its filter type. At minimum include all the fields you want to fill. Example:

```dotenv
NOTION_EMPTY_PROPERTY_MAP='{
  "Poster":"rich_text",
  "Genre":"multi_select",
  "Director":"rich_text",
  "Studio / Distributor":"multi_select",
  "Type":"select"
}'
```
Example .env
```dotenv
TMDB_TOKEN=eyJxxxYOUR_TMDB_TOKENxxx
NOTION_TOKEN=secret_xxxYOUR_NOTION_TOKENxxx
NOTION_DB=25ee7153-f4b9-80b2-9dfd-cea91237d4b1
NOTION_DB_TITLE="Movie / Series"
NOTION_EMPTY_PROPERTY_MAP={"Poster":"rich_text","Genre":"multi_select","Director":"rich_text","Studio / Distributor":"multi_select","Type":"select"}
```

## Usage
Run the updater script:

```bash
python notion_tmdb_updater.py
```
You should see logs like:

```
2025-08-30 14:22:01 INFO Found 5 pages to update
2025-08-30 14:22:01 INFO Updated 'The Big Lebowski'
...
```

## Extending with New Fields
Add the new property name and filter type to `NOTION_EMPTY_PROPERTY_MAP` in your `.env`.

In `handlers.py`, register a new entry in `PROP_HANDLERS`:

```python
PROP_HANDLERS["Revenue"] = lambda info: {"number": info["revenue"]}
```
Re-run the script—it will now query pages missing **Revenue** and attempt to populate them.

## Troubleshooting
If you see 400 Bad Request errors, verify your property names and types in Notion match your map.

Use logging output to identify pages that failed.

Confirm your `.env` is in the same directory where you launch the script.