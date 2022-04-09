from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, *args, **kwargs):
        user = self.model(
            **kwargs
        )
        user.is_superuser = False
        password = kwargs.get('password')
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, *args, **kwargs):
        user = self.model(
            **kwargs
        )
        user.is_superuser = True
        password = kwargs.get('password')
        user.set_password(password)
        user.save(using=self._db)
        return user
