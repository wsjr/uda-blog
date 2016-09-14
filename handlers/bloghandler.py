from models import user
from models import blog
from models import comment
from models import like

from handlers import basehandler
from handlers import utils


class NewBlogHandler(basehandler.Handler):

    """
    Handler responsible used for new posts.
    """

    def render_post(self):
        u = utils.get_user_from_cookie(self)
        user_id = u.key().id()
        username = user.Users.get_username_by_id(int(user_id))

        self.render("post.html",
                    title="New Blog",
                    user_id=user_id,
                    username=username)

    def handle_post(self):
        u = utils.get_user_from_cookie(self)
        user_id = u.key().id()
        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:
            b = blog.Blogs.create(subject=subject,
                                  content=content,
                                  user_id=user_id)
            b.put()

            blog_id = b.key().id()

            self.redirect("/blog/%s" % blog_id)

        else:
            error = "subject and content, please!"
            username = user.Users.get_username_by_id(int(user_id))

            self.render("post.html",
                        title="New Blog",
                        subject=subject,
                        content=content,
                        error=error,
                        user_id=user_id,
                        username=username)

    def get(self):
        # Valid user
        if utils.is_valid_user(self):
            self.render_post()

        # Not a valid user, redirect to login
        else:
            self.render("login.html",
                        loginfirsterror=utils.LOGIN_REQ_ERROR)

    def post(self):
        # Valid user
        if utils.is_valid_user(self):
            self.handle_post()

        # Not a valid user, redirect to login
        else:
            self.render("login.html",
                        loginfirsterror=utils.LOGIN_REQ_ERROR)


class DisplayBlogsHandler(basehandler.Handler):

    """
    Handler used for display blogs for logged and logged out users.
    """

    def render_blogs(self):
        u = utils.get_user_from_cookie(self)
        user_id = None
        username = None
        blogs = blog.Blogs.by_user_id()
        users_map = user.Users.get_users_map()
        likes_map = {}

        # Valid user
        if utils.is_valid_user(self):
            user_id = u.key().id()
            username = user.Users.get_username_by_id(int(user_id))
            likes_map = like.Likes.get_likes_map()

        self.render("blogs.html",
                    user_id=user_id,
                    blogs=blogs,
                    users_map=users_map,
                    likes_map=likes_map,
                    username=username)

    def get(self):
        self.render_blogs()


class DisplayBlogHandler(basehandler.Handler):

    """
    Handler responsible for displaying a blog after the user posted it.
    """

    def render_blog(self, blog_id):
        u = utils.get_user_from_cookie(self)
        user_id = u.key().id()
        users_map = user.Users.get_users_map()
        username = user.Users.get_username_by_id(int(user_id))
        b = blog.Blogs.by_id(int(blog_id))

        self.render("blog.html",
                    user_id=user_id,
                    blog=b,
                    username=username)

    def get(self, blog_id):
        # Valid user
        if utils.is_valid_user(self):
            self.render_blog(blog_id)
        # Not a valid user, redirect to login
        else:
            self.render("login.html",
                        loginfirsterror=utils.LOGIN_REQ_ERROR)


class EditBlogHandler(basehandler.Handler):

    """
    Handler responsible for editing a blog.
    """

    def edit_blog(self, blog_id):
        u = utils.get_user_from_cookie(self)
        user_id = u.key().id()
        username = user.Users.get_username_by_id(int(user_id))

        b = blog.Blogs.by_id(int(blog_id))
        subject = b.subject
        content = b.content

        self.render("post.html",
                    title="Edit Post",
                    subject=subject,
                    content=content,
                    blog_id=blog_id,
                    user_id=user_id,
                    username=username)

    def handle_blog(self, blog_id):
        subject = self.request.get("subject")
        content = self.request.get("content")

        # Update blog subject and content
        b = blog.Blogs.by_id(int(blog_id))
        b.subject = subject
        b.content = content

        # Flush
        b.put()

        # Redirect
        self.redirect("/blog")

    def get(self, blog_id):
        # Valid user
        if utils.is_valid_user(self):
            self.edit_blog(blog_id)
        # Not a valid user, redirect to login
        else:
            self.render("login.html",
                        loginfirsterror=utils.LOGIN_REQ_ERROR)

    def post(self, blog_id):
        # Valid user and its the blog owner.
        if utils.is_valid_user(self) and utils.is_blog_owner(self, blog_id):
            self.handle_blog(blog_id)
        # Not a valid user, redirect to login
        else:
            self.render("login.html",
                        loginfirsterror=utils.LOGIN_REQ_ERROR)


class DeleteBlogHandler(basehandler.Handler):

    """
    Handler responsible for deleting a blog.
    """

    def delete_blog(self, blog_id):
        blog_id = int(blog_id)

        # Delete the blog
        blog.Blogs.delete_by_id(blog_id)

        # Delete comments associated with the blog
        comment.Comments.delete_by_blog_id(blog_id)

        # Delete likes associated with the blog
        like.Likes.delete_by_blog_id(blog_id)

        self.redirect("/blog")

    def get(self, blog_id):
        # Valid user and its the blog owner.
        if utils.is_valid_user(self) and utils.is_blog_owner(self, blog_id):
            self.delete_blog(blog_id)
        # Not a valid user, redirect to login
        else:
            self.render("login.html",
                        loginfirsterror=utils.LOGIN_REQ_ERROR)
