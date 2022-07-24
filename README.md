#  DFE Console chatbot 

## About
The conversational console service which is built on [Dialog Flow Engine (DFE)](https://github.com/deepmipt/dialog_flow_engine).
With [Dialog Flow DB Connector](https://github.com/deepmipt/dialog_flow_db_connector) added an ability to save and retrieve user dialogue states using Postgresql. 

The bot offers you to complete a small quest, the plot of which is based on a book about Harry Potter.
A new user starts from the first year of study at Hogwarts. The user already in the database continues training from the corresponding year.
## Quick Start

Install requirements from Pipfile:
```
pipenv install
```

You may pass the user ID when initializing the console chat:
```
python main.py 1
```
Otherwise, will be assigned a random ID.

To start the chat, just type:
```
Me: Hi
```
