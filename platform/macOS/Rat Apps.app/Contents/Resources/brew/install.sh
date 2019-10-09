#!/bin/bash -e
# set -x

if hash brew 2>/dev/null; then
	echo "Brew is already installed"
else
	echo "Installing brew first..."
	CI=1 /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
	eval `/usr/libexec/path_helper -s`
fi

printf "\n\nInstalling python 3\n\n"
brew install python3
brew link --overwrite python3
printf "\n\nInstalling pyqt\n\n"
brew install pyqt
printf "\n\nInstalling pyqtgraph\n\n"
pip3 install pyqtgraph
printf "\n\nInstalling numpy\n\n"
brew install numpy
printf "\n\nInstalling opencv-python\n\n"
pip3 install opencv-python

printf "\n\nInstallation complete. You may quit Terminal and return to the Rat Apps."
