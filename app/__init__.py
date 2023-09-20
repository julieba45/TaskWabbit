import os
from flask import Flask, render_template, request, session, redirect, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect, generate_csrf
from flask_login import LoginManager, login_required
from .models import db, User, Review
from .api.user_routes import user_routes
from .api.auth_routes import auth_routes
from .api.tasktypes_routes import tasktype_routes
from .api.review_routes import review_routes
from .api.taskers_routes import taskers_routes
from .api.task_routes import task_routes
from .api.tasker_profile_routes import tasker_profile_routes
from .seeds import seed_commands
from .config import Config
from .forms.review_form import ReviewForm

app = Flask(__name__, static_folder='../react-app/build', static_url_path='/')

# Setup login manager
login = LoginManager(app)
login.login_view = 'auth.unauthorized'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


# Tell flask about our seed commands
app.cli.add_command(seed_commands)

app.config.from_object(Config)
app.register_blueprint(taskers_routes, url_prefix='/api/taskers')
app.register_blueprint(user_routes, url_prefix='/api/users')
app.register_blueprint(auth_routes, url_prefix='/api/auth')
app.register_blueprint(tasktype_routes, url_prefix='/api/tasktype')
app.register_blueprint(review_routes, url_prefix='/api/reviews')
app.register_blueprint(task_routes, url_prefix='/api/tasks')
app.register_blueprint(tasker_profile_routes, url_prefix='/api/taskerTaskTypes')
db.init_app(app)
Migrate(app, db)

# Application Security
CORS(app)


# Since we are deploying with Docker and Flask,
# we won't be using a buildpack when we deploy to Heroku.
# Therefore, we need to make sure that in production any
# request made over http is redirected to https.
# Well.........
@app.before_request
def https_redirect():
    if os.environ.get('FLASK_ENV') == 'production':
        if request.headers.get('X-Forwarded-Proto') == 'http':
            url = request.url.replace('http://', 'https://', 1)
            code = 301
            return redirect(url, code=code)


@app.after_request
def inject_csrf_token(response):
    response.set_cookie(
        'csrf_token',
        generate_csrf(),
        secure=True if os.environ.get('FLASK_ENV') == 'production' else False,
        samesite='Strict' if os.environ.get(
            'FLASK_ENV') == 'production' else None,
        httponly=True)
    return response


@app.route("/api/docs")
def api_help():
    """
    Returns all API routes and their doc strings
    """
    acceptable_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    route_list = { rule.rule: [[ method for method in rule.methods if method in acceptable_methods ],
                    app.view_functions[rule.endpoint].__doc__ ]
                    for rule in app.url_map.iter_rules() if rule.endpoint != 'static' }
    return route_list


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def react_root(path):
    """
    This route will direct to the public directory in our
    react builds in the production environment for favicon
    or index.html requests
    """
    if path == 'favicon.ico':
        return app.send_from_directory('public', 'favicon.ico')
    return app.send_static_file('index.html')


# get all reviews by a tasker's id, Require Authentication: false
@app.route('/api/taskers/<int:tasker_id>/reviews')
def review_taker_id(tasker_id):
    """
    Query for review by tasker_id and returns all reviews in a list as dictonaries
    Require Authentication: false
    """
    taskers_reviews = Review.query.filter(Review.tasker_id == tasker_id)
    print(taskers_reviews)
    return {"Reviews": [review.to_dict_im() for review in taskers_reviews]}


# Create a Review for a Tasker based on the Tasker's id, Require Authentication: true
@app.route('/api/taskers/reviews', methods=['POST'])
@login_required
def createReview():
    """
    creates a review based on the tasker's id
    """
    form = ReviewForm()
    print(form, 'test form')
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        newReview = Review(
            description=form.data['description'],
            rating=form.data['rating'],
            tasker_id=form.data['tasker_id'],
            user_id=form.data['user_id'],
            task_id=form.data['task_id']
        )
        db.session.add(newReview)
        db.session.commit()

        return newReview.to_dict_im()
    return { 'Error': 'Error creating Review'}



@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')
