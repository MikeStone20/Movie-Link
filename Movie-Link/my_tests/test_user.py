from sys import path
from os.path import dirname as dir
from Flask_Project.user import User
from Flask_Project.app import app
#path.append(dir(path[0]))


def test_get_all_exists(): #Return existing Users
    with app.app_context():
        User.reset()
        user = User(
            id_=1, name='ahmed1', email="ahmed1@columbia.edu",
            profile_pic="pic.jpg", movieList='Spiderman',
            wishList='Superman', friendList='Michael',
            sessionList='Spiderman%10/20/10%zoom.com'
        )

        User.create(user.id, user.name, user.email, user.profile_pic,
                    user.movieList, user.wishList, user.friendList,
                    user.sessionList)

        getUser = User.getAll()
        assert len(getUser) == 1

def test_get_all_empty(): # Get all Users when non exist
    with app.app_context():
        User.reset()
        getUser = User.getAll()
        assert len(getUser) == 0

#--------------------------------------------------------------------------

def test_get_exists(): # get when a user exists and use valid id
    with app.app_context():
        User.reset()
        user = User(
            id_=1, name='ahmed1', email="ahmed1@columbia.edu",
            profile_pic="pic.jpg", movieList='Spiderman',
            wishList='Superman', friendList='Michael',
            sessionList='Spiderman%10/20/10%zoom.com'
        )
        User.create(user.id, user.name, user.email, user.profile_pic,
                    user.movieList, user.wishList, user.friendList,
                    user.sessionList)

        getUser = User.get(user.id)

        temp1 = (user.id, user.name, user.profile_pic, user.movieList,
                 user.wishList, user.friendList, user.sessionList)

        temp2 = (int(getUser.id), getUser.name, getUser.profile_pic,
                 getUser.movieList, getUser.wishList, getUser.friendList,
                 getUser.sessionList)

        assert temp1 == temp2

def test_get_invalid_id(): # get when a user exists and use invalid id
    with app.app_context():
        User.reset()
        user = User(
            id_=1, name='ahmed1', email="ahmed1@columbia.edu",
            profile_pic="pic.jpg", movieList='Spiderman',
            wishList='Superman', friendList='Michael',
            sessionList='Spiderman%10/20/10%zoom.com'
        )
        User.create(user.id, user.name, user.email, user.profile_pic,
                    user.movieList, user.wishList, user.friendList,
                    user.sessionList)

        getUser = User.get('2')
        getUser == None

def test_get_no_users(): #given id and no users
    with app.app_context():
        User.reset()
        getUser = User.get('1')
        assert getUser == None


def test_get_none(): # input None so we return None
    with app.app_context():
        User.reset()
        user = User(
            id_=1, name='ahmed1', email="ahmed1@columbia.edu",
            profile_pic="pic.jpg", movieList='Spiderman',
            wishList='Superman', friendList='Michael',
            sessionList='Spiderman%10/20/10%zoom.com'
        )
        User.create(user.id, user.name, user.email, user.profile_pic,
                    user.movieList, user.wishList, user.friendList,
                    user.sessionList)

        getUser = User.get(None)

        assert getUser == None

def test_get_none_no_users(): # User gets None so we return None and no users
    with app.app_context():
        User.reset()
        getUser = User.get(None)
        assert getUser == None


def test_get_empty(): # empty String
    with app.app_context():
        User.reset()
        user = User(
            id_=1, name='ahmed1', email="ahmed1@columbia.edu",
            profile_pic="pic.jpg", movieList='Spiderman',
            wishList='Superman', friendList='Michael',
            sessionList='Spiderman%10/20/10%zoom.com'
        )
        User.create(user.id, user.name, user.email, user.profile_pic,
                    user.movieList, user.wishList, user.friendList,
                    user.sessionList)

        getUser = User.get('')
        assert getUser == None

def test_get_empty_no_users(): # empty String and no users
    with app.app_context():
        User.reset()
        getUser = User.get('')
        assert getUser == None

#--------------------------------------------------------------------------

