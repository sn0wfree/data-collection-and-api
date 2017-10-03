
# Install pip

GET_PIP_FILE=/tmp/get-pip.py
GET_REQIREMENT_FILE =/tmp/requirements.txt

# install pip
curl "https://bootstrap.pypa.io/get-pip.py" -o "${GET_PIP_FILE}"
python ${GET_PIP_FILE}
yum update
# install requirements
curl "https://raw.githubusercontent.com/sn0wfree/data-collection-and-api/master/API/Google_trend/Source/requirements.txt" -o "${GET_REQIREMENT_FILE}"
pip install -r ${GET_REQIREMENT_FILE}
pip install cython
yum -y install gcc libxslt-devel libxml2-devel python-devel
pip install unqlite


sudo tee /etc/yum.repos.d/gcsfuse.repo > /dev/null <<EOF
[gcsfuse]
name=gcsfuse (packages.cloud.google.com)
baseurl=https://packages.cloud.google.com/yum/repos/gcsfuse-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg
https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOF

yum -y update
yum -y upgrade
yum -y install gcsfuse
