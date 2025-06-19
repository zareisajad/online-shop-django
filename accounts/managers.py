from django.contrib.auth.models import BaseUserManager
import re

class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password, confirm_password=None):
        if not first_name and not last_name:
            raise ValueError('First name and last name are required!')
        if not email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError('Valid email is required!')
        if not username and len(username) < 30:
            raise ValueError('Username is required!')
        if password != confirm_password and len(password) >= 8:
            raise ValueError('Passwords do not match!')

        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password, confirm_password=None):
        user = self.create_user(first_name, last_name, email, username, password, confirm_password)
        user.is_admin = True
        user.save(using=self.db)
        return user

class profileManager(BaseUserManager):
    def create_profile(self, user, profile_picture=None, birth_date=None, address=None, bio=None, location=None, website=None):
        if not user:
            raise ValueError('User is required to create a profile!')

        profile = self.model(
            user=user,
            profile_picture=profile_picture,
            birth_date=birth_date,
            address=address,
            bio=bio,
            location=location,
            website=website
        )
        profile.save(using=self.db)
        return profile
