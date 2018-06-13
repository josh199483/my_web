import os

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from app import create_app, mysql
from app.main.models import User, Role

apprun = create_app('development')  # ['development', 'production', 'testing']

manager = Manager(apprun)
def _make_context():
    return dict(app=apprun, db=mysql, User=User, Role=Role)

manager.add_command('db', MigrateCommand)
manager.add_command("shell", Shell(make_context=_make_context))

if __name__ == '__main__':
    manager.run()