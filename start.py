import os


environ = 'source ../env/bin/activate'
python_command = 'python manage.py'

backend = '{} runserver'.format(python_command)
celery = 'celery -A backend worker -l INFO -P threads'
beat = 'celery -A backend beat -l INFO'

commands = [backend, celery, beat]

for command in commands:
    os.system("gnome-terminal -e 'bash -c \" {} && {} \" ' ".format(environ, command))