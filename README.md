# code bin

A very quick pastebin replacement for sharing code/information with others easily and without worrying what pastebin or (zoom, etc.) is doing with your information. I deploy this to a t2.micro ec2 instance ($62.00 a year w/ cost savings plan in 2023).

### Change your domain 

In order to deploy this application you have to alter the domain settings to the domain you intend to use for this site. Of course this should be included in the environment but I haven't gotten to that yet. That domain is in a few places, but most importantly:

compose/production/traefik/traefik.yml
config/settings/base.py
config/settings/production.py

or simply grep for code.freelancelance.com


### deploy

this project uses tailwind. you have to build the tailwind css files before you deploy. make sure you have postcss-cli installed and then you can run 

npm install 
npm build:css 

and then

sudo docker compose -f production.yml run --rm django python manage.py migrate 
sudo docker compose -f production.yml run --rm django python manage.py createsuperuser

### todo 

fix bug related to the settings not pulling the login url 


### Docker

This application can be built and deployed with docker quickly. 

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).
