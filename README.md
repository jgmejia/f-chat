# Financial Chat

Financial Chat is a small chat application that allows you to create conversation rooms in which multiple users can interact.

Financial Chat also uses a chat bot that consumes an external stock-value endpoint.  In order to call the bot, the user should issue the following command:
```
/stock=AMZN
```
The bot takes the command and gets the stock price for the company that appears after the equal sign('='), if it exists.

## Demo

To see Financial Chat in action, please visit [the demo page](http://66.228.52.196:54321/chat/)

## Libraries

Financial Chat uses some libraries, but the most important are:

 * Django 2.1.7
 * Channels 2.1.7
 * requests 2.21.0

## Pre-requisites

In order to run Financial Chat, the server must be running an instance of redis-server.
Proceed to install it according to your distro and the run:
```
$ redis-server
```

After that you should be seeing something like this:

```
[...]
23952:M 26 Feb 2019 18:31:50.265 * Ready to accept connections
```

## Installation

```
$ mkdir chat
$ cd chat
$ python -m venv venv
$ source venv/bin/activate
$ git clone https://github.com/jgmejia/f-chat.git
$ cd f-chat
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py loaddata user.json
$ python manage.py runserver 0.0.0.0:54321
```

## Running the bot worker

The bot is a decoupled channels worker.  In order to start the bot, run in a separate command line the following commands:

```
$ source venv/bin/activate
$ cd f-chat
$ python manage.py runworker stockbot
```
