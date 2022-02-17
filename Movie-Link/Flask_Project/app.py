# Python standard libraries
import json
import os
import sqlite3
import random
import smtplib
import ssl


# Third party libraries

from flask import Flask, redirect, request, url_for, render_template
from flask import jsonify
try:
    from model import parseRowFriends
    from model import parseTopMovies
    from model import parseSession
    from model import parseFriendsEmails
    from model import constructNewMovielist
    from model import constructNewSessionList
    from model import sendEmail
    from model import constructUserList
    from model import constructNewFriendList
    from model import getTopMovies
    from model import renderUserHome
    from model import renderMovie
    from model import findMovies
    from model import parseAllMovies
    from user import User
    # from db import init_db_command
except Exception:
    from Flask_Project.model import parseRowFriends
    from Flask_Project.model import parseTopMovies
    from Flask_Project.model import parseSession
    from Flask_Project.model import parseFriendsEmails
    from Flask_Project.model import constructNewMovielist
    from Flask_Project.model import constructNewSessionList
    from Flask_Project.model import sendEmail
    from Flask_Project.model import constructUserList
    from Flask_Project.model import constructNewFriendList
    from Flask_Project.model import getTopMovies
    from Flask_Project.model import renderUserHome
    from Flask_Project.model import renderMovie
    from Flask_Project.model import findMovies
    from Flask_Project.model import parseAllMovies
    from Flask_Project.user import User
    # from Flask_Project.db import init_db_command

from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests


# Configuration
GOOGLE_CLIENT_ID = "903645435965-sai5lsrvdkdbso16d1o3c35vthocqmap.apps" \
    ".googleusercontent.com"
GOOGLE_CLIENT_SECRET = "P2jL2nxQeAnuGoaFHLrCMALM"
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.unauthorized_handler
def unauthorized():
    return "You must be logged in to access this content.", 403


'''

# Naive database setup: Note, include this if you want to create a databsae
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass

'''
# OAuth2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)


# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    # I think this is where I set the current_user.
    # It uses this as a helper so whenever I call curren_user,
    # it calls this info
    # so now current_user is whatever User.get() returns
    return User.get(user_id)


@app.route("/")
def index():

    if current_user.is_authenticated:
        return (
            redirect(url_for("user_home")))

    else:
        # return '<a class="button" href="/login">Google Login</a>'

        return(redirect(url_for("home")))


@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in our db with the information provided
    # by Google
    # This is where I put it to my end, the User db---------------------------

    # Doesn't exist? Add to database
    # The following are temporary. Make into '' after.
    # Logic why is that if it doesn't exist, I add it, if it does exist: I
    # change user to point to what is in there.
    user = User(
        id_=unique_id,
        name=users_name,
        email=users_email,
        profile_pic=picture,
        movieList='',
        wishList='',
        friendList='',
        sessionList='')
    if not User.get(unique_id):
        # TODO:change the text here into just '' aka empty string
        # If it doesn't exist, add it to the database itself
        User.create(
            unique_id,
            users_name,
            users_email,
            picture,
            movieList='',
            wishList='',
            friendList='',
            sessionList='')
        print('creating user')
    else:
        # This means the user already exists,
        # so I need to change the user object.
        # User.get() method gives me it if I provide the unique ID
        user = User.get(unique_id)
    login_user(user)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route('/getAllFriends')
@login_required
def getAllFriends():
    user = User.getFriends(current_user.id)  # name1:email1,name2:email2
    friends_list = parseRowFriends(user)
    return jsonify(friends_list)


@app.route('/getTop')
@login_required
def getUserTopWishList():
    user = User.getMovieWishlist(current_user.id)
    wishlist = parseTopMovies(user)
    return jsonify(wishlist)


@app.route('/getMovies')
@login_required
def getUserMovies():
    user = User.getMovieWishlist(current_user.id)
    wishlist = parseAllMovies(user)
    return jsonify(wishlist)


@app.route('/getSessions')
@login_required
def getUserSessions():
    user = User.getSessions(current_user.id)
    session_list = parseSession(user)
    return jsonify(session_list)


@app.route('/getFriendsEmail')
@login_required
def getUserFriendsEmail():
    user = User.getFriends(current_user.id)
    email_list = parseFriendsEmails(user)
    return jsonify(email_list)


