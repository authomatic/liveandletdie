# Default to python2 for venv
PYTHON_VER=${PYTHON_VER:-2}

rm -f bootstrap/bootstrap.py
python${PYTHON_VER} bootstrap/makebootstrap.py
python${PYTHON_VER} bootstrap/bootstrap.py -p python${PYTHON_VER} venv
. venv/bin/activate
pip install -r requirements${PYTHON_VER}.txt
deactivate
