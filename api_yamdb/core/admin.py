from django.contrib import admin
<<<<<<< HEAD
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    list_filter = ("slug",)


class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("slug",)


class TitleAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "name", "year", "description")
    search_fields = ("name",)
    list_filter = ("category", "year")
    empty_value_display = "-пусто-"


class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ("genre", "title")


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "pub_date", "score", "text")
    search_fields = ("text", "author", "title")
    list_filter = (
        "pub_date",
        "score",
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "review", "author", "pub_date", "text")
    search_fields = ("text", "author", "review")
    list_filter = ("pub_date",)
=======
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_filter = ('slug',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('slug',)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'name', 'year', 'description')
    search_fields = ('name', )
    list_filter = ('category', 'year')
    empty_value_display = '-пусто-'


class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('genre', 'title')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'pub_date', 'score', 'text')
    search_fields = ('text', 'author', 'title')
    list_filter = ('pub_date', 'score',)



class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'author', 'pub_date', 'text')
    search_fields = ('text', 'author', 'review')
    list_filter = ('pub_date',)
>>>>>>> 242e640 (Админ панель)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
<<<<<<< HEAD
admin.site.register(User)
=======

>>>>>>> 242e640 (Админ панель)