def test_get_friends_friend_list(): # friend list isnt empty
    with app.app_context():
        User.reset()
        user = User(
            id_=1, name='ahmed1', email="ahmed1@columbia.edu",
            profile_pic="pic.jpg", movieList='Spiderman',
            wishList='Superman', friendList='Michael',
            sessionList='Spiderman%10/20/10%zoom.com'
        )
        User.create(user.id, user.name, user.email, user.profile_pic,
                    user.movieList, user.wishList, user.friendList,
                    user.sessionList)

        friends = User.getFriends('1')
        for i in friends:
            assert i == 'Michael'

def test_get_friends_invalid_id(): # friend list isnt empty but use invalid id
    with app.app_context():
        User.reset()
        user = User(
            id_=1, name='ahmed1', email="ahmed1@columbia.edu",
            profile_pic="pic.jpg", movieList='Spiderman',
            wishList='Superman', friendList='Michael',
            sessionList='Spiderman%10/20/10%zoom.com'
        )
        User.create(user.id, user.name, user.email, user.profile_pic,
                    user.movieList, user.wishList, user.friendList,
                    user.sessionList)

        friends = User.getFriends('2')
        friends == None

def test_get_friends_no_users(): # no users and non empty input
    with app.app_context():
        User.reset()
        friends = User.getFriends('1')
        assert friends == None

def test_get_friends_empty(): # get friends when user empty string
     with app.app_context():
        User.reset()
        user = User(
            id_=1, name='ahmed1', email="ahmed1@columbia.edu",
            profile_pic="pic.jpg", movieList='Spiderman',
            wishList='Superman', friendList='Michael',
            sessionList='Spiderman%10/20/10%zoom.com'
        )
        User.create(user.id, user.name, user.email, user.profile_pic,
                    user.movieList, user.wishList, user.friendList,
                    user.sessionList)

        friends = User.getFriends("")
        assert None == friends

def test_get_friends_no_users_empty(): #no users and empty input
    with app.app_context():
        User.reset()
        friends = User.getFriends('')
        assert friends == None

def test_get_friends_no_friends(): #user has no friends
    with app.app_context():
        User.reset()
        user = User(
            id_=1, name='ahmed1', email="ahmed1@columbia.edu",
            profile_pic="pic.jpg", movieList='Spiderman',
            wishList='Superman', friendList='',
            sessionList='Spiderman%10/20/10%zoom.com'
        )
        User.create(user.id, user.name, user.email, user.profile_pic,
                    user.movieList, user.wishList, user.friendList,
                    user.sessionList)

        friends = User.getFriends('1')
        for friend in friends:
            assert '' == friend

#--------------------------------------------------------------------------

def test_get_movie_wish_list_movie_list_exists(): # get wishlist when it exists
    with app.app_context():
        User.reset()
        user = User(
            id_=1, name='ahmed1', email="ahmed1@columbia.edu",
            profile_pic="pic.jpg", movieList='Spiderman',
            wishList='Superman', friendList='Michael',
            sessionList='Spiderman%10/20/10%zoom.com'
        )
        User.create(user.id, user.name, user.email, user.profile_pic,
                    user.movieList, user.wishList, user.friendList,
                    user.sessionList)

        movieWishlist = User.getMovieWishlist('1')
        for i in movieWishlist:
            assert i == 'Superman'

def test_get_movie_wish_list_movie_list_invalid_id(): # get wishlist but invalid id
    with app.app_context():
        User.reset()
        user = User(
            id_=1, name='ahmed1', email="ahmed1@columbia.edu",
            profile_pic="pic.jpg", movieList='Spiderman',
            wishList='Superman', friendList='Michael',
            sessionList='Spiderman%10/20/10%zoom.com'
        )
        User.create(user.id, user.name, user.email, user.profile_pic,
                    user.movieList, user.wishList, user.friendList,
                    user.sessionList)

        movieWishlist = User.getMovieWishlist('2')
        assert movieWishlist == None

def test_get_movie_wish_list_movie_no_user(): # get wishlist when no user
    with app.app_context():
        User.reset()
        movieWishlist = User.getMovieWishlist('1')
        movieWishlist == None

