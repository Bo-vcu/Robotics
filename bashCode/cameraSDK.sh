git clone git@github.com:unitreerobotics/UnitreecameraSDK.git
sudo apt install libopencv-dev
sudo apt-get install libglew-dev libglfw3-dev libglm-dev

cd UnitreecameraSDK
mkdir build && cd build	

cmake ..
make