from django.db import models
from django.contrib.auth.models import User
from shortuuid.django_fields import ShortUUIDField
# Create your models here.

CATEGORIES = (
    ('blush', 'Blush'),
    ('bronzer', 'Bronzer'),
    ('eyebrow', 'Eyebrow'),
    ('eyeliner', 'Eyeliner'),
    ('eyeshadow', 'Eyeshadow'),
    ('foundation', 'Foundation'),
    ('lip liner', 'Lip Liner'),
    ('lipstick', 'Lipstick'),
    ('mascara', 'Mascara'),
    ('nail polish', 'Nail Polish'),
)


class Category(models.Model):
    categoryId = ShortUUIDField(unique = True, length=10, max_length=20, prefix="cat", alphabet="abcdefghijk123456789")
    title = models.CharField(choices=CATEGORIES)
    image = models.CharField()

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title

class Product(models.Model):

    BRANDS = (
    ('almay', 'Almay'),
    ('alva', 'Alva'),
    ('anna sui', 'Anna Sui'),
    ('annabelle', 'Annabelle'),
    ('benefit', 'Benefit'),
    ('boosh', 'Boosh'),
    ('burt\'s bees', 'Burt\'s Bees'),
    ('butter london', 'Butter London'),
    ('c\'est moi', 'C\'est Moi'),
    ('cargo cosmetics', 'Cargo Cosmetics'),
    ('china glaze', 'China Glaze'),
    ('clinique', 'Clinique'),
    ('coastal classic creation', 'Coastal Classic Creation'),
    ('colourpop', 'Colourpop'),
    ('covergirl', 'Covergirl'),
    ('dalish', 'Dalish'),
    ('deciem', 'Deciem'),
    ('dior', 'Dior'),
    ('dr. hauschka', 'Dr. Hauschka'),
    ('e.l.f.', 'E.L.F.'),
    ('essie', 'Essie'),
    ('fenty', 'Fenty'),
    ('glossier', 'Glossier'),
    ('green people', 'Green People'),
    ('iman', 'Iman'),
    ('l\'oreal', 'L\'Oreal'),
    ('lotus cosmetics usa', 'Lotus Cosmetics USA'),
    ('maia\'s mineral galaxy', 'Maia\'s Mineral Galaxy'),
    ('marcelle', 'Marcelle'),
    ('marienatie', 'Marienatie'),
    ('maybelline', 'Maybelline'),
    ('milani', 'Milani'),
    ('mineral fusion', 'Mineral Fusion'),
    ('misa', 'Misa'),
    ('mistura', 'Mistura'),
    ('moov', 'Moov'),
    ('nudus', 'Nudus'),
    ('nyx', 'NYX'),
    ('orly', 'Orly'),
    ('pacifica', 'Pacifica'),
    ('penny lane organics', 'Penny Lane Organics'),
    ('physicians formula', 'Physicians Formula'),
    ('piggy paint', 'Piggy Paint'),
    ('pure anada', 'Pure Anada'),
    ('rejuva minerals', 'Rejuva Minerals'),
    ('revlon', 'Revlon'),
    ('sally b\'s skin yummies', 'Sally B\'s Skin Yummies'),
    ('salon perfect', 'Salon Perfect'),
    ('sante', 'Sante'),
    ('sinful colours', 'Sinful Colours'),
    ('smashbox', 'Smashbox'),
    ('stila', 'Stila'),
    ('suncoat', 'Suncoat'),
    ('w3llpeople', 'W3LLPeople'),
    ('wet n wild', 'Wet n Wild'),
    ('zorah', 'Zorah'),
    ('zorah biocosmetiques', 'Zorah Biocosmetiques'),
)

    productId = ShortUUIDField(unique = True, length=10, max_length=20, prefix="pro", alphabet="abcdefghijk123456789")
    title = models.CharField(max_length=150)
    product_type = models.CharField(max_length=150)
    image = models.CharField()
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    brand = models.CharField(choices=BRANDS)
    featured = models.BooleanField(default=True)
    on_sale = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class ProductColors(models.Model):
    colorId =ShortUUIDField(unique = True, length=10, max_length=20, prefix="col", alphabet="abcdefghijk123456789")
    hex_value = models.CharField(max_length=50)
    color_name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Product Colors"

    def __str__(self):
        return self.color_name

class ProductEntry(models.Model):
    productId = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    colorId = models.ForeignKey(ProductColors, on_delete=models.SET_NULL, null=True, blank=True)
    sku = ShortUUIDField(unique = True, length=10, max_length=20, prefix="pro", alphabet="abcdefghijk123456789")
    quantity = models.IntegerField(null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Product Entries"

    def __str__(self):
        return self.sku

class CartItem(models.Model):
    cart_item_id = ShortUUIDField(unique = True, length=10, max_length=20, prefix="cart-item", alphabet="abcdefghijk123456789")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    sku = models.ForeignKey(ProductEntry, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(null=True,blank=True) 

    class Meta:
        verbose_name_plural = "Cart Items"

    def __str__(self):
        return self.cart_item_id

    



