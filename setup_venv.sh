#!/bin/sh

# Fancy colors
BLACK=$(tput setaf 0)
RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
BLUE=$(tput setaf 4)
MAGENTA=$(tput setaf 5)
CYAN=$(tput setaf 6)
NORMAL=$(tput sgr0)

# Create venv
virtualenv venv

# Add path file
pwd -LP > venv/lib/python2.7/site-packages/testliveserver.pth

# Download and extract Chromedriver according to OS architecture
if [ `getconf LONG_BIT` = "64" ]
then
	wget https://chromedriver.googlecode.com/files/chromedriver_linux64_2.2.zip
	unzip chromedriver_linux64_2.2.zip
	rm chromedriver_linux64_2.2.zip
else
    wget https://chromedriver.googlecode.com/files/chromedriver_linux32_2.2.zip
	unzip chromedriver_linux32_2.2.zip
	rm chromedriver_linux32_2.2.zip
fi

# Move the executable and change permissions
mv chromedriver venv/bin
chmod 777 venv/bin/chromedriver

# Activate venv
. venv/bin/activate

# Install requirements
pip install --requirement requirements.txt

#########################
# Google App Engine SDK #
#########################

echo "${YELLOW}Downloading Google App Engine SDK.${NORMAL}"

wget $QUIET http://googleappengine.googlecode.com/files/google_appengine_1.8.3.zip
unzip $QUIET google_appengine_1.8.3.zip
rm google_appengine_1.8.3.zip

echo "${GREEN}Installing Google App Engine SDK to:${NORMAL} venv/bin/google_appengine"
mv google_appengine venv/bin

PTH=venv/lib/python2.7/site-packages/gae.pth
echo "${GREEN}Adding pth file:${NORMAL} $PTH"
echo "$(pwd -LP)/venv/bin/google_appengine/" >> $PTH
echo "import dev_appserver; dev_appserver.fix_sys_path()" >> $PTH

# Deactivate venv (redundant?)
deactivate
