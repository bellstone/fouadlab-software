# Rat Apps

This collection of rat apps is used to analyze the behavior of rats in a research setting. There are four apps:
* Open Field
* SPG Analysis
* White Box
* X Maze

## Installation Instructions

### macOS

To bundle the app, cd into `platform/macOS` and run `insertResources.sh`. That will copy the four python apps into an AppleScript launcher. The resulting `Rat Apps.app` can be copied to any Mac.

After launching `Rat Apps.app`, choose "Install" to install the required python libraries. Then you can select any of the apps to be launched.

### Windows

To bundle the app, first install Python from https://www.python.org/downloads/windows/. Make sure to

From a command prompt, run `pip install pyqt5 pyqtgraph opencv-python auto-py-to-exe`.

Run `auto-py-to-exe` and launch with a web browser. Select "OneFile" mode and "Window Based," then build each app by selecting the appropriate .py file.

The resulting .EXEs should run on any Windows 10 computer.
