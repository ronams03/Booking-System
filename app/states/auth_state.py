import reflex as rx
from typing import Optional
import hashlib


class AuthState(rx.State):
    """The authentication state for the app."""

    authenticated_user_email: Optional[str] = rx.LocalStorage(
        None, name="authenticated_user"
    )
    ADMIN_USER_EMAIL = "admin@bookify.com"
    ADMIN_USER_PASSWORD_HASH = (
        "$2b$12$QQqiAe4XwyUv8yG5F5Rvnu1TJ6Gpw/WrpmQj3s0RYHxcNd3ukp4BW"
    )
    login_error: Optional[str] = None
    is_loading: bool = False

    @rx.var
    def is_authenticated(self) -> bool:
        """Check if a user is authenticated."""
        return (
            self.authenticated_user_email is not None
            and self.authenticated_user_email != ""
        )

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a hashed one."""
        import bcrypt

        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )

    @rx.event
    def login(self, form_data: dict):
        """Handle the login form submission."""
        self.is_loading = True
        self.login_error = None
        yield
        email = form_data.get("email")
        password = form_data.get("password")
        if not email or not password:
            self.login_error = "Email and password are required."
            self.is_loading = False
            return
        if email == self.ADMIN_USER_EMAIL and self._verify_password(
            password, self.ADMIN_USER_PASSWORD_HASH
        ):
            self.authenticated_user_email = email
            self.is_loading = False
            yield rx.redirect("/admin")
        else:
            self.login_error = "Invalid credentials. Please try again."
            self.is_loading = False

    @rx.event
    def logout(self):
        """Log the user out."""
        self.authenticated_user_email = None
        return rx.redirect("/")

    @rx.event
    def check_auth(self):
        """Check if the user is authenticated and redirect if not."""
        if not self.is_authenticated:
            return rx.redirect("/login")