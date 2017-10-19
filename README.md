# recruiting

## setup
vagrant up
vagrant ssh

## update apt-get
sudo apt-get update && sudo apt-get -y upgrade

## install dependencies
sudo apt-get install python-pip python-dev python-pillow python-reportlab
sudo apt-get install libxml2-dev libxslt1-dev libffi-dev python-lxml
sudo pip install -r requirements.txt

## setup a new database
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

## run the server
python manage.py runserver 0.0.0.0:80