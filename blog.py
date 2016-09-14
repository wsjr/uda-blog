#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2

from models import blog
from models import comment
from models import like
from models import user

from handlers import userhandler
from handlers import bloghandler
from handlers import commenthandler
from handlers import likehandler


app = webapp2.WSGIApplication([
    ('/signup', userhandler.SignUpHandler),
    ('/welcome', userhandler.WelcomeHandler),
    ('/login', userhandler.LoginHandler),
    ('/logout', userhandler.LogoutHandler),
    ('/', bloghandler.DisplayBlogsHandler),
    ('/blog', bloghandler.DisplayBlogsHandler),
    ('/blog/(\d+)', bloghandler.DisplayBlogHandler),
    ('/editblog/(\d+)', bloghandler.EditBlogHandler),
    ('/deleteblog/(\d+)', bloghandler.DeleteBlogHandler),
    ('/blog/newpost', bloghandler.NewBlogHandler),
    ('/viewblogcomments/(\d+)', commenthandler.ViewBlogCommentsHandler),
    ('/editblogcomment/(\d+)', commenthandler.EditBlogCommentHandler),
    ('/deleteblogcomment/(\d+)', commenthandler.DeleteBlogCommentHandler),
    ('/viewlikeblog/(\d+)', likehandler.ViewLikeBlogHandler),
    ('/likeblog', likehandler.LikeBlogHandler),
    ('/unlikeblog', likehandler.UnLikeBlogHandler)
], debug=True)
