from sys import path
from os.path import dirname as dir
from Flask_Project.model import parseRowFriends, parseTopMovies, parseAllMovies, parseSession
from Flask_Project.model import constructNewMovielist, constructNewSessionList
from Flask_Project.model import constructUserList, getTopMovies, renderUserHome, renderMovie
from Flask_Project.model import parseFriendsEmails, constructNewFriendList, sendEmail
from Flask_Project.model import findMovies
path.append(dir(path[0]))


def test_parseRowFriendsExist(): # check to see if it works when people already exist
    sample_friends = ["person1:email1,person2:email2,person3:email3"]
    actual_results = parseRowFriends(sample_friends)
    assert actual_results['friends'] == ['person1', 'person2', 'person3']

def test_parseRowFriendsEmpty(): # check to see if it works when empty
    sample_friends = []
    actual_results = parseRowFriends(sample_friends)
    assert actual_results['friends'] == []

def test_parseRowFriendsExistInfali(): # check to see if it works when people already exist
    sample_friends = ["person1,person2,person3"]
    actual_results = parseRowFriends(sample_friends)
    assert actual_results['friends'] == ['person1', 'person2', 'person3']

def test_parseRowFriendsInvalidRow(): # invalid row
    sample_friends = ["person1;email1,person2;email2,person3;email3"]
    actual_results = parseRowFriends(sample_friends)
    assert actual_results['friends'] == ['person1;email1', 'person2;email2', 'person3;email3']

#--------------------------------------------------------------------------

def test_parseTopMovies(): # testing to see if we get all 10 moviess if there are only 10
    t = 'm,movie2,movie3,movie4,movie5,movie6,movie7,movie8,movie9,movie10'
    sample_movies = [t]
    actual_results = parseTopMovies(sample_movies)
    assert actual_results['wishlist'] == ['m', 'movie2', 'movie3',
                                          'movie4', 'movie5', 'movie6',
                                          'movie7', 'movie8', 'movie9']

def test_parseTopMoviesUnder10(): #if there are less than 10 movies
    sample_movies = ['movie1,movie2,movie3,movie4']
    actual_results = parseTopMovies(sample_movies)
    assert actual_results['wishlist'] == ['movie1', 'movie2',
                                          'movie3', 'movie4']

def test_parseTopMoviesOver10(): #if there is more than 10 movies
    sample_movies = ['movie1,movie2,movie3,movie4,movie5,movie6,movie7,movie8,movie9,movie10,movie11,movie12']
    actual_results = parseTopMovies(sample_movies)
    assert actual_results['wishlist'] == ['movie1', 'movie2',
                                          'movie3', 'movie4',
                                          'movie5', 'movie6',
                                          'movie7', 'movie8',
                                          'movie9']

def test_parseTopMoviesEmpty(): #check to see if the wishlist is empty
    sample_movies = []
    actual_results = parseTopMovies(sample_movies)
    assert actual_results['wishlist'] == ['']    

def test_parseTopMoviesInvalidRow(): # invalid row format
    t = 'm:movie2:movie3:movie4:movie5:movie6:movie7:movie8:movie9:movie10'
    sample_movies = [t]
    actual_results = parseTopMovies(sample_movies)
    assert actual_results['wishlist'] == ['m:movie2:movie3:movie4:movie5:movie6:movie7:movie8:movie9:movie10']

#--------------------------------------------------------------------------

def test_parseAllMovies(): #get all movies from the wishlist
    sample_movies = ['movie1,movie2,movie3,movie4,movie5,movie6,movie7,movie8,movie9,movie10,movie11,movie12']
    results = parseAllMovies(sample_movies)
    assert results['wishlist'] == ['movie1', 'movie2',
                                   'movie3', 'movie4',
                                   'movie5', 'movie6',
                                   'movie7', 'movie8',
                                   'movie9', 'movie10',
                                   'movie11','movie12']

def test_parseAllMoviesEmpty(): # if movie list was empty
    sample_movies = []
    actual_results = parseAllMovies(sample_movies)
    assert actual_results['wishlist'] == ['']

#--------------------------------------------------------------------------

def test_parseSession(): # check if we can parse sessions
    sample_session = ['movie1:time:link%movie1:time1:link']
    actual_results = parseSession(sample_session)
    assert actual_results['sessions'] == ['movie1:time:link',
                                          'movie1:time1:link']

def test_parseSessionEmpty(): # check if behavior if sessions list is empty
    sample_session = []
    actual_results = parseSession(sample_session)
    assert actual_results['sessions'] == ['']

def test_parseSessionInvalidRow(): # invalid row format
    sample_session = ['movie1;time;link;movie1;time1;link']
    actual_results = parseSession(sample_session)
    assert actual_results['sessions'] == ['movie1;time;link;movie1;time1;link']

