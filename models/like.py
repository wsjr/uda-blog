
from google.appengine.ext import db


def likes_key(name='default'):
    return db.Key.from_path('likes', name)


class Likes(db.Model):

    """
    Likes db model
    """
    user_id = db.IntegerProperty(required=True)
    blog_id = db.IntegerProperty(required=True)
    like = db.BooleanProperty()

    @classmethod
    def toggle_by_id(cls, blog_id, user_id):
        r = cls.all()\
               .ancestor(likes_key())\
               .filter('blog_id =', blog_id)\
               .filter('user_id =', user_id)

        # Just update the entry
        if r.count() > 0:
            r = r.get()
            # Toggle the value
            r.like = not r.like
            r.put()
        # Create entry
        else:
            r = Likes(user_id=user_id,
                      blog_id=blog_id,
                      like=True,
                      parent=likes_key())
            r.put()

    @classmethod
    def like_by_id(cls, blog_id, user_id):
        cls.toggle_by_id(blog_id, user_id)

    @classmethod
    def unlike_by_id(cls, blog_id, user_id):
        cls.toggle_by_id(blog_id, user_id)

    @classmethod
    def by_blog_id(cls, blog_id):
        return cls.all().ancestor(likes_key()).filter('blog_id =', blog_id)

    @classmethod
    def by_blog_id_likes(cls, blog_id):
        return cls.by_blog_id(blog_id).filter('like =', True)

    @classmethod
    def delete_by_blog_id(cls, blog_id):
        rs = cls.by_blog_id(blog_id)
        for r in rs:
            r.delete()

    # Note: INNER JOIN is not possible in GQL so needed to use
    #       maps/dictionary to get what I need to do.
    @classmethod
    def get_likes_map(cls):
        likes_map = {}
        likes = cls.all().ancestor(likes_key()).filter('like =', True)
        for like in likes:
            # Add entry to map blog's total "like" count
            if likes_map.get(like.blog_id) is None:
                likes_map[like.blog_id] = 1
            else:
                likes_map[like.blog_id] = likes_map[like.blog_id] + 1

            # Add entry to map of blog's like status per user id
            key = "%s-%s" % (like.user_id, like.blog_id)
            likes_map[key] = like.like

        return likes_map
