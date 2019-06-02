![image](https://raw.githubusercontent.com/instagrambot/instabot.ai/master/img/banner.png)
---
### [Website](https://instabotai.com/) | [Read the Docs](https://instabotai.github.io/docs/) | [Contribute](https://github.com/instagrambot/docs/blob/master/CONTRIBUTING.md) | [Buy Instagram Expert Marketing](https://www.fiverr.com/hourapp/grow-your-instagram-followers-for-7-days)
---
# InstabotAi

Instabotai is an instagram bot with face detection that uses the undocumented Web API. Instabotai can reupload photo to feed, reupload photo to stories, comment, like and DM users if a face is detected on image.
Unlike other bots, Instabotai does not require Selenium or a WebDriver. Instead, it interacts with the API over simple HTTP Requests. It runs on most systems.

[![Telegram Chat](https://camo.githubusercontent.com/67fd2a1c7649422a770e7d82cb35795c2a8baf32/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f636861742532306f6e2d54656c656772616d2d626c75652e737667)](https://t.me/instabotai)

## Requirements
* Python 3.6+
* Min 20-30 Profiles to scrape or it will repost same image when no new image is posted in list.

### Installation with PIP
Install `instabotai` with:
``` bash
pip install -U instabotai
```
Run `instabotai` with:
``` bash
instabotai -u yourusername -p password -l josephineskriver,wolfiecindy -t "#like4like#follow4follow"
```

### Installation with Docker
``` bash
docker pull reliefs/instabotai

docker run reliefs/instabotai -u username -p password -l josephineskriver,wolfiecindy -t "#tag1#tag2"
```

## Face detection at work on a live webcam 

![image](https://res.cloudinary.com/practicaldev/image/fetch/s--qdvR8Vl8--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_66%2Cw_880/https://cloud.githubusercontent.com/assets/896692/24430398/36f0e3f0-13cb-11e7-8258-4d0c9ce1e419.gif)

This script scrapes images from users and then repost, like and comment their images if face is detected with your own tags.

Demo:
https://www.instagram.com/maskofshiva

The script does not work with new accounts. If you know how to fix, send me a message. 

## To install script on Windows:

### Install Cmake 
download link : https://github.com/Kitware/CMake/releases/download/v3.14.1/cmake-3.14.1.zip

### Install Dblib
Download dlib ‘.wheel’ file as ur system requirnment (use link bellow)
download link : https://pypi.python.org/simple/dlib/

```
Open cmd navigate to dlib wheel file path and hit command
pip install dlib_file_name.wheel
```

### Then run

``` bash
git clone https://github.com/instagrambot/instabotai.git --recursive
```

```
cd instabotai/
```

```
pip install -r requirements.txt
```

```
python example.py -u yourusername -p password -l josephineskriver,wolfiecindy -t "#like4like#follow4follow"

```

And press Enter.


## To install script on Linux:
```
Ubuntu:
apt-get install python-dev python3-dev
sudo apt install g++
sudo apt install cmake
sudo apt install python3-pip

Arch Linux:
sudo pacman -S cmake
sudo pacman -S python3-pip
```

First, make sure you have dlib already installed with Python bindings:

  * [How to install dlib from source on macOS or Ubuntu](https://gist.github.com/ageitgey/629d75c1baac34dfa5ca2a1928a7aeaf)
  

### Then do

```
git clone https://github.com/instagrambot/instabotai.git

cd instabotai

sudo pip install -r requirements.txt

python example.py -u yourusername -p password -l josephineskriver,wolfiecindy -t "#like4like#follow4follow"

```

## Troubleshoot
If you are getting Illegal Instruction with face_recognition follow this guide:
https://github.com/ageitgey/face_recognition/issues/11#issuecomment-475482716

AttributeError: 'module' object has no attribute 'face_recognition_model_v1'

Solution: The version of dlib you have installed is too old. You need version 19.7 or newer. Upgrade dlib.

### For Dlib install error run 

python3 setup.py install --no DLIB_USE_CUDA
