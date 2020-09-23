
from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import UpdateProfile,PitchForm,CommentForm
from flask_login import login_required,current_user
from ..models import Pitch, User, Comment
from .. import db, photos
import markdown2  


# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''

    title = 'MAKE YOUR PITCH'
    tech = Pitch.query.filter_by(category='tech')
    funny = Pitch.query.filter_by(category='funny')
    life = Pitch.query.filter_by(category='life')

    return render_template('index.html',title = title,tech=tech,funny=funny,life=life)


@main.route('/life', methods = ['GET','POST'])
def pitch():

    '''
    View pitch page function that returns the pitch details page and its data
    '''
    form = PitchForm()

    if form.validate_on_submit():
        
        new_pitch = Pitch(category=form.category.data,content=form.content.data)
        db.session.add(new_pitch)
        db.session.commit()

    life = Pitch.query.filter_by(category='life')

    return render_template('life.html',title = 'life',life=life,form=form)
  

@main.route('/funny', methods = ['GET','POST'])
def funny():

    '''
    View pitch page function that returns the pitch details page and its data
    '''
    form = PitchForm()

    if form.validate_on_submit():
        
        new_pitch = Pitch(category=form.category.data,content=form.content.data)
        db.session.add(new_pitch)
        db.session.commit()

    funny = Pitch.query.filter_by(category='funny')

    return render_template('funny.html',title = 'life',funny=funny,form=form)


@main.route('/tech', methods = ['GET','POST'])
def tech():

    '''
    View pitch page function that returns the pitch details page and its data
    '''
    form = PitchForm()

    if form.validate_on_submit():
        
        new_pitch = Pitch(category=form.category.data,content=form.content.data)
        db.session.add(new_pitch)
        db.session.commit()

    tech = Pitch.query.filter_by(category='tech')

    return render_template('tech.html',title = 'life',tech=tech,form=form)
  
@main.route('/pitch/pitch/new/', methods = ['GET','POST'])
@login_required
def new_pitch():
    form = PitchForm()

    if form.validate_on_submit():
        
        new_pitch = Pitch(category=form.category.data,content=form.content.data)
        db.session.add(new_pitch)
        db.session.commit()

    return render_template('new_pitch.html',title = 'new pitch', pitch_form=form, pitch=pitch)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)    

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))    