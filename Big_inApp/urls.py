"""Big_in URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from .views import home, login_view, buyer_registration, seller_profile, seller_registration,\
    category_products, product_sell_entry, feedback_hub, articles, custom_logout, search_view, \
    initkhalti, verifyKhalti,  videos, chat
urlpatterns = [
    path('logout/', custom_logout, name='logout'),

    path('products/<int:category_id>/', category_products, name='category_products'),
    path("product-sell/", product_sell_entry, name="product_sell_entry"),

    path('login/', login_view, name='login'),
    path('register/buyer/', buyer_registration, name='buyer_registration'),
    path('register/seller/', seller_registration, name='seller_registration'),

    path('feedback-hub/', feedback_hub, name='feedback_hub'),
    path('articles', articles, name='articles'),
    path("home/", home, name="home_page"),
    path('', home, name='home_page'),

    path('seller-profile/<int:seller_id>/', seller_profile, name='seller_profile'),
    path('search/', search_view, name='search_view'),
    path('video/', videos, name='videos'),
    path('initiate', initkhalti,name="initiate"),
    path('verify', verifyKhalti,name="verify"),
    path('chat/', chat, name='chat'),
    # path('video_embed/', video_embed, name="video_embed"),
    # path('videos/', video_list, name='video_list'),
    # path('add_video/', add_video, name='add_video'),
    

 
]
