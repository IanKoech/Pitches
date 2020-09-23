from app import create_app, db
from flask_script import Manager, Server
from  flask_migrate import Migrate, MigrateCommand
from app.models import User,Pitch,Comment

app=create_app('production')
#Using test config above to test database URI


manager=Manager(app)
manager.add_command('server', Server)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

def test():
    """Run unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.shell
def make_shell_context():
    #Method allows us to pass in some properties into our shell
    return dict(app = app,db = db,User = User, Pitch = Pitch ,Comment=Comment)
if __name__ == '__main__':
    manager.run()
#Import create_app function from app folder and import Manger class from flask script
#Manager class will initialize our extension and server class that helps us launch our server
#We instantiate Manager class by passing in app instance
#Command line argument tells us how to run our application
#add_command()  creates a new command 'server' that launches our application server