from flask import render_template, redirect, url_for, request, flash, jsonify
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

RESULTS_PER_PAGE = 5

# video upload handling
from werkzeug import secure_filename
from flask import send_from_directory
import os
from flask import current_app as application


# LOGIN

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
    # because routes are now in the main blueprint object, we do our redirects
    # with main.index, which is getting the index.html file from main 
    # blueprint. Blueprints allow namespacing to happen, so we are namespacing
    # the endpoint names what if two or more blueprints have an index route?
    # Flask handles that by namespacing the endpoint names, which is why we
    # need to say main.index to get to the specific views in a particular
    # blueprint (which is main, as that is the only blueprint right now).

    return redirect(url_for('main.index'))

# NEED TO CONNECT TO DATABASE, UPDATE DATABASE!!!
# registration
@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        User.register(form.username.data, form.email.data, form.password.data)
        flash('Thanks for registering')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)



# index route
@main.route('/')
def index():
    return render_template('index.html')



@main.route('/AJAXtest', methods=['GET', 'POST'])
def AJAXtest():
    '''test for AJAX response. 
    open JS console in browser on any page of app, then try: 
       > $.post("/AJAXtest", { username: "hello"  });
       or
       > $.get("/AJAXtest");    
    '''
    print "AJAXtest() called"
    if request.method == 'POST':
        print("POST method called")
        print(request.form['username'])
        return (request.form['username'])
    return "GET method called"


#@main.route('/videosearch', methods=['GET', 'POST'])
#@login_required
#def videosearch():
#    tagform = TagSearchForm()

#    if tagform.validate_on_submit():
#        user_tag = tagform.tag.data
#        parser_input = input_cleanup.input_prep(user_tag)
#        video_package = video_feed_parser.load(parser_input)
#        # send video_package to search result db
#        # return render_template('videofeed.html', video_package=video_package)
        
#        # delete entries in db after pages are created? delete entries after user session is done?


#    return render_template('videosearch.html', tagform=tagform)



@main.route('/feed/<user_tag>', methods=['GET'])
@login_required
def feed(user_tag):
    '''
    creating feed URL with user_tag collected in /proctected view function so 
    could be http://127.0.0.1:8000/feed/boxing the first feed url with videos
    is technically page one, but we do not see the page value until page 2
    (when user clicks next button) then we will see url like:
    http://127.0.0.1:8000/feed/boxing?page=2
    But these urls are created via url_for() functions attached to the prev and
    next buttons in the videofeed.html template the url_for() functions
    attached to the previous and next buttons are essentially creation a loop
    wherein the user clicks, for example, the next button, then url_for()
    generates the url for main.feed, passing in the user_tag and page number
    (that is either incremented or decremented, for next and previous). Due to
    Flask architecture, when the client GETs the url generated by url_for() for
    main.feed, this feed() view function is called (with the tag passed back in)
    and the page object in feed() gets the current page number in the url 
    (tag?page=2)
    (((apparently even though we have hard-coded in ('page', 1), request.args.get() does
    get the current value for the page argument in the URL...and the first render
    of the view, because there is no page argument in the URL, defaults to 1.
    Why? Consider the following: 
        >>>page = {} #page is an empty dictionary
        >>>foo = page.get('page') #try getting non-existent key
        >>>print(foo)
        None
        >>>foo = page.get('page', 23) #trying to access value for non-existent
        key 'page' in page dict but also providing alternative argument of 23 to get()
        >>>print(foo)
        23
        So, in this scenario, foo becomes equal to 23 as page.get('page') 
        evaluates to nothing (not None, but literally, nothing)
         ))) 
    Also note:
    according to docs for flask.url_for(endpoint, **values), because in the 
    videofeed.html template for the next and previous buttons we have 
    page=(page - 1) or page=(page + 1), and page is not an argument taken by
    the feed() endpoint, we end up with ?page=2 in the URL. This is because 
    (http://flask.pocoo.org/docs/0.10/api/#flask.url_for) any variables 
    arguments not included in the endpoint are appended to the generated URL
    as a query argument The new page number accessed by page object in feed(),
    together with the RESULTS_PER_PAGE value are passed to video_feed_parser
    for the start, stop values in our slice operation on the feed API url.

    '''

    page = request.args.get('page', 1)
    print("THIS IS page in feed(): %s" % page)
    parser_input = input_cleanup.input_prep(user_tag)
    #converting page from Unicode to int for passing to d.entries slice operation in load()
    page = int(page)
    
    #sending user submitted tag to ovp API link, as well as page and RESULTS_PER_PAGE values for slicing response from API link
    video_package = video_feed_parser.load(parser_input, page, RESULTS_PER_PAGE)

    # this is rendering the videofeed.html template but still at the /protected URL. Can send POST data (the user submitted tag) via redirect to /videofeed endpoint?
    # return render_template('videofeed.html', video_id=video_id)

    # sending video_package, current page number, and tag objects
    return render_template('videofeed.html', video_package=video_package, page=page, tag=user_tag)




