import re

import hashlib

from models import user
from models import blog
from models import comment


# Validation-related utility functions


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
LOGIN_REQ_ERROR = "Please login first before trying to do any actions!"


def valid_username(username):
    return USER_RE.match(username)


def valid_password(password):
    return PASSWORD_RE.match(password)


def valid_email(email):
    return EMAIL_RE.match(email)


# Hash-related utility functions

def hash_str(s):
    return hashlib.md5(s).hexdigest()


def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))


def check_secure_val(h):
    val = h.split("|")[0]
    if h == make_secure_val(val):
        return val


def set_cookie(self, s):
    hash_string = hash_str(str(s))
    user_id_val = "%s|%s" % (s, hash_string)

    self.response.headers.add_header(
        'Set-Cookie', 'user_id=%s; Path=/' % user_id_val)


def get_user_from_cookie(self):
    user_id_val = self.request.cookies.get('user_id')

    # Valid user
    if user_id_val is not None and check_secure_val(user_id_val):
        user_id = user_id_val.split("|")[0]

        u = user.Users.by_id(int(user_id))
        return u


def is_valid_user(self):
    u = get_user_from_cookie(self)
    return u is not None


def is_blog_owner(self, blog_id):
    b = blog.Blogs.by_id(int(blog_id))
    u = get_user_from_cookie(self)

    return int(b.user_id) == int(u.key().id())


def is_comment_owner(self, comment_id):
    c = comment.Comments.by_id(int(comment_id))
    u = get_user_from_cookie(self)

    return int(c.user_id) == int(u.key().id())