# expected input {movie: "dragon ball"}
@app.route('/addToWishlist', methods=['GET', 'POST'])
@login_required
def addMovieToWishlist():

    movie_info = request.get_json()  # get movie name from JSON body
    movie_info = movie_info['movieName']
    current_movies = User.getMovieWishlist(
        current_user.id)  # get all movies from wishlist
    updated_movies = constructNewMovielist(current_movies, movie_info)
    user = User.addToWishlist(current_user.id, updated_movies)

    if(user):
        return jsonify({'message': 'True'})

    return jsonify({'message': 'False'})


# example {session: "movieName1,03282020-10:30-PM,link"}
@app.route('/makeSession', methods=['GET', 'POST'])
@login_required
def createSession():
    session_info = request.get_json()['session']
    current_sessions = User.getSessions(current_user.id)
    updated_user_sessions = constructNewSessionList(
        current_sessions, session_info)
    user = User.addSessionToWishlist(current_user.id, updated_user_sessions)
    user = User.getFriends(current_user.id)  # name1:email1,name2:email2
    friend_list = parseFriendsEmails(user)
    friend_list.append(current_user.email)
    sendEmail(friend_list, session_info)
    if(user):
        return jsonify({'message': 'True'})

    return jsonify({'message': 'False'})

# @app.route('/searchUser', methods=['GET','POST'])


@app.route('/searchUser/<friend_name>')
@login_required
def searchUser(friend_name):

    # user_info = request.get_json()
    user_info = friend_name
    print(user_info)
    current_users = User.getAll()

    # return jsonify({"usernames": matching_users, "emails": matching_emails,
    # 'images':matching_pics})

    if friend_name is not None:
        temp = constructUserList(current_users, user_info, current_user.id)
        for i in range(len(temp[0])):
            if temp[0][i] == current_user.name:
                temp[0].pop(i)
                temp[1].pop(i)
                temp[2].pop(i)
    else:
        temp = []

    temp = constructUserList(current_users, user_info, current_user.id)
    return render_template(
        'friendSearch.html',
        friend_list=temp[0],
        username=current_user.name,
        email_list=temp[1],
        img_list=temp[2])
    # return jsonify({"usernames": matching_users, "emails": matching_emails})

    # return jsonify(constructUserList(current_users,user_info))


# Sample input {"name":"Bob","email":"Bob@email.com"}
@app.route('/addFriend', methods=['GET', 'POST'])
@login_required
def addUserFriend():  # need to add some more error checking here
    friend_info = request.get_json()['name']
    email_info = request.get_json()['email']
    current_friends_emails = User.getFriends(
        current_user.id)  # get all movies from wishlist
    updated_friends_list = constructNewFriendList(
        current_friends_emails, friend_info, email_info)
    user = User.addFriend(current_user.id, updated_friends_list)

    if(user):
        return jsonify({'message': 'True'})

    return jsonify({'message': 'False'})


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route('/home')
def home():

    # Displays 9 random movies
    # Allows you to sign in
    top = getTopMovies()

    return render_template('home.html', popular=top[0], image_test=top[1])


@app.route('/getPopular')
def getPopular():
    temp = ""
    top = getTopMovies()
    for movie in top[0]:
        temp += str(movie) + ","
    temp = temp[0:len(temp) - 1]

    return jsonify(temp)


@app.route('/user_home')
@login_required
def user_home():

    user_movies = User.getMovieWishlist(current_user.id)
    user_friends = User.getFriends(current_user.id)
    temp = renderUserHome(user_movies, user_friends)

    return render_template(
        'user_home.html',
        popular=temp[0],
        username=current_user.name,
        movieList=temp[1],
        friendList=temp[2],
        image_test=temp[3],
        profile_pic=current_user.profile_pic)


@app.route('/movie_search/<movie_name>')
@login_required
def movie_search(movie_name):

    possible_movies = findMovies(movie_name)

    return render_template(
        'search.html',
        movie_list=possible_movies,
        username=current_user.name)


@app.route('/session_list')
@login_required
def session_list():

    user = User.getSessions(current_user.id)

    sessionList = parseSession(user)

    # returning sessions
    return render_template(
        'session_list.html',
        sessionList=sessionList['sessions'])


@app.route('/movieView/<movieID>')
@login_required
def movieDisplay(movieID):

    # throwing error due to renderMovie on search
    temp = renderMovie(movieID)
    return render_template(
        'view.html',
        movie_title=temp[0],
        img_url=temp[1],
        movie_info=temp[2],
        release_date=temp[3])


if __name__ == "__main__":
    app.run(ssl_context="adhoc")
