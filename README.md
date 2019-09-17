![image](https://raw.githubusercontent.com/instabotai/instabotai/master/img/banner.png)
---
### | [Website](https://instabotai.com/) | [Read the Docs](https://instabotai.github.io/docs/) | [Contribute](https://github.com/instagrambot/docs/blob/master/CONTRIBUTING.md) |

---
 [![PyPI version](https://badge.fury.io/py/instabotai.svg)](https://badge.fury.io/py/instabotai)
 [![Telegram Chat](https://camo.githubusercontent.com/67fd2a1c7649422a770e7d82cb35795c2a8baf32/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f636861742532306f6e2d54656c656772616d2d626c75652e737667)](https://t.me/instabotai)
 [![Build Status](https://travis-ci.org/instagrambot/instabot.svg?branch=master)](https://travis-ci.org/instagrambot/instabotai)
![Python 2.7, 3.5, 3.6, 3.7](https://img.shields.io/badge/python-2.7%2C%203.5%2C%203.6%2C%203.7-blue.svg)

# InstabotAI

Instabotai is an instagram bot with face detection that uses the undocumented Web API. Instabotai can reupload photo to feed, reupload photo to stories, watch stories, comment, like and DM users if a face is detected on image.
Unlike other bots, Instabotai does not require Selenium or a WebDriver. Instead, it interacts with the API over simple HTTP Requests. It runs on most systems.

![image](https://i.imgur.com/yv9eAyv.png)

### Requirements
* Python 3.7+ 64bit
* Microsoft Visual C++ 2015 Redistributable Update 3 
* https://www.microsoft.com/en-us/download/details.aspx?id=53587 (Only required for Windows Users)

## Features
* Like Users Following Images with AI
* Like Users Followers Images with AI
* Like Hashtag Images AI
* Follow User Followers
* Follow User Following
* Comment User Followers
* Comment User Following
* Watch Infinity Stories by user
* Like Hashtag Images
* Like all image comments
* Multibot
* GUI

### Installation 
Python 3.7+ 64bit - https://www.python.org/ftp/python/3.7.4/python-3.7.4-amd64.exe - Enable ADD TO PATH
https://www.microsoft.com/en-us/download/details.aspx?id=53587 (Only required for Windows Users)
``` bash
git clone https://github.com/instabotai/instabotai.git or Click Download Above
cd instabotai
pip install -U pip
pip install -r requirements.txt
python run.py -u username -p password

If you only want to use CLI run:
python cli.py -u username -p password
```
### Installation with docker

``` bash
git clone https://github.com/instabotai/instabotai.git
docker build .
sudo docker run -ti -p 8000:8000 YOURIMAGEID -u username -p password
[On Linux You need to change the run.py line 652 127.0.0.1 to 0.0.0.0 before building docker]

```

### Installation with tensorflow 1.14 or Python 32 bit+
``` bash
If your system does not support tensorflow 2.0.
Delete mtcnn folder
Download it trough pip: pip install mtcnn
python run.py -u username -p password
```

## Run: 
python run.py -u yourusername -p yourpassword

Open http://127.0.0.1:8000/ in your browser

Works on all browsers without extensions!

To install tensorflow on your system without pip.
### Arch Linux:
Pacman -S tensorflow

