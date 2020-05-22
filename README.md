# 4.2 inch Waveshare E-paper display API / transmission torrent display

###### Display script and API for Waveshare 4.2 inch black and colour e-paper (400x300) with Raspberry pi. Can be installed as a service. Runs two modes, which can be switched via the API:
###### 1. Displays images sent to a flask endpoint (currently accepts separate black and yellow image)
###### 2. Monitors a transmission client and displays torrents on screen. Plain or a silly chilli theme
###### More modes to come, including dithered image display, gallery display, piHole stats. Simple UI also coming.
###### I used this project to pick up python, so be nice!

![](images/torrent_box_demo.jpg)

## Pre-requisites:

This script has been written to work on a Raspberry Pi running Raspbian Buster.   

Uses a 4.2 inch wave-share e-paper module, connected according to the instructions in the wiki here:
https://www.waveshare.com/wiki/4.2inch_e-Paper_Module_(B)

Also requires transmission to have been set up on the local machine with the network UI like here: 
https://pimylifeup.com/raspberry-pi-transmission/

## Installation:
1. Follow the steps above to install transmission and get the waveshare epaper demo running
2. Install project dependencies by going to the terminal and entering:
    ```bash
    sudo apt update
    sudo apt install python3
    sudo apt install python3-pip
    sudo apt install python3-pil
    sudo apt install python3-numpy
    sudo pip3 install RPi.GPIO
    sudo pip3 install spidev
    sudo pip3 install PyYAML
3. Enable SPI interface by entering
    ```bash
    sudo raspi-config
then navigating through Interfacing Options -> SPI interface -> enable. 
4. Clone this repo
    ```bash
    git clone https://github.com/myx360/torrent_box_epaper_display.git
5. Go to the within the project directory and configure the config.yml file using your favourite terminal editor
    ```bash
    cd torrent_box_epaper_display
    sudo chmod 600 config.yml
    vi config.yml
6. If you wish to use the API then you will need to open up the port to do so, do the following:
    ```bash
    sudo ufw allow in 5001
7. At this point, if you would just like to test the display, trying running the following with
your username and password for the transmission client. Remember to stop it before the next step.
(you can close the program using ctrl + c)
    ```bash
    python3 main.py username password
8. If you would like to run the torrent display as a service run the install_as_a_service.sh script. This only works with systemd.
    ```bash
    sudo ./install_as_a_service.sh
    sudo systemctl enable epaper_display

## Disclaimer:
Running as a service requires storing your username and password to the transmission daemon in a config file,
config.yml in order to use those details when polling the transmission daemon. This file should be left only readable by
root, and obviously will be readable by the root user no matter what, so don't re-use this password. I accept no
responsibility for any risks caused by or associated with this. Some encryption may come in a future release, but even
then any user with root access will be able to decrypt it. A workaround has been provided in which you give the user and
password as arguments when running the script as described in the install steps.