#--------------------------------------------------------------------------

def test_parseFriendsEmails(): #if a user has friends return emails
    sample_friends_emails = ['friend1:email1,friend2:email2']
    actual_results = parseFriendsEmails(sample_friends_emails)
    assert actual_results == ['email1', 'email2']

def test_parseFriendsEmailsEmpty(): #friends list is empty
    sample_friends_emails = []
    actual_results = parseFriendsEmails(sample_friends_emails)
    assert actual_results == []

def test_parseFriendsEmailsInvalidRow(): #if a user has friends return emails
    sample_friends_emails = ['friend1;email1,friend2;email2']
    actual_results = parseFriendsEmails(sample_friends_emails)
    assert actual_results == []

#--------------------------------------------------------------------------


def test_constructNewMovielistOneMovie(): #add Movie to pre-existing list
    current_movies = ['movie1']
    movie_info = 'movie2'
    actual_results = constructNewMovielist(current_movies, movie_info)
    assert actual_results == 'movie1,movie2'

def test_constructNewMovielistEmpty(): # add Movie to an empty list
    current_movies = []
    movie_info = 'movie1'
    actual_results = constructNewMovielist(current_movies,movie_info)
    assert actual_results == 'movie1'

def test_constructNewMovielistInvalidList(): #invalid list
    actual_results = constructNewMovielist(None, 'movie1')
    assert actual_results == 'movie1'

def test_constructNewMovielistInvalidName(): # empty movie name
    current_movies = ['movie1']
    movie_info = ''
    actual_results = constructNewMovielist(current_movies,movie_info)
    assert actual_results == 'movie1'

def test_constructNewMovielistInvalidListAndInvalidName(): #invalid list and string
    actual_results = constructNewMovielist(None, '')
    assert actual_results == ''


#--------------------------------------------------------------------------

def test_constructNewSessionListAddOneSession(): #pre existing session list
    current_sessions = ['movie:link:time']
    session_info = 'movie2:link2:time2'
    actual_results = constructNewSessionList(current_sessions, session_info)
    assert actual_results == 'movie:link:time%movie2:link2:time2'

def test_constructNewSessionListAddToNone(): # current_sessions was None (retuned from the dbs)
    session_info = 'movie2:link2:time2'
    actual_results = constructNewSessionList(None, session_info)
    assert actual_results == 'movie2:link2:time2'

def test_constructNewSessionListAddEmpty(): # current_sessions is empty
    actual_results = constructNewSessionList([''],'movie2:link2:time2')
    assert 'movie2:link2:time2' == actual_results

def test_constructNewSessionListEmptyNewSession(): # empty new session
    actual_results = constructNewSessionList(['movie1:link1:time1'], '')
    assert actual_results == 'movie1:link1:time1'

def test_constructNewSessionListEmptyNewSessionAndInvalidList(): # empty new session and None current sessions
    actual_results = constructNewSessionList(None, '')
    assert actual_results == ''

#--------------------------------------------------------------------------

def test_constructUserListDifferentName(): #Different Username looks up Michael
    users = [('4y33757545', 'Michael Stone', 'Michael@email.com', 'pic'),('3273y2y8343', 'Person2', 'person2@email.com','pic')]
    user = 'Michael'
    actual_results = constructUserList(users, user, '3273y2y8343')
    assert actual_results == (['Michael Stone'], ['Michael@email.com'], ['pic'])

def test_constructUserListSameName(): #Different User same name
    users = [('4y33757545', 'Michael Stone', 'Michael@email.com', 'pic'),('3273y2y8343', 'Michael Stone', 'person2@email.com','pic')]
    user = 'Michael'
    actual_results = constructUserList(users, user, '3273y2y8343')
    assert actual_results == (['Michael Stone'], ['Michael@email.com'], ['pic'])

def test_constructUserListNoUsers(): #Empty user list
    users = []
    user = 'Michael'
    actual_results = constructUserList(users, user, '3273y2y8343')
    assert actual_results == ([], [], [])

def test_constructUserListNoneUser(): #User list is None
    users = None
    user = 'Michael'
    actual_results = constructUserList(users, user, '3273y2y8343')
    assert actual_results == ([], [], [])

def test_constructUserListNoUsersEmptySearch(): #Empty user list and empty search
    users = []
    user = ''
    actual_results = constructUserList(users, user, '3273y2y8343')
    assert actual_results == ([], [], [])

def test_constructUserListNoneUserEmptySearch(): #User list is None and search is Empty
    users = None
    user = 'Michael'
    actual_results = constructUserList(users, user, '3273y2y8343')
    assert actual_results == ([], [], [])

