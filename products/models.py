from django.db import models

# Create your models here.

class ProductSearch(models.Model):

    PRODUCT_TYPES = [
        ('cake', 'Cake'),
        ('dessert', 'Dessert'),
        ('pudding', 'Pudding'),
    ]

    name = models.CharField(max_length=150)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES)

    category = models.CharField(max_length=100, blank=True, null=True)
    flavor = models.CharField(max_length=100, blank=True, null=True)

    price = models.IntegerField()
    image = models.ImageField(upload_to='search/')
    product_id = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.product_type})"

class Cake(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='cakes/')
    price = models.IntegerField()

    category = models.CharField(
        max_length=50,
        choices=[
            ('wedding', 'Wedding'),
            ('birthday', 'Birthday'),
            ('bento', 'Bento'),
            ('vegan', 'Vegan'),
            ('kids', 'Kids'),
        ]
    )
    FLAVOR_CHOICES = [
    ('chocolate','Chocolate'),
    ('vanilla','Vanilla'),
    ('red-velvet','Red Velvet'),
    ('butterscotch','Butterscotch'),
    ('fruit-cakes','Fruit Cakes'),
    ('cheese_cakes','Cheese Cakes'),
]
    STRUCTURE_CHOICES = [
    ('single','Single Tier'),
    ('double','Double Tier'),
    ('trible','Trible Tier'),
    ('cupcakes','Cup Cakes'),
    ('sheetcakes','Sheet Cakes'),
    ('spongecakes','Sponge Cakes'),
    ('themecakes','Theme Cakes'),
    ]
    flavor = models.CharField(max_length=50, choices=FLAVOR_CHOICES)
    structure = models.CharField(max_length=50, choices=STRUCTURE_CHOICES)


    def __str__(self):
        return self.name

class Dessert(models.Model):
    CATEGORY_CHOICES = [
        ('pastries', 'Pastries'),
        ('cookies_biscuits', 'Cookies & Biscuits'),
        ('brownie', 'Brownie'),
        ('pistachio', 'Pistachio'),
    ]

    FLAVOR_CHOICES = [
        ('chocolate', 'Chocolate'),
        ('vanilla', 'Vanilla'),
        ('fruit', 'Fruit'),
        ('nutty_caramel','Nutty & Caramel')
    ]

    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='desserts/')
    price = models.IntegerField()

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    flavor = models.CharField(
        max_length=50,
        choices=FLAVOR_CHOICES
    )

    def __str__(self):
        return self.name
    
class Pudding(models.Model):

    STYLE_CHOICES = [
        ('warm', 'Warm'),
        ('chilled', 'Chilled'),
        ('vegan', 'Vegan'),
    ]

    TAG_COLOR_CHOICES = [
        ('default', 'Default'),
        ('green', 'Green'),
        ('vegan', 'Vegan'),
    ]

    FLAVOR_CHOICES = [
        ('chocolate', 'Chocolate'),
        ('vanilla', 'Vanilla'),
        ('fruit', 'Fruit'),
        ('pistachio', 'Pistachio'),
        ('strawberry', 'Strawberry'),
        ('mango', 'Mango'),
        ('butter','Butter')
    ]

    name = models.CharField(max_length=150)
    image = models.ImageField(upload_to='puddings/')
    price = models.IntegerField()

    flavor = models.CharField(
        max_length=50,
        choices=FLAVOR_CHOICES,
        blank=True,
        null=True
    )

    style = models.CharField(
        max_length=20,
        choices=STYLE_CHOICES,
        default='chilled'
    )

    tag_text = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    tag_color = models.CharField(
        max_length=20,
        choices=TAG_COLOR_CHOICES,
        default='default'
    )

    def __str__(self):
        return self.name