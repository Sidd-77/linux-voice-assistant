#! /bin/bash

cd frontend
echo "Installing frontend packages..."
npm install
sudo apt update
sudo apt install -y chromium-browser
echo "Frontend packages installed."


cd ../backend
echo "Installing backend packages..."
pyhton -m venv .venv
source venv/bin/activate
pip install -r requirements.txt
echo "Backend packages installed."


