from models import user
from models import blog
from models import comment

from handlers import basehandler
from handlers import utils


class ViewBlogCommentsHandler(basehandler.Handler):

    """
    Handler responsible for viewing comments in a blog.
    """

    def view_blog_comments(self, blog_id):
        u = utils.get_user_from_cookie(self)

        # Valid user
        if u:
            user_id = u.key().id()
            username = user.Users.get_username_by_id(int(user_id))

            blog_id = int(blog_id)
            b = blog.Blogs.by_id(blog_id)
            blog_title = b.subject

            c = comment.Comments.by_blog_id(blog_id)
            users_map = user.Users.get_users_map()

            self.render("comments.html",
                        blog_title=blog_title,
                        comments=c,
                        user_id=user_id,
                        users_map=users_map,
                        username=username)

        # Not a valid user, redirect to login
        else:
            self.render("login.html",
                        loginfirsterror=utils.LOGIN_REQ_ERROR)

    def handle_view_blog_comments(self, blog_id):
        content = self.request.get("content")

        if content:
            u = utils.get_user_from_cookie(self)
            user_id = int(u.key().id())

            blog_id = int(blog_id)

            c = comment.Comments.register(user_id=user_id,
                                          blog_id=blog_id,
                                          content=content)
            c.put()

            self.redirect("/viewblogcomments/%s" % blog_id)
        else:
            error = "content, please!"
            self.render("comments.html",
                        content=content,
                        error=error)

    def get(self, blog_id):
        # Valid user
        if utils.is_valid_user(self):
            self.view_blog_comments(blog_id)
        # Not a valid user, redirect to login
        else:
            self.render("login.html",
                        loginfirsterror=utils.LOGIN_REQ_ERROR)

    def post(self, blog_id):
        # Valid user
        if utils.is_valid_user(self):
            self.handle_view_blog_comments(blog_id)
        # Not a valid user, redirect to login
        else:
            self.render("login.html",
                        loginfirsterror=utils.LOGIN_REQ_ERROR)


class EditBlogCommentHandler(basehandler.Handler):

    """
    Handler responsible for editing a blog comment.
    """

    def edit_blog_comment(self, comment_id):
        u = utils.get_user_from_cookie(self)
        user_id = u.key().id()
        username = user.Users.get_username_by_id(int(user_id))

        c = comment.Comments.by_id(int(comment_id))

        self.render("comment.html",
                    comment=c,
                    username=username)

    def handle_blog_comment(self, comment_id):
        content = self.request.get("content")

        # Update blog comments
        c = comment.Comments.by_id(int(comment_id))
        c.content = content

        # Flush
        c.put()

        # Redirect
        self.redirect("/viewblogcomments/%s" % c.blog_id)

    def get(self, comment_id):
        # Valid user
        if utils.is_valid_user(self):
            self.edit_blog_comment(comment_id)
        # Not a valid user, redirect to login
        else:
            self.render("login.html",
                        loginfirsterror=utils.LOGIN_REQ_ERROR)

    def post(self, comment_id):
        # Valid user and its the blog owner.
        if (utils.is_valid_user(self) and
                utils.is_comment_owner(self, comment_id)):
            self.handle_blog_comment(comment_id)
        # Not a valid user, redirect to login
        else:
            self.render("login.html",
                        loginfirsterror=utils.LOGIN_REQ_ERROR)


class DeleteBlogCommentHandler(basehandler.Handler):

    """
    Handler responsible for deleting a blog comment.
    """

    def delete_blog_comment(self, comment_id):
        comment_id = int(comment_id)
        c = comment.Comments.by_id(comment_id)

        # Delete comment
        comment.Comments.delete_by_id(comment_id)

        self.redirect("/viewblogcomments/%s" % c.blog_id)

    def get(self, comment_id):
        # Valid user and its the blog owner.
        if (utils.is_valid_user(self) and
                utils.is_comment_owner(self, comment_id)):
            self.delete_blog_comment(comment_id)
        # Not a valid user, redirect to login
        else:
            self.render("login.html",
                        loginfirsterror=utils.LOGIN_REQ_ERROR)
