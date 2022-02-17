from flask_login import UserMixin
try:
    from Flask_Project.db import get_db
except Exception:
    from db import get_db

class User(UserMixin):
    def __init__(
            self,
            id_,
            name,
            email,
            profile_pic,
            movieList,
            wishList,
            friendList,
            sessionList):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic
        self.movieList = movieList
        self.wishList = wishList
        self.friendList = friendList
        self.sessionList = sessionList

    @staticmethod
    def get(user_id):
        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            return None

        user = User(
            id_=user[0],
            name=user[1],
            email=user[2],
            profile_pic=user[3],
            movieList=user[4],
            wishList=user[5],
            friendList=user[6],
            sessionList=user[7])
        return user

    @staticmethod
    def getAll():
        db = get_db()
        user = db.execute(
            "SELECT * FROM user"
        ).fetchall()

        return user

    @staticmethod
    def reset():
        db = get_db()
        db.execute(
            "DELETE FROM user"
        )
        db.commit()

    @staticmethod
    def create(
            id_,
            name,
            email,
            profile_pic,
            movieList,
            wishList,
            friendList,
            sessionList):
        db = get_db()
        temp = "INSERT INTO user (id, name, email, profile_pic, movieList, "
        temp += "wishList, friendList, sessionList)"
        temp += " VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        db.execute(
            temp,
            (id_,
             name,
             email,
             profile_pic,
             movieList,
             wishList,
             friendList,
             sessionList),
        )
        db.commit()

    @staticmethod
    def getFriends(user_id):
        db = get_db()
        user = db.execute(
            "SELECT friendList from user WHERE id = \'" + user_id + "\'"
        ).fetchone()

        return user

    @staticmethod
    def getMovieWishlist(user_id):
        db = get_db()
        user = db.execute(
            "SELECT wishlist from user WHERE id = \'" + user_id + "\'"
        ).fetchone()

        return user

    @staticmethod
    def getSessions(user_id):
        db = get_db()
        user = db.execute(
            "SELECT sessionList from user WHERE id = \'" + user_id + "\'"
        ).fetchone()

        return user

    @staticmethod
    def addToWishlist(user_id, movie_list):
        db = get_db()

        user = db.execute(
            "UPDATE user SET wishlist = \'{0}\' WHERE id = \'{1}\'"
            .format(movie_list, user_id))

        db.commit()
        if not user:
            return False
        return True

    @staticmethod
    def addSessionToWishlist(user_id, session_list):
        db = get_db()

        user = db.execute(
            "UPDATE user SET sessionList = \'{0}\' WHERE id = \'{1}\'"
            .format(session_list, user_id))

        db.commit()
        if not user:
            return False
        return True

    @staticmethod
    def addFriend(user_id, friend_list):
        db = get_db()

        user = db.execute(
            "UPDATE user SET friendList = \'{0}\' WHERE id = \'{1}\'"
            .format(friend_list, user_id))

        db.commit()
        if not user:
            return False
        return True
