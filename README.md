# Financial Chat

Financial Chat is a small chat application that allows you to create conversation rooms in which multiple users can interact.

## Demo

To see Financial Chat in action, please visit [the demo page](http://66.228.52.196:54321/chat/)

## Libraries

Financial Chat uses some libraries, but the most important are:

 * Django 2.1.7
 * Channels 2.1.7
 * requests 2.21.0

## Installation

```
mkdir chat
cd chat
python -m venv venv
source venv/bin/activate
git clone https://github.com/jgmejia/f-chat.git
cd f-chat
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:54321
```