def test_get_movie_wish_list_movie_list_empty(): # user exists but no wishlist
    with app.app_context():
        User.reset()
        user = User(
            id_=1, name='ahmed1', email="ahmed1@columbia.edu",
            profile_pic="pic.jpg", movieList='',
            wishList='', friendList='Michael',
            sessionList='Spiderman%10/20/10%zoom.com'
        )
        User.create(user.id, user.name, user.email, user.profile_pic,
                    user.movieList, user.wishList, user.friendList,
                    user.sessionList)

        movieWishlist = User.getMovieWishlist('1')
        for i in movieWishlist:
            assert i == ''

def test_get_movie_wish_list_movie_list_no_id(): # user exists but empty id
    with app.app_context():
        User.reset()
        user = User(
            id_=1, name='ahmed1', email="ahmed1@columbia.edu",
            profile_pic="pic.jpg", movieList='Spiderman',
            wishList='Superman', friendList='Michael',
            sessionList='Spiderman%10/20/10%zoom.com'
        )
        User.create(user.id, user.name, user.email, user.profile_pic,
                    user.movieList, user.wishList, user.friendList,
                    user.sessionList)

        movieWishlist = User.getMovieWishlist('')
        assert movieWishlist == None

def test_get_movie_wish_list_movie_no_id_and_no_user(): # get wishlist when it exists
    with app.app_context():
        User.reset()
        movieWishlist = User.getMovieWishlist('')
        movieWishlist == None

#--------------------------------------------------------------------------

def test_get_sessions(): #test if we can get a session
    with app.app_context():
        User.reset()
        user = User(
            id_=1, name='ahmed1', email="ahmed1@columbia.edu",
            profile_pic="pic.jpg", movieList='Spiderman',
            wishList='Superman', friendList='Michael',
            sessionList='Spiderman%10/20/10%zoom.com'
        )
        User.create(user.id, user.name, user.email, user.profile_pic,
                    user.movieList, user.wishList, user.friendList,
                    user.sessionList)

        sessions = User.getSessions('1')
        for i in sessions:
            assert i == 'Spiderman%10/20/10%zoom.com'

def test_get_sessions_no_users(): #test if we can get a session with no users
    with app.app_context():
        User.reset()
        sessions = User.getSessions('1')
        assert sessions == None

def test_get_sessions_invalid_id(): #test if we can get a session but id is invalid
    with app.app_context():
        User.reset()
        user = User(
            id_=1, name='ahmed1', email="ahmed1@columbia.edu",
            profile_pic="pic.jpg", movieList='Spiderman',
            wishList='Superman', friendList='Michael',
            sessionList='Spiderman%10/20/10%zoom.com'
        )
        User.create(user.id, user.name, user.email, user.profile_pic,
                    user.movieList, user.wishList, user.friendList,
                    user.sessionList)

        sessions = User.getSessions('2')
        assert sessions == None

def test_get_sessions_empty_list(): #test if we can get a session but, session list is empty
    with app.app_context():
        User.reset()
        user = User(
            id_=1, name='ahmed1', email="ahmed1@columbia.edu",
            profile_pic="pic.jpg", movieList='Spiderman',
            wishList='Superman', friendList='Michael',
            sessionList=''
        )
        User.create(user.id, user.name, user.email, user.profile_pic,
                    user.movieList, user.wishList, user.friendList,
                    user.sessionList)

        sessions = User.getSessions('1')
        for session in sessions:
            assert session == ''

def test_get_sessions_empty_input(): #test if we can get a session but, id is empty
    with app.app_context():
        User.reset()
        user = User(
            id_=1, name='ahmed1', email="ahmed1@columbia.edu",
            profile_pic="pic.jpg", movieList='Spiderman',
            wishList='Superman', friendList='Michael',
            sessionList='Spiderman%10/20/10%zoom.com'
        )
        User.create(user.id, user.name, user.email, user.profile_pic,
                    user.movieList, user.wishList, user.friendList,
                    user.sessionList)

        sessions = User.getSessions('')
        assert sessions == None

#--------------------------------------------------------------------------

