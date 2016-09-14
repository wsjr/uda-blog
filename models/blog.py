from google.appengine.ext import db


def blogs_key(name='default'):
    return db.Key.from_path('blogs', name)


class Blogs(db.Model):

    """
    Blogs db model
    """
    user_id = db.IntegerProperty(required=True)
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid, parent=blogs_key())

    @classmethod
    def by_user_id(cls, user_id=None):
        if user_id is not None:
            u = cls.all()\
                   .ancestor(blogs_key())\
                   .filter('user_id =', user_id)\
                   .order('-last_modified')
        else:
            u = cls.all().ancestor(blogs_key()).order('-last_modified')
        return u

    @classmethod
    def delete_by_id(cls, blog_id):
        b = cls.by_id(blog_id)
        b.delete()

    @classmethod
    def create(cls, subject, content, user_id):
        return Blogs(subject=subject,
                     content=content,
                     user_id=user_id,
                     parent=blogs_key())
