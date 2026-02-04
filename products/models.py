from django.db import models

# Create your models here.

class ProductSearch(models.Model):
    PRODUCT_TYPES = [
        ('cake', 'Cake'),
        ('dessert', 'Dessert'),
        ('pudding', 'Pudding'),
    ]

    product_id = models.PositiveIntegerField()
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES)

    name = models.CharField(max_length=200, db_index=True)

    category = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    flavor = models.CharField(
        max_length=100,
        blank=True,
        default=""
    )

    tags = models.CharField(max_length=250, blank=True)
    description = models.TextField(blank=True)

    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='search/', blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


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