def test_addToWishlist_non_empty_list(): # add a movie to an existing wishlist
    with app.app_context():
        User.reset()
        user = User(
            id_=1, name='ahmed1', email="ahmed1@columbia.edu",
            profile_pic="pic.jpg", movieList='Spiderman',
            wishList='Superman', friendList='Michael',
            sessionList='Spiderman%10/20/10%zoom.com'
        )
        User.create(user.id, user.name, user.email, user.profile_pic,
                    user.movieList, user.wishList, user.friendList,
                    user.sessionList)

        User.addToWishlist('1', 'Superman,X-Men')
        wishList = User.get('1').wishList
        assert wishList == 'Superman,X-Men'

def test_add_to_wishlist__empty_list(): # add a movie to an empty wishlist
    with app.app_context():
        User.reset()
        user = User(
            id_=1, name='ahmed1', email="ahmed1@columbia.edu",
            profile_pic="pic.jpg", movieList='Spiderman',
            wishList='Superman', friendList='Michael',
            sessionList='Spiderman%10/20/10%zoom.com'
        )
        User.create(user.id, user.name, user.email, user.profile_pic,
                    user.movieList, user.wishList, user.friendList,
                    user.sessionList)

        User.addToWishlist('1', 'X-Men')
        wishList = User.get('1').wishList
        assert wishList == 'X-Men'

def test_addToWishlist_no_users(): # try adding to wishlist with no Users
    with app.app_context():
        User.reset()
        User.addToWishlist('1', 'Superman,X-Men')
        assert User.get('1') == None

def test_addToWishlist_empty_input(): # add an emptry string to wishlist
    with app.app_context():
        User.reset()
        user = User(
            id_=1, name='ahmed1', email="ahmed1@columbia.edu",
            profile_pic="pic.jpg", movieList='Spiderman',
            wishList='', friendList='Michael',
            sessionList='Spiderman%10/20/10%zoom.com'
        )
        User.create(user.id, user.name, user.email, user.profile_pic,
                    user.movieList, user.wishList, user.friendList,
                    user.sessionList)

        User.addToWishlist('1', '')
        wishList = User.get('1').wishList
        assert wishList == ''

def test_addToWishlist_invalid_id(): #User exists but id is invalid
    with app.app_context():
        User.reset()
        user = User(
            id_=1, name='ahmed1', email="ahmed1@columbia.edu",
            profile_pic="pic.jpg", movieList='Spiderman',
            wishList='Superman', friendList='Michael',
            sessionList='Spiderman%10/20/10%zoom.com'
        )
        User.create(user.id, user.name, user.email, user.profile_pic,
                    user.movieList, user.wishList, user.friendList,
                    user.sessionList)

        User.addToWishlist('2', 'Superman,X-Men')
        wishList = User.get('1').wishList
        assert wishList == "Superman"


#--------------------------------------------------------------------------

def test_addSessionToWishlist(): #add to existing list
    with app.app_context():
        User.reset()
        user = User(
            id_=1, name='ahmed1', email="ahmed1@columbia.edu",
            profile_pic="pic.jpg", movieList='Spiderman',
            wishList='Superman', friendList='Michael',
            sessionList='Spiderman%10/20/10%zoom.com'
        )
        User.create(user.id, user.name, user.email, user.profile_pic,
                    user.movieList, user.wishList, user.friendList,
                    user.sessionList)

        userSessions = 'Spiderman%10/20/10%zoom.com' * 2
        User.addSessionToWishlist('1', userSessions)
        sessionsList = User.get('1').sessionList
        assert userSessions == sessionsList

def test_add_Session_to_wishlist_empty(): #add to empty list empty list
    with app.app_context():
        User.reset()
        user = User(
            id_=1, name='ahmed1', email="ahmed1@columbia.edu",
            profile_pic="pic.jpg", movieList='Spiderman',
            wishList='Superman', friendList='Michael',
            sessionList=''
        )
        User.create(user.id, user.name, user.email, user.profile_pic,
                    user.movieList, user.wishList, user.friendList,
                    user.sessionList)

        userSessions = 'Spiderman%10/20/10%zoom.com' * 2
        User.addSessionToWishlist('1', userSessions)
        sessionsList = User.get('1').sessionList
        assert userSessions == sessionsList

