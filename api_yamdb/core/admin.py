from django.contrib import admin

from users.models import User
from reviews.models import Review, Title, Category, Comment


admin.site.register(Review)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(User)
