# Creating and Running a ROS 2 Package

## 1. Setting Up the Workspace

Open your workspace in terminal (In Thallium this would be ros2_ws)\

```
cd ~/ros2_ws
```

go to the src folder and execute the following command:

```
cd src
ros2 pkg create --build-type ament_python --license Apache-2.0 <name>
```

## 2. Writing code in ROS

Navigate to the package directory:

```
cd <name>/<name>
```

here, create a **`.py`** file and write your program. For detailed code examples, refer to the ROS 2 documentation. (see other docs for code)

## 3. Modifying `package.xml`

Navigate to `src/<name>` and open `package.xml`. In this file, you can add descriptions, maintainers, email addresses, and licenses. Usually, you won't need to change these fields.

To add imports from your **`.py`** file, include the dependencies:

```
<exec_depend>dependency</exec_depend>
```

## 4. Configuring `setup.py`

In the same directory (`src/<name>`), open `setup.py` and add the necessary fields. To publish your functions, modify the **`entry_points`** section as follows:

```
entry_points={
    'console_scripts': [
        'fuction_name = package.fuctionname:main',
    ],
},
```

## 5. Building and Running the Package

### Installing Dependencies

In your workspace, install all needed dependencies:

```
rosdep install -i --from-path src --rosdistro humble -y
```

### Building the Package

Build the package using `colcon`:

```
colcon build --packages-select package name
```

### Sourcing and Running

Source the setup file:

```
source install/setup.bash
```

Run your scripts with:

```
ros2 run package fuctionname
```

## Source

https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html

https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Creating-Your-First-ROS2-Package.html
