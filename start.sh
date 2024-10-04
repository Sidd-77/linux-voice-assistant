#! /bin/bash

cd frontend
npm run dev &
chromium-browser --kiosk http://localhost:5173 &

cd ../backend
source .venv/bin/activate
fastapi dev main.py &

