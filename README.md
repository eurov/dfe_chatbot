#  DFE Console chatbot 

## About
Telegram bot which is built on [Dialog Flow Engine (DFE)](https://github.com/deepmipt/dialog_flow_engine),
with add-ons:

- [Dialog Flow Telegram Connector](https://github.com/deepmipt/dialog_flow_telegram_connector)
- [Dialog Flow DB Connector](https://github.com/deepmipt/dialog_flow_db_connector)
- [Dialog Flow Runner](https://github.com/deepmipt/dialog_flow_runner/tree/dev/df_runner) 

To store and retrieve a dialog context is used Yandex Database which is use [YQL](https://ydb.tech/en/docs/yql/reference/) 
query language.


The bot offers you to complete a small quest, the plot of which is based on a book about Harry Potter.
A new user starts from the first year of study at Hogwarts. The user already in the database continues training from the corresponding year.
## Quick Start


```
make start_app
```

To start the chat, just type:
```
Hi
```
