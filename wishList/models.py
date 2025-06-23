from django.db import models

# Create your models here.
class WishList(models.Model):
    """
    Model representing a user's wish list.
    """
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='wish_list')
    product = models.ForeignKey('shop.Product', on_delete=models.CASCADE, related_name='wish_list_items')
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username}'s wish list item: {self.product.name}"
