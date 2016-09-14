import hashlib
import random
import string


from google.appengine.ext import db


def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))


def make_pw_hash(name, pw, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (h, salt)


def valid_pw(name, pw, h):
    salt = h.split(",")[1]
    return h == make_pw_hash(name, pw, salt)


def users_key(group='default'):
    return db.Key.from_path('users', group)


class Users(db.Model):

    """
    Users db model
    """
    username = db.StringProperty(required=True)
    hash_salt = db.StringProperty(required=True)
    email = db.StringProperty(required=False)
    created = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid, parent=users_key())

    @classmethod
    def by_name(cls, name):
        return cls.all().ancestor(users_key()).filter('username =', name).get()

    @classmethod
    def get_username_by_id(cls, uid):
        return cls.by_id(uid).username

    @classmethod
    def register(cls, name, pw, email=None):
        pw_hash = make_pw_hash(name, pw)
        return Users(username=name,
                     hash_salt=pw_hash,
                     email=email,
                     parent=users_key())

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.hash_salt):
            return u

    # Note: INNER JOIN is not possible in GQL so needed to use
    #       maps/dictionary to get what I need to do.
    @classmethod
    def get_users_map(cls):
        users_map = {}
        users = cls.all().ancestor(users_key())
        for user in users:
            users_map[user.key().id()] = user.username

        return users_map
