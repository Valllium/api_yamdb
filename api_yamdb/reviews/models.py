from django.db import models

from users.models import User

CHOICES = [(i, i) for i in range(1, 11)]

# Ниже в коде использовала Ирину модель Title, чтобы получилось сделать миграции
class Title(models.Model):
    pass

class Review(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    score = models.IntegerField(default=0, choices=CHOICES)

    class Meta:
        verbose_name = 'review'
        verbose_name_plural = 'reviews'
        unique_together = ('user', 'title',)


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'
