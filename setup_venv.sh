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

# Deactivate venv (redundant?)
deactivate
