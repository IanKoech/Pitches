from . import db , login_manager
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_secure = db.Column(db.String(255))

    #Creating the relationship between user model and pitch model
    pitch = db.relationship('Pitch',backref = 'user',lazy = "dynamic")
    #db.ForeignKey argument tells SQlAlchemy that this is  a foreign key and it is the is the id of a role model
   

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

class Pitch(UserMixin,db.Model):
    __tablename__  =  'pitch'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    category = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    #Creating relationship between user and pitch
    comment=db.relationship('Comment',backref='',lazy="dynamic")
    #class methods below
    def save_pitch(self):
        '''
        Function that saves pitches
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all_pitches(cls):
        '''
        Function that queries the databse and returns all the pitches
        '''
        return Pitch.query.all()

    @classmethod
    def get_pitches_by_category(cls,category_id):
        '''
        Function that queries the databse and returns pitches based on the
        category 
        '''
        return Pitch.query.filter_by(category_id= category_id)


class Comment(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    comment= db.Column(db.String)
    pitch_id = db.Column(db.Integer,db.ForeignKey('pitch.id'))
    username =  db.Column(db.String)
    votes= db.Column(db.Integer)

    def save_comment(self):
        '''
        Function that saves comments
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def clear_comments(cls):
        Comment.all_comments.clear()

    @classmethod
    def get_comments(cls,id):
        comments = Comment.query.filter_by(pitch_id=id).all()

        return comments