def test_add_Session_to_wishlist_no_users(): #attempt to add when no users exist
    with app.app_context():
        User.reset()
        userSessions = 'Spiderman%10/20/10%zoom.com' * 2
        User.addSessionToWishlist('1', userSessions)
        assert None == User.get('1')

def test_add_Session_to_wishlist_empty_input(): #add empty string to sessions list
    with app.app_context():
        User.reset()
        user = User(
            id_=1, name='ahmed1', email="ahmed1@columbia.edu",
            profile_pic="pic.jpg", movieList='Spiderman',
            wishList='Superman', friendList='Michael',
            sessionList=''
        )
        User.create(user.id, user.name, user.email, user.profile_pic,
                    user.movieList, user.wishList, user.friendList,
                    user.sessionList)

        User.addSessionToWishlist('1', '')
        sessionsList = User.get('1').sessionList
        assert '' == sessionsList

def test_add_Session_to_wishlist_invalid_id(): #User exists but invalid id
    with app.app_context():
        User.reset()
        user = User(
            id_=1, name='ahmed1', email="ahmed1@columbia.edu",
            profile_pic="pic.jpg", movieList='Spiderman',
            wishList='Superman', friendList='Michael',
            sessionList=''
        )
        User.create(user.id, user.name, user.email, user.profile_pic,
                    user.movieList, user.wishList, user.friendList,
                    user.sessionList)

        User.addSessionToWishlist('2', 'Spiderman%10/20/10%zoom.com')
        sessionsList = User.get('1').sessionList
        assert '' == sessionsList

#--------------------------------------------------------------------------

def test_add_friend_existing(): #adding more friends
    with app.app_context():
        User.reset()
        user = User(
            id_=1, name='ahmed1', email="ahmed1@columbia.edu",
            profile_pic="pic.jpg", movieList='Spiderman',
            wishList='Superman', friendList='Michael',
            sessionList='Spiderman%10/20/10%zoom.com'
        )
        User.create(user.id, user.name, user.email, user.profile_pic,
                    user.movieList, user.wishList, user.friendList,
                    user.sessionList)

        User.addFriend('1', 'Michael,Alex')
        newFriends = User.get('1').friendList
        assert newFriends == 'Michael,Alex'

def test_add_friend_empty(): #adding first friend
    with app.app_context():
        User.reset()
        user = User(
            id_=1, name='ahmed1', email="ahmed1@columbia.edu",
            profile_pic="pic.jpg", movieList='Spiderman',
            wishList='Superman', friendList='',
            sessionList='Spiderman%10/20/10%zoom.com'
        )
        User.create(user.id, user.name, user.email, user.profile_pic,
                    user.movieList, user.wishList, user.friendList,
                    user.sessionList)

        User.addFriend('1', 'Michael')
        newFriends = User.get('1').friendList
        assert newFriends == 'Michael'

def test_add_friend_no_users(): #adding friends when no other users exist
    with app.app_context():
        User.reset()
        User.addFriend('1', 'Michael')
        newFriends = User.get('1')
        assert newFriends == None

def test_add_friend_empty_input(): #adding empty string as friend
    with app.app_context():
        User.reset()
        user = User(
            id_=1, name='ahmed1', email="ahmed1@columbia.edu",
            profile_pic="pic.jpg", movieList='Spiderman',
            wishList='Superman', friendList='',
            sessionList='Spiderman%10/20/10%zoom.com'
        )
        User.create(user.id, user.name, user.email, user.profile_pic,
                    user.movieList, user.wishList, user.friendList,
                    user.sessionList)

        User.addFriend('1', '')
        newFriends = User.get('1').friendList
        assert newFriends == ''

def test_add_friend_invalid_id(): #adding friend to invalid id
    with app.app_context():
        User.reset()
        user = User(
            id_=1, name='ahmed1', email="ahmed1@columbia.edu",
            profile_pic="pic.jpg", movieList='Spiderman',
            wishList='Superman', friendList='',
            sessionList='Spiderman%10/20/10%zoom.com'
        )
        User.create(user.id, user.name, user.email, user.profile_pic,
                    user.movieList, user.wishList, user.friendList,
                    user.sessionList)

        User.addFriend('2', 'Michael')
        newFriends = User.get('1').friendList
        assert newFriends == ''
