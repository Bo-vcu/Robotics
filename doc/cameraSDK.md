# documentatie van research voor de camera SDK van de Unitree Go 1

## interessante links

* app: https://www.unitree.com/app/go1/  https://play.google.com/store/apps/details?id=com.unitree.doggo2&hl=en_US  

## installatie volgen via de git van de cameraSDK van Unitree GO 1

link: https://github.com/unitreerobotics/UnitreecameraSDK

**Alles op de virtuele Linux machine!**

Voor de shell scripts uit te voeren, eerst het script op de juiste plaats kopiëren, daarna de permission aanpassen:

```
chmod +x cameraSDK.sh
```

Eerst de git van de unitree binnenhalen op je eigen linux machine.

```
$ git clone git@github.com:unitreerobotics/UnitreecameraSDK.git
```

Daarna builden door deze commands:

```
$ mkdir build && cd build;
$ cmake ..;
$ make;
```

Na de readme.md van de cameraSDK te volgen krijg ik deze error bij cmake ..

```
brinio@Ubuntu:~/Documents/testCameraSDK/UnitreecameraSDK$ cd build
brinio@Ubuntu:~/Documents/testCameraSDK/UnitreecameraSDK/build$ cmake ..
CMake Deprecation Warning at CMakeLists.txt:1 (cmake_minimum_required):
  Compatibility with CMake < 2.8.12 will be removed from a future version of
  CMake.

  Update the VERSION argument <min> value or use a ...<max> suffix to tell
  CMake that the project does not need compatibility with older versions.


CMake Error at CMakeLists.txt:11 (find_package):
  By not providing "FindOpenCV.cmake" in CMAKE_MODULE_PATH this project has
  asked CMake to find a package configuration file provided by "OpenCV", but
  CMake did not find one.

  Could not find a package configuration file provided by "OpenCV" with any
  of the following names:

    OpenCVConfig.cmake
    opencv-config.cmake

  Add the installation prefix of "OpenCV" to CMAKE_PREFIX_PATH or set
  "OpenCV_DIR" to a directory containing one of the above files.  If "OpenCV"
  provides a separate development package or SDK, be sure it has been
  installed.


-- Configuring incomplete, errors occurred!
See also "/home/brinio/Documents/testCameraSDK/UnitreecameraSDK/build/CMakeFiles/CMakeOutput.log".
```

Cmake vindt niks van opencv. Hierdoor moet er iets aangepast worden in de CMakeLists.txt, als ik dit doe, krijg ik nog steeds dezelfde error

Dit is op te lossen door alles fatsoenlijk te installeren door 

```
sudo apt install libopencv-dev
sudo apt-get install libglew-dev libglfw3-dev libglm-dev
//sudo apt-get install libao-dev libmpg123-dev
```

Nu is de camera SDK geïnstalleerd, je kan checken of alles goed is geïnstalleerd door een example uit te voeren.

Als je opnieuw wil builden, altijd eerst de build folder verwijderen en daarna opnieuw te builden.

```
$ rm -rf ../build/;
$ mkdir build && cd build;
$ cmake ..;
$ make;
```