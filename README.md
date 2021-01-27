# Inventory
This is te Module 5 assignement

commands for virtual environment

python3 -m venv venv
source venv/bin/activate

on Windows
.\venv\Scripts\activate

make a gitignore
/venv
/__pycache__

pip3 install -r requirements.txt

# after a new package being installed 
# you need to update the requirements
pip3 freeze > requirements.txt
- will install the new files

# to install the reqirements
pip3 install -r requirements.txt