@main.route('/videosearch', methods=['GET', 'POST'])
@login_required
def videosearch():
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

        # send user-submitted text to input_cleanup function before sending to parser
        return redirect(url_for('main.feed', user_tag=user_tag))


        # return redirect(url_for('main.videofeed', video_id=video_id))
        # return redirect(url_for('main.videofeed', video_id=video_id))
    return render_template('videosearch.html', tagform=tagform)


# for video file uploading
# these should be in config file!!! They are, but not available to routes.py
# DATABASE_URI and DATABASE_URL work because they are exported as environment variables
ALLOWED_EXTENSIONS = set(['mov', 'mp4', 'mpeg', 'mpg', 'flv', 'avi'])
UPLOAD_FOLDER = "/app/ovpAPI/uploads"
MAX_CONTENT_LENGTH = 900 * 1024 * 102
UPLOAD_FOLDER_GET = "/app/ovpAPI/uploads" 


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@main.route('/upload', methods=['GET', 'POST'])
def upload():
    '''
    AJAX in upload.html is handling POST and redirect to main.upload_file
    '''
    if request.method == 'POST':
        file = request.files['uploaded_file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('main.uploaded_file', filename=filename))
    return render_template('upload.html')



@main.route('/uploads/<filename>')
def uploaded_file(filename):
    root_dir = os.path.dirname(os.getcwd())
    print(root_dir)
    return send_from_directory(os.path.join(root_dir, 'ovp-frontend-heroku','app', 'ovpAPI', 'uploads'), filename)
    # return send_from_directory('/Users/mdublin1/Downloads/ovp-frontend-heroku/app/ovpAPI/uploads/', filename)



# new video upload w/AJAX


from ..ovpAPI.DI import BC
from ..ovpAPI.DI import uploader
from ..ovpAPI import AWS_S3_test

@main.route('/videoupload', methods=['GET', 'POST'])
@login_required
def videoupload():
    '''
    receiving ImmutableMultiDict from AJAX POST request in videoupload.html
    /http://werkzeug.pocoo.org/docs/0.11/datastructures/#werkzeug.datastructures.MultiDict

    '''
    if request.method == 'POST':
        print("POST CALLED!")
        try:
            print("THIS IS request.form")
            print request.form
            video_meta_data = dict((key, request.form.getlist(key)) for key in request.form.keys())
            videofile = request.files['file_attach']
            # send video metadata to uploader.py 
            #video_meta_data = uploader.meta_parser(data)
           #print(video_meta_data)

            if videofile and allowed_file(videofile.filename):
                filename = secure_filename(videofile.filename)
                # saving video file in local file system
                videofile.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
                # calling AWS S3 script to upload file to S3 bucket, which returns public URL of file
                video_asset_url = AWS_S3_test.AWSConnector(filename)
                print(video_asset_url)

                # send clean up metadata
                getMetaData = uploader.BCDI(video_meta_data)
                # send metadata and source file URL to BC.py
                push_to_ovp = BC.createAndIngest(getMetaData, video_asset_url)

                return jsonify(message=push_to_ovp)

            return jsonify(message='hello')
            
        except Exception, e:
            print e
    return render_template('videoupload.html')



@main.route('/uploadsuccess', methods=['GET', 'POST'])
def uploadsuccess():
    return render_template('uploadsuccess.html')



################################## ENDPOINT TESTS ##################################

# ajax example
@main.route('/ajaxtest', methods=['GET','POST'])
def ajaxtest():
    return render_template('ajaxtest.html')

# jsonify example
@main.route('/get_current_user')
def get_current_user():
    test = {
    "username": "admin",
    "email": "admin@localhost",
    "id": 42
}
    return jsonify(test)


# for testing MDN example of AJAX upload using FormData object 
@main.route('/FormDataTest', methods=['GET', 'POST'])
def FormDataTest():
    if request.method == 'POST':
        print("POST CALLED!")
        try:
            print request.form
            data = dict((key, request.form.getlist(key)) for key in request.form.keys())
            print(data)
            videofile = request.files['file_attach']
            print(videofile.filename)

            # send video metadata to uploader.py
            #uploader.meta_parser(data)

            if videofile and allowed_file(videofile.filename):
                filename = secure_filename(videofile.filename)
                videofile.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
                #return redirect(url_for('main.uploadsuccess'))
            #print("before jsonify")
            #return jsonify(message="Hello!")
            
        except Exception, e:
            print e
    
    return render_template('FormDataTest.html')