def test_constructUserListEmptySearch(): #empty search string
    users = [('4y33757545', 'Michael Stone', 'Michael@email.com', 'pic'),('3273y2y8343', 'Person2', 'person2@email.com','pic')]
    user = ''
    actual_results = constructUserList(users, user, '3273y2y8343')
    assert actual_results == ([], [], [])

#--------------------------------------------------------------------------

def test_constructNewFriendListFriendsExist(): #Add Friend to existing list
    current_friends = ['person1:email1,person2:email2']
    friend_info = 'person3'
    email_info = 'email3'
    actual_results = constructNewFriendList(current_friends,
                                            friend_info, email_info)
    assert actual_results == 'person1:email1,person2:email2,person3:email3'

def test_constructNewFriendListNoFriend(): #First friend
    current_friends = []
    friend_info = 'person1'
    email_info = 'email1'
    actual_results = constructNewFriendList(current_friends,friend_info, email_info)
    assert actual_results == 'person1:email1'

def test_constructNewFriendListNoFriends():
    current_friends = None
    friend_info = 'person1'
    email_info = 'email1'
    actual_results = constructNewFriendList(current_friends,
                                            friend_info, email_info)
    assert actual_results == 'person1:email1'

def test_constructNewFriendListEmptyNewName(): #New name is empty
    current_friends = ['person1:email1']
    friend_info = ''
    email_info = 'email1'
    actual_results = constructNewFriendList(current_friends,friend_info, email_info)
    assert actual_results == 'person1:email1'

def test_constructNewFriendListEmptyNewEmail(): #New email is empty
    current_friends = ['person1:email1']
    friend_info = 'person2'
    email_info = ''
    actual_results = constructNewFriendList(current_friends,friend_info, email_info)
    assert actual_results == 'person1:email1'

def test_constructNewFriendListEmptyNewEmailAndNewFriend(): #New email is empty
    current_friends = ['person1:email1']
    friend_info = ''
    email_info = ''
    actual_results = constructNewFriendList(current_friends,friend_info, email_info)
    assert actual_results == 'person1:email1'

#--------------------------------------------------------------------------

def test_getTopMovies(): # check if API returns top movies correctly
    movie_results_1 = getTopMovies()
    movie_results_2 = getTopMovies()
    assert len(movie_results_1[0]) == len(movie_results_2[0])
    assert len(movie_results_1[1]) == len(movie_results_2[1])

#--------------------------------------------------------------------------

def test_renderUserHomeWithUsers(): # render Home when some Users Exist
    sample_movies = ['movie1,movie2']
    sample_friends = ['friend1:email1,friend2:email2']
    actual_results = renderUserHome(sample_movies, sample_friends)
    assert len(actual_results[0]) == 9
    assert actual_results[1] == ['movie1', 'movie2']
    assert actual_results[2] == ['friend1', 'friend2']
    assert len(actual_results[3]) == 9

def test_renderUserHomeWithoutUsers(): #render Home when new users exist
    sample_movies = []
    sample_friends = []
    actual_results = renderUserHome(sample_movies, sample_friends)
    assert len(actual_results[0]) == 9
    assert actual_results[1] == ['']
    assert actual_results[2] == []
    assert len(actual_results[3]) == 9

#--------------------------------------------------------------------------

def test_findMoviesActualMovie(): # Check if a real movie name returns result
    actual_results = findMovies('Shrek')
    assert len(actual_results) > 0 

def test_findMoviesDoesntExist(): # Check if a fake movie name returns no results
    bad_search_results = findMovies('vjbefhbfbhabhawg')
    assert len(bad_search_results) == 0

def test_findMoviesEmptyRequest(): # Check if no results are returned for empty query
    bad_search_results = findMovies('')
    assert len(bad_search_results) == 0

#--------------------------------------------------------------------------

def test_renderMovie(): # Check if movies render correctly when given valid movie ID
    actual_results = renderMovie('0126029')
    assert actual_results[0] == 'Shrek' and len(actual_results[1]) > 0
    assert len(actual_results[1]) > 0 and len(actual_results[2]) > 0
    assert len(actual_results[2]) > 0 and actual_results[3] == 2001

#--------------------------------------------------------------------------

def test_sendEmailWithFriends(): # See if we can send an email with a friends list

    friend_list = ['chrisjkowalcz@gmail.com', 'cjk2159@columbia.edu']
    session_info = "Info:Citizen Kane,20201210-01:07,ZoomLink"

    validity = sendEmail(friend_list, session_info)
    assert(validity == "valid")

def test_sendEmailWithNoFriends(): # See if we can send an email with a friends list
    friend_list = []
    session_info = "Info:Citizen Kane,20201210-01:07,ZoomLink"
    validity = sendEmail(friend_list, session_info)
    assert validity == 'invalid'

