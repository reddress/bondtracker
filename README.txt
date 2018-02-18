Bond Tracker

A Django (1.10.5) app to keep track of bond purchases and sales

Superuser password hint:
heitor/dj----##

Ubuntu setup

One-time only in bondtracker (root) folder:
virtualenv -p /usr/bin/python3 venv

source venv/bin/activate
pip install Django  # (once only)

# in /bondtracker
python manage.py migrate
python manage.py createsuperuser

In Ubuntu, use Python 3 with:
source venv/bin/activate

In PTL Windows, Python 3 is the default.
