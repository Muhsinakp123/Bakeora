from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import Cake, Dessert, Pudding, ProductSearch


def update_index(instance, ptype, tags=""):
    ProductSearch.objects.update_or_create(
        product_id=instance.id,
        product_type=ptype,
        defaults={
            "name": instance.name,
            "category": getattr(instance, "category", ""),
            "flavor": getattr(instance, "flavor", ""),
            "price": instance.price,
            "image": instance.image,
            "tags": tags,
        }
    )


@receiver(post_save, sender=Cake)
def index_cake(sender, instance, **kwargs):
    update_index(instance, "cake", "cake,birthday,wedding,sweet")


@receiver(post_save, sender=Dessert)
def index_dessert(sender, instance, **kwargs):
    update_index(instance, "dessert", "dessert,party,sweet")


@receiver(post_save, sender=Pudding)
def index_pudding(sender, instance, **kwargs):
    update_index(instance, "pudding", "pudding,cream,sweet")
