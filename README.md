# SP24-Improving race shifting with a Raspberry Pi powered heads up display

## What We Did
AboutTheProject.txt

## Prototype
![Alt text](data/images/___.jpg?raw=true "Title")

## Our github repository:
https://github.com/csu-hci-projects/SP24-Cb213

## Video Links from our project:
#### Demo Video:
#### Presentation Video:
#### Code Explanation Video: 

## Hardware and setup:
- Raspberry Pi 4B <u>[here](https://www.amazon.com/Raspberry-Pi-Computer-Suitable-Workstation/dp/B0899VXM8F/ref=sr_1_4?dib=eyJ2IjoiMSJ9.mP4drOfyakW9P2E6ytjWi1Dw0PQxL-Sc1CRzWf-ayOeFXq7dwFWtzoG82WzU25ZkPVlzjV3imXZ2hwHfWyDn9shPao4IqA4gqXBsAYxI52NS0z7AgQioveqIQ1zacFrsFhxBa2aCrA3va0MtR3xgbrNKrCU0m-byPpEbLOCdcZA76Dyj8MAPYNkj9Ba2xUe7_u2oL0GCb-m68LqrDgSg_rrFI2M3-iB8qyHgW9U-Gic.Is6NkNRdQ7_Ij12SCAoDxZYJnEoNy9law47qb4Nj2cA&dib_tag=se&keywords=raspberry+pi+4+model+b&qid=1715048708&sr=8-4)</u>
- 7 in Raspberry Pi Compatible LCD Display <u>[here](https://www.amazon.com/GeeekPi-Raspberry-1024x600-Display-Portable/dp/B0CHRD7CQ3/ref=sr_1_3?crid=1H16K4QM1GHI9&dib=eyJ2IjoiMSJ9.twZud7y9W0u7JivHUrlIvR_tP-swfTW5BsLRF-1f4AFct7xgrF_5tVBZnSbvIyCHf35DqGnN_DIidW0PMTBvLK03A0DDQzAPlJTVvFcj11oDiCyAFRrNCgncfBCcK0xme_E0dIkDBkdZVdo7npPhkWyCrhvIhYgMS_MQDgHsvztbWx_WQyLlhAKqn6OeZIN_7GoA84Ie8VgvTJJDliMRJo9ZuxGFilNhpoXYbqzR7sM.Xhl_41ElD6po8xW6yKO3Zqj83NvEgjYwCrKGFsTk0Kg&dib_tag=se&keywords=raspberry%2Bpi%2B7in%2Bdisplay%2B1024x600&qid=1715048646&sprefix=raspberry%2Bpi%2B7in%2Bdisplay%2B1024x600%2Caps%2C137&sr=8-3&th=1)</u>
- Generic ELM327 OBD Chip <u>[here](https://www.amazon.com/dp/B011NSX27A?ref=nb_sb_ss_w_as-reorder_k0_1_5&amp=&crid=2G321JFQ6RFD5&amp=&sprefix=obd2+)</u>
- Raspberry Pi OS (64-bit) Kernel version: 6.6, Debian version: 12 (bookworm), Release date: March 15th 2024
- Python 3.7.3 (For the sake of OBDII software compatibility)

## How to run the project 

#### Installing Kivy from pi terminal-- our chosen GUI langauage for the project
- `sudo apt-get update`
- `sudo apt-get install libfreetype6-dev libgl1-mesa-dev libgles2-mesa-dev libdrm-dev libgbm-dev libudev-dev libasound2-dev liblzma-dev libjpeg-dev libtiff-dev libwebp-dev git build-essential`
- `sudo apt-get install gir1.2-ibus-1.0 libdbus-1-dev libegl1-mesa-dev libibus-1.0-5 libibus-1.0-dev libice-dev libsm-dev libsndio-dev libwayland-bin libwayland-dev libxi-dev libxinerama-dev libxkbcommon-dev libxrandr-dev libxss-dev libxt-dev libxv-dev x11proto-randr-dev x11proto-scrnsaver-dev x11proto-video-dev x11proto-xinerama-dev`

#### Installing SDL2 from pi terminal-- for windows in the GUI
- `wget https://libsdl.org/release/SDL2-2.0.10.tar.gz`
- `tar -zxvf SDL2-2.0.10.tar.gz`
- `pushd SDL2-2.0.10`
- `./configure --enable-video-kmsdrm --disable-video-opengl --disable-video-x11 --disable-video-rpi`
- `make -j$(nproc)`
- `sudo make install`
- `popd`

#### Install SDL2_image:
- `wget https://libsdl.org/projects/SDL_image/release/SDL2_image-2.0.5.tar.gz`
- `tar -zxvf SDL2_image-2.0.5.tar.gz`
- `pushd SDL2_image-2.0.5`
- `./configure`
- `make -j$(nproc)`
- `sudo make install`
- `popd`

#### Install SDL2_mixer:
- `wget https://libsdl.org/projects/SDL_mixer/release/SDL2_mixer-2.0.4.tar.gz`
- `tar -zxvf SDL2_mixer-2.0.4.tar.gz`
- `pushd SDL2_mixer-2.0.4`
- `./configure`
- `make -j$(nproc)`
- `sudo make install`
- `popd`

#### Install SDL2_ttf:
- `wget https://libsdl.org/projects/SDL_ttf/release/SDL2_ttf-2.0.15.tar.gz`
- `tar -zxvf SDL2_ttf-2.0.15.tar.gz`
- `pushd SDL2_ttf-2.0.15`
- `./configure`
- `make -j$(nproc)`
- `sudo make install`
- `popd`

#### Make sure the dynamic libraries cache is updated:
- `sudo ldconfig -v`

#### Install the dependencies:
- `sudo apt update`
- `sudo apt upgrade`
- `sudo apt install pkg-config libgl1-mesa-dev libgles2-mesa-dev \
   python3-setuptools libgstreamer1.0-dev git-core \
   gstreamer1.0-plugins-{bad,base,good,ugly} \
   gstreamer1.0-{omx,alsa} python3-dev libmtdev-dev \
   xclip xsel libjpeg-dev`

#### Install pip3:
- `sudo apt install python3-pip`

#### Install pip dependencies:
- `sudo python3 -m pip install --upgrade pip setuptools`
- `sudo python3 -m pip install --upgrade Cython==0.29.19 pillow`

#### Install Kivy:
- `sudo python3 -m pip install https://github.com/kivy/kivy/archive/master.zip`

#### Copy code and data folders to home/usr/
- "data" folder
- "kivymd" folder
- main.kv
- main.py

#### Navigate to directory and run main.py 
- `sudo python3 main.py`

#### Install Python OBD:
<u>[here](https://python-obd.readthedocs.io/en/latest/#installation)</u>
- `sudo pip3 install obd`

#### Bluetooth Setup:
- `sudo bluetoothctl`
- `agent on`
- `default-agent`
- `scan on`
- `pair xx:xx:xx:xx:xx:xx` <- Your BT OBDII MAC Address
- `connect xx:xx:xx:xx:xx:xx`
- `trust xx:xx:xx:xx:xx:xx`

#### To Start on pi Boot:
- `sudo nano launcher.sh`
```
#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd
cd /home/pi/DRDS
sudo python3 main.py
cd
```

