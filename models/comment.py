
from google.appengine.ext import db


def comments_key(name='default'):
    return db.Key.from_path('comments', name)


class Comments(db.Model):

    """
    Users db model
    """
    user_id = db.IntegerProperty(required=True)
    blog_id = db.IntegerProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid, parent=comments_key())

    @classmethod
    def delete_by_id(cls, id):
        c = cls.by_id(id)
        c.delete()

    @classmethod
    def by_blog_id(cls, blog_id):
        return cls.all()\
                  .ancestor(comments_key())\
                  .filter('blog_id =', blog_id)\
                  .order('created')

    @classmethod
    def register(cls, user_id, blog_id, content):
        return Comments(user_id=user_id,
                        blog_id=blog_id,
                        content=content,
                        parent=comments_key())

    @classmethod
    def add(cls, user_id, blog_id, content):
        r = cls.register(user_id, blog_id, content)
        r.put()

    @classmethod
    def delete_by_blog_id(cls, blog_id):
        rs = cls.by_blog_id(blog_id)
        for r in rs:
            r.delete()
