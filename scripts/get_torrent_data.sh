#!/bin/bash

: '
This script is used by the python app for reading torrents from the transmission-daemon CLI and takes the username
and password as the first and second argument.
Feel free to swap in another script for reading from a different client. If doing that (and not modifying the python)
then the script should return a list of torrents in this format:

Percentage Status Name

Example output:

0% Stopped ubuntu-18.04.3-desktop-amd64.iso
72% Downloading ubuntu-16.04-live-server-amd64.iso
100% Idle ubuntu-19.10-live-server-amd64.iso

Percentage sign in the first column is stripped off if present.

The status "Downloading" in the example above is the only status that the python app cares about and is used to
determine if a torrent is not paused/complete. Otherwise the percentage is used to decide if a torrent is completed or
in progress.
'

transmission-remote -n "$1:$2" -l | awk '{print $2, $(NF-1), $NF}' | awk 'NR>2 {print last} {last=$0}'