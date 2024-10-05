#! /bin/bash

echo "===================================="
echo "    Welcome to the Linux Copilot    "
echo "===================================="

# making it fancy for no specific reason
function print_message() {
    local msg="$1"
    echo "--------------------------------"
    echo "$msg"
    echo "--------------------------------"
}

# Cleanup function to terminate background processes
cleanup() {
    print_message "Terminating all background processes..."
    kill $(jobs -p)
    wait
}

trap cleanup SIGINT SIGTERM  # Catch signals to cleanup

# Navigate to the backend, activate virtual environment, and start FastAPI
cd backend || { echo "Backend directory not found!"; exit 1; }
print_message "Activating virtual environment and starting FastAPI..."
source .venv/bin/activate
fastapi dev main.py &

# Navigate to the frontend and start the development server
cd ../frontend || { echo "Frontend directory not found!"; exit 1; }
print_message "Starting frontend development server..."
npm run dev &

# Uncomment the following line if you want to start Electron as well
# npm run start-electron &

# Launch Google Chrome with specific flags
print_message "Launching Google Chrome..."
google-chrome --alsa-output-device=default --no-sandbox --disable-web-security --enable-media-stream \
--use-fake-ui-for-media-stream --disable-gpu --disable-software-rasterizer --window-size=800,600 \
--kiosk http://localhost:5173 &

# Wait for all background processes to complete
wait
