from imdb import IMDb
import random
import smtplib


def parseRowFriends(user):
    list_row = []
    for row in user:
        if len(row) > 3:
            data = row.split(',')  # [name1:email1,name2:e,email2]
            for item in data:
                list_row.append(item.split(':')[0])
    return {'friends': list_row}


def parseTopMovies(user):
    wishlist = []
    favs = ''
    for row in user:
        favs = row
    favsList = favs.split(',')

    if len(favsList) >= 10:
        wishlist = {'wishlist': favsList[0:9]}
    else:
        wishlist = {'wishlist': favsList}
    return wishlist


def parseAllMovies(user):
    wishlist = []
    favs = ''
    for row in user:
        favs = row
    wishlist = {'wishlist': favs.split(',')}
    return wishlist


def parseSession(user):
    sessionList = []
    sessions = ''
    for row in user:
        sessions = row

    sessionList = {'sessions': sessions.split('%')}
    return sessionList


def parseFriendsEmails(user):
    email_list = []
    for row in user:
        if len(row) > 3:
            emails = row.split(',')
            for email in emails:
                if ':' in email:
                    email_list.append(email.split(':')[1])
    return email_list


def constructNewMovielist(current_movies, movie_info):
    updated_movies = ''
    # check if some movies already exist
    if current_movies is not None:
        # if some movies exist then make a new String of movies
        for all_movies in current_movies:
            updated_movies = all_movies

        if len(movie_info) == 0:
            return updated_movies
        elif len(updated_movies) > 0:
            # in case dbs doesn't return None & no movies to report
            updated_movies += ',' + movie_info
        else:
            updated_movies = movie_info
    else:
        updated_movies = movie_info
    return updated_movies



def constructNewSessionList(current_sessions_row, session_info):
    if len(session_info) > 0 and ',' in session_info:
        info = session_info.split(',')
        if len(info) > 2:
            if "https://" not in info[2] or "zoom" not in info[2]:
                session_info = 'Invalid link. Try again.'
    updated_user_sessions = ''
    current_sessions = ''

    if current_sessions_row is not None:
        for session in current_sessions_row:
            updated_user_sessions = session

        if len(updated_user_sessions) == 0:
            return session_info
        if len(session_info) == 0:
            return updated_user_sessions
        elif len(updated_user_sessions) > 0:
            updated_user_sessions += '%' + session_info
        else:
            updated_user_sessions = session_info
    else:
        updated_user_sessions = session_info
    return updated_user_sessions


def constructUserList(current_users, user_info, user_id):
    usernames = []
    useremails = []
    profile_pics = []
    ids = []
    matching_users = []
    matching_emails = []
    matching_pics = []

    if len(user_info) == 0:
        return (matching_users, matching_emails, matching_pics)

    if current_users is None:  # needs to return a diff template
        return (matching_users, matching_emails, matching_pics)

    for row in current_users:
        ids.append(row[0])
        usernames.append(row[1])
        useremails.append(row[2])
        profile_pics.append(row[3])

    for i in range(0, len(usernames)):
        if user_info in usernames[i] and user_id != ids[i]:
            matching_users.append(usernames[i])
            matching_emails.append(useremails[i])
            matching_pics.append(profile_pics[i])

    return (matching_users, matching_emails, matching_pics)


def constructNewFriendList(current_friends_emails, friend_info, email_info):
    updated_friends = []
    updated_emails = []
    updated_friends_list = ''
    if current_friends_emails is not None:
        for all_info in current_friends_emails:
            # if some friends exist then make a new String of friends
            if len(all_info) > 3:
                all_friends = all_info.split(',')
                # makes the form friend1:email1, friend2:email2, ...
                for friend in all_friends:
                    friend_data = friend.split(':')
                    # [friend1, email1]
                    updated_friends.append(friend_data[0])
                    updated_emails.append(friend_data[1])

    if len(friend_info) != 0 and len(email_info) != 0:
        updated_emails.append(email_info)
        updated_friends.append(friend_info)

    for i in range(0, len(updated_friends)):
        updated_friends_list += updated_friends[i] + ':' + updated_emails[i]
        if i < len(updated_friends) - 1:
            updated_friends_list += ','
    return updated_friends_list


def sendEmail(friend_list, session_info):
    valid_send = "invalid"
    for friend in friend_list:
        port = 587
        receiver_email = friend

        print("Recipients:" + receiver_email)

        # substitute with real Zoom link
        message = """\
        MovieLink Zoom Session

        Info:""" + session_info

        info = session_info.split(",")

        # requirements for valid Zoom link
        if "https://" not in info[2] or "zoom" not in info[2]:
            message = """\
            MovieLink Zoom Session
            Info:""" + "\nInvalid link input"

        with smtplib.SMTP("smtp.gmail.com", port) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login("thesnakepie@gmail.com", "kztxyadebjhbhezi")
            server.sendmail("thesnakepie@gmail.com", receiver_email, message)
            valid_send = "valid"

    return valid_send


def getTopMovies():
    ia = IMDb()
    top = ia.get_top250_movies()
    popular_movies = []
    image_urls = []

    for _i in range(0, 9):

        a = random.randint(0, 249)
        popular_movies.append(top[a])

        movie = ia.search_movie(str(top[a]))
        image_urls.append(movie[0].data['cover url'])
    return (popular_movies, image_urls)


def renderUserHome(user_movies, user_friends):
    ia = IMDb()
    top = ia.get_top250_movies()
    popular_movies = []
    image_urls = []
    for _i in range(0, 9):
        a = random.randint(0, 249)
        popular_movies.append(top[a])
        movie = ia.search_movie(str(top[a]))
        image_urls.append(movie[0].data['cover url'])

    # user = User.getMovieWishlist(current_user.id)
    # for row in user:
    #     movies = row
    # wishList = movies.split(',')

    wishlist = parseAllMovies(user_movies)['wishlist']
    friends_list = parseRowFriends(user_friends)['friends']

    return(popular_movies, wishlist, friends_list, image_urls)


def findMovies(movie_name):
    ia = IMDb()
    # temporary, should allow user to custom search a specific movie..
    movie = ia.search_movie(movie_name)
    print(movie)

    possible_movies = []

    for i in range(len(movie)):
        possible_movies.append(movie[i])

    return possible_movies


def renderMovie(movieID):
    ia = IMDb()
    movie = ia.get_movie(movieID)
    info = movie['plot']
    title = movie['title']
    imgUrl = movie['cover url']
    rDate = movie['year']

    return (title, imgUrl, info, rDate)
