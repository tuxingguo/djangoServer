from django.db import models

# Create your models here.
from django.db import models

class User(models.Model):
    class Meta:
        db_table = 'user'

    userId = models.IntegerField(primary_key=True, db_column='userId')
    userName = models.CharField(max_length = 20)
    phone = models.CharField(max_length = 20, null = True)
    password = models.CharField(max_length = 64)
    email = models.CharField(max_length = 20, null = True)
    avatar = models.CharField(max_length = 100, null=True)
    signature = models.CharField(max_length = 100, null=True)
    title = models.CharField(max_length = 20, null=True)
    group = models.CharField(max_length = 50, null=True)
    notifyCount = models.IntegerField(null=True)
    unreadCount = models.IntegerField(null=True)
    country = models.CharField(max_length = 120, null=True)
    address = models.CharField(max_length = 100, null=True)

    def __repr__(self):
        return "".format(self.userId, self.phone)

    __str__ = __repr__


class Book(models.Model):
    class Meta:
        db_table = 'book'
    id = models.IntegerField(primary_key=True, db_column='id')
    bookName = models.CharField(max_length = 20)
    author = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    publish = models.CharField(max_length = 20, null=True)

    def __repr__(self):
        return "".format(self.bookName, self.author)

    __str__ = __repr__


# class tick(models.Model):
#     class Meta:
#         db_table = 'tick'
#
#
#
#     def __repr__(self):
#         return "".format(self.bookName, self.author)
#
#     __str__ = __repr__