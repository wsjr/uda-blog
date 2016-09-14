from models import user

from handlers import basehandler
from handlers import utils


class LoginHandler(basehandler.Handler):

    """
    Handler responsible for logging in  users.
    """

    def display_login_error(self, username):
        loginerror = "Invalid login"
        self.render("login.html", username=username, loginerror=loginerror)

    def validate_user(self, username, password):
        u = user.Users.by_name(username)

        if (u is not None and
                user.valid_pw(username, password, u.hash_salt)):
            utils.set_cookie(self, u.key().id())
            self.redirect("/welcome")
        else:
            self.display_login_error(username)

    def get(self):
        if utils.is_valid_user(self):
            self.redirect("/welcome")
        else:
            self.render("login.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")

        # Check if username and password are valid
        if (utils.valid_username(username) is None or
                utils.valid_password(password) is None):
            self.display_login_error(username)
        # Check if the username exists.
        else:
            self.validate_user(username, password)


class LogoutHandler(basehandler.Handler):

    """
    Handler responsible for logging out users.
    """

    def clear_cookie(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def get(self):
        # Clear cookie
        self.clear_cookie()

        # Redirect to sign up page.
        self.redirect("/login")


class SignUpHandler(basehandler.Handler):

    """
    Handler responsible for signing up new users
    """

    def get(self):
        if utils.is_valid_user(self):
            self.redirect("/welcome")
        else:
            self.render("signup.html")

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        usernameerror = ""
        passworderror = ""
        verifyerror = ""
        emailerror = ""

        # Check username
        if utils.valid_username(username) is None:
            usernameerror = "That's not a valid username."

        # Check password
        if utils.valid_password(password) is None:
            passworderror = "That wasn't a valid password."

        # Check password2
        else:
            if utils.valid_password(verify) is None or password != verify:
                verifyerror = "Your passwords didn't match."

        # Verify email (optional)
        if len(email) and valid_email(email) is None:
            emailerror = "That's not a valid email."

        if (len(usernameerror) or len(passworderror) or
                len(verifyerror) or len(emailerror)):
            self.render("signup.html",
                        username=username,
                        usernameerror=usernameerror,
                        passworderror=passworderror,
                        verifyerror=verifyerror,
                        email=email,
                        emailerror=emailerror)
        else:
            u = user.Users.by_name(username)

            # If it exists, error out
            if u:
                usernameerror = "User already exists."
                self.render("signup.html",
                            username=username,
                            usernameerror=usernameerror,
                            passworderror=passworderror,
                            verifyerror=verifyerror,
                            email=email,
                            emailerror=emailerror)
            else:
                b = user.Users.register(username, password, email)
                b.put()

                # Set cookie
                utils.set_cookie(self, b.key().id())

                # Redirect to welcome page
                self.redirect("/welcome")


class WelcomeHandler(basehandler.Handler):

    """
    Handler responsible for welcoming logged users.
    """

    def render_welcome(self):
        u = utils.get_user_from_cookie(self)
        user_id = u.key().id()
        username = user.Users.get_username_by_id(int(user_id))

        self.render("welcome.html",
                    username=username)

    def get(self):
        # Valid user
        if utils.is_valid_user(self):
            self.render_welcome()

        # Not a valid user, redirect to login.
        else:
            self.render("login.html",
                        loginfirsterror=utils.LOGIN_REQ_ERROR)
