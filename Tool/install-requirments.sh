
# Install pip on Mac

GET_PIP_FILE=/tmp/get-pip.py
GET_REQIREMENT_FILE =/tmp/requirements.txt

# install pip
#curl "https://bootstrap.pypa.io/get-pip.py" -o "${GET_PIP_FILE}"
#python ${GET_PIP_FILE}

# install requirements
curl "https://raw.githubusercontent.com/sn0wfree/data-collection-and-api/master/API/Google_trend/Source/requirements.txt" -o "${GET_REQIREMENT_FILE}"
pip install -r ${GET_REQIREMENT_FILE}
