# Appear

## Introduction

It's a python base solution for managing presence of people comming in and out of school classes. 
You need a webcam or anycamera linked to the computer to be able to run.

## Installation requires python 3 (Windows)
```python
pip install -r requirements.txt
```

You gonna need and ``` env.py ``` with the ``` TELEGRAM_TOKEN="xpto" ``` and ``` CHAT_ID="123" ``` defined, the token is from your bot and the chat_id is a group with the bot in case the registered chat_id of a person is not available.

## Running

***You have 2 options for this***

### Regestering Faces

```ps
python src/register_main.py
```
You'll be asked to fill the inputs bellow:
- Name: ```Ex.: John```
- Code: ```Any Unique Identifier```
- Phone: ```not used yet, can be blank```
- Chat-Id: ```Telegrams Chat-Id```

### Managing Presence

Open 2 terminals:
- On terminal 1:
```ps
python src/presence_main.py
```
- On terminal 2:
```ps
python src/image_bus_main.py
```

### Output

The ``` image_bus_main.py ``` will generate a .csv containing all identifications with their timespan, remember, an identification is considered when the mathing of an face accured (*n*) times, *n* being defined in the ``` public_env.py ``` file.