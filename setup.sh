#! /bin/bash


echo " "
echo " ////////////////////////////////////////////////////////////////////////////////////////// "
echo " //                                                                                      // "
echo " //    __       __  .__   __.  __    __  ___   ___                                       // "
echo " //   |  |     |  | |  \ |  | |  |  |  | \  \ /  /                                       // "
echo " //   |  |     |  | |   \|  | |  |  |  |  \  V  /                                        // "
echo " //   |  |     |  | |  . '  | |  |  |  |   >   <                                         // "
echo " //   |  '----.|  | |  |\   | |  '--'  |  /  .  \                                        // "
echo " //   |_______||__| |__| \__|  \______/  /__/ \__\                                       // "
echo " //                                                                                      // "
echo " //     ______   ______   .______     ______    __   __        ______   .___________.    // "
echo " //    /      | /  __  \  |   _  \   /  __  \  |  | |  |      /  __  \  |           |    // "
echo " //   |  ,----'|  |  |  | |  |_)  | |  |  |  | |  | |  |     |  |  |  | '---|  |----'    // "
echo " //   |  |     |  |  |  | |   ___/  |  |  |  | |  | |  |     |  |  |  |     |  |         // "
echo " //   |  '----.|  '--'  | |  |      |  '--'  | |  | |  '----.|  '--'  |     |  |         // "
echo " //    \______| \______/  | _|       \______/  |__| |_______| \______/      |__|         // "
echo " //                                                                                      // "
echo " //           _______. _______ .___________. __    __  .______                           // "
echo " //          /       ||   ____||           ||  |  |  | |   _  \                          // "
echo " //         |   (----'|  |__   '---|  |----'|  |  |  | |  |_)  |                         // "
echo " //          \   \    |   __|      |  |     |  |  |  | |   ___/                          // "
echo " //      .----)   |   |  |____     |  |     |  '--'  | |  |                              // "
echo " //      |_______/    |_______|    |__|      \______/  | _|                              // "
echo " //                                                                                      // "
echo " ////////////////////////////////////////////////////////////////////////////////////////// "
echo " "

echo "==============================="
echo "    Welcome to the Installer   "
echo "==============================="
echo ""

function print_message() {
    local msg="$1"
    echo "--------------------------------"
    echo "$msg"
    echo "--------------------------------"
}

cd frontend || { echo "Frontend directory not found!"; exit 1; }
print_message "Installing frontend packages..."
npm install
wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt update -y
sudo apt install -y ./google-chrome-stable_current_amd64.deb
print_message "Frontend packages installed."

cd ../backend || { echo "Backend directory not found!"; exit 1; }
print_message "Installing backend packages..."
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
print_message "Backend packages installed."

echo ""
echo "==============================="
echo "    Installation Completed!     "
echo "==============================="



