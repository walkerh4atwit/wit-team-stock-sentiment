BASE_PYTHON_PATH="/bin/python3.11"

if [ ! -d "venv" ]; then 
    $BASE_PYTHON_PATH -m pip install virtualenv
    virtualenv venv
fi

VIRTUAL_PYTHON_PATH="./venv/bin/python"

$VIRTUAL_PYTHON_PATH -m pip install -r requirements.txt