from django.contrib import admin
from .models import Feedback, CustomUser, BuyerProfile, SellerProfile, ProductCategory,\
    ProductSellEntry, Article, Order, Video

admin.site.register(Feedback)
admin.site.register(BuyerProfile)
admin.site.register(SellerProfile)
admin.site.register(CustomUser)
admin.site.register(ProductCategory)
admin.site.register(ProductSellEntry)
admin.site.register(Article)
admin.site.register(Order)
admin.site.register(Video)


