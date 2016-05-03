from flask import render_template, redirect, url_for, request, flash
# TK: add context variables (session, g) and user login registration,
# login callback, load user data upon login, etc

from flask.ext.login import login_required, login_user, logout_user

# importing from upper directory models via .. notation
from ..models import User

# importing main, which is the blueprint object defined in the __init__.py
# file in this directory
from . import main
from .forms import LoginForm, TagSearchForm, RegistrationForm
from ..parser import video_feed_parser, input_cleanup


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            return redirect(url_for('main.login', **request.args))
        login_user(user, form.remember_me.data)
        return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('login.html', form=form)


# logout route
# instead of sayin app.route() we are saying main.route() because all the
# routes are contained in our main blueprint object (the blueprint is a
# global variable, like app used to be before we instantiated app inside
# the create_app() factory function in app/__init__.py file.
@main.route('/logout')
@login_required
def logout():
    logout_user()
    # because routes are now in the main blueprint object, we do our redirects with main.index, which is getting the index.html file from main blueprint.
    # blueprints allow namespacing to happen, so we are namespacing the endpoint names
    # what if two or more blueprints have an index route? Flask handles that
    # by namespacing the endpoint names, which is why we need to say
    # main.index to get to the specific views in a particular blueprint (which
    # is main, as that is the only blueprint right now).

    return redirect(url_for('main.index'))



from ..models import User
# NEED TO CONNECT TO DATABASE, UPDATE DATABASE!!!
# registration
@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        User.register(form.username.data, form.email.data, form.password.data)
        #user = User(form.username.data, form.email.data, form.password.data)
        #db_session.add(user)
        #db.add(user)
        flash('Thanks for registering')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)



# index route
@main.route('/')
def index():
    return render_template('index.html')


# videofeed route
@main.route('/videofeed')
#@app.route('/videofeed')
def videofeed(video_id):
    return render_template('videofeed.html', video_id=video_id)


#@main.route('/protected')
#@login_required
# def protected():
#    return render_template('protected.html')

# new:
@main.route('/protected', methods=['GET', 'POST'])
@login_required
def protected():
    tagform = TagSearchForm()

    if tagform.validate_on_submit():
        # the actual user-submitted text in the tag field is accessed this way (it is a Unicode object)
        # extracting from type <class 'wtforms.widgets.core.HTMLString'> object
        # POST request sends this via tagform.tag object: <input id="tag"
        # name="tag" type="text" value="THIS IS A TAG">
        user_tag = tagform.tag.data

        # call to feed parser
        #video_id = video_feed_parser.load(user_tag)
        #video_package = video_feed_parser.load(user_tag)
        # print(video_package)

        # call to input_cleanup function before sending to parser
        parser_input = input_cleanup.input_prep(user_tag)
        video_package = video_feed_parser.load(parser_input)

       # this is rendering the videofeed.html template but still at the /protected URL. Can send POST data (the user submitted tag) via redirect to /videofeed endpoint?
        # return render_template('videofeed.html', video_id=video_id)

        return render_template('videofeed.html', video_package=video_package)

        # return redirect(url_for('main.videofeed', video_id=video_id))
        # return redirect(url_for('main.videofeed', video_id=video_id))

    return render_template('protected.html', tagform=tagform)
