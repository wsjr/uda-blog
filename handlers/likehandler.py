from models import user
from models import blog
from models import like

from handlers import basehandler
from handlers import utils


class ViewLikeBlogHandler(basehandler.Handler):

    """
    Handler responsible for viewing likes in a blog.
    """

    def view_blog_likes(self, blog_id):
        u = utils.get_user_from_cookie(self)
        user_id = u.key().id()

        blog_id = int(blog_id)
        b = blog.Blogs.by_id(blog_id)
        blog_title = b.subject

        l = like.Likes.by_blog_id_likes(blog_id)
        users_map = user.Users.get_users_map()
        username = user.Users.get_username_by_id(int(user_id))

        self.render("likes.html",
                    likes=l,
                    user_id=user_id,
                    users_map=users_map,
                    username=username)

    def get(self, blog_id):
        # Valid user
        if utils.is_valid_user(self):
            self.view_blog_likes(blog_id)
        # Not a valid user, redirect to login
        else:
            self.render("login.html",
                        loginfirsterror=utils.LOGIN_REQ_ERROR)


class LikeBlogHandler(basehandler.Handler):

    """
    Handler responsible for liking a blog.
    """

    def handle_like_blog(self):
        u = utils.get_user_from_cookie(self)
        user_id = int(u.key().id())
        blog_id = int(self.request.get("blog_id"))

        like.Likes.like_by_id(blog_id, user_id)

    def post(self):
        # Valid user
        if utils.is_valid_user(self):
            self.handle_like_blog()
        # Not a valid user, redirect to login
        else:
            self.render("login.html",
                        loginfirsterror=utils.LOGIN_REQ_ERROR)


class UnLikeBlogHandler(basehandler.Handler):

    """
    Handler responsible for unliking a blog.
    """

    def handle_unlike_blog(self):
        u = utils.get_user_from_cookie(self)
        user_id = int(u.key().id())
        blog_id = int(self.request.get("blog_id"))

        like.Likes.unlike_by_id(blog_id, user_id)

    def post(self):
        # Valid user
        if utils.is_valid_user(self):
            self.handle_unlike_blog()
        # Not a valid user, redirect to login
        else:
            self.render("login.html",
                        loginfirsterror=utils.LOGIN_REQ_ERROR)
