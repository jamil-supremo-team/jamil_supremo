#!/bin/bash

sudo adduser company
sudo adduser engineer
sudo adduser operator

sudo usermod -aG sudo company

sudo groupadd distribution

sudo usermod -aG distribution company
sudo usermod -aG distribution engineer
sudo usermod -aG distribution operator

groups company
groups engineer
groups operator