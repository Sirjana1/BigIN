from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.urls import reverse
from django.db.models import Q
from django.conf import settings
from decimal import Decimal
# from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
# from .models import Video
# from .forms import VideoForm
import json
import requests
from django.shortcuts import render, redirect
from .models import Feedback, ProductSellEntry, CustomUser, ProductCategory, Article,\
    BuyerProfile, SellerProfile, Order, Video
from django.contrib import messages




def initkhalti(request):
    url = "https://a.khalti.com/api/v2/epayment/initiate/"
    return_url = request.POST.get('return_url')
    website_url = request.POST.get('return_url')
    amount = request.POST.get('amount')
    purchase_order_id = request.POST.get('purchase_order_id')


    print("url",url)
    print("return_url",return_url)
    print("web_url",website_url)
    print("amount",amount)
    print("purchase_order_id",purchase_order_id)
    payload = json.dumps({
        "return_url": return_url,
        "website_url": website_url,
        "amount": float(amount) * 100,
        "purchase_order_id": purchase_order_id,
        "purchase_order_name": "test",
        "customer_info": {
        "name": "Sirjana Chaudhary",
        "email": "bigIN@gmail.com",
        "phone": "9800000005"
        }
    })

    headers = {
        'Authorization': 'key live_secret_key_68791341fdd94846a146f0457ff7b455',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    new_res = json.loads(response.text)
    return redirect(new_res['payment_url'])


def verifyKhalti(request):
    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    if request.method == 'GET':
        headers = {
            'Authorization': 'key live_secret_key_68791341fdd94846a146f0457ff7b455',
            'Content-Type': 'application/json',
        }
        pidx = request.GET.get('pidx')
        purchase_order_id = request.GET.get('purchase_order_id')
        data = json.dumps({
            'pidx': pidx
        })
        res = requests.request('POST', url, headers=headers, data=data)
        print(res)
        print(res.text)

        new_res = json.loads(res.text)
        print(new_res)

        if new_res['status'] == 'Completed':
            product = ProductSellEntry.objects.get(id=purchase_order_id)
            user = request.user
            Order.objects.create(product=product, ordered_by=user)
            print("Payment success.")
        
        else:
            print("Error in payment.")

        return redirect('home_page')


def search_view(request):
    query = request.GET.get('search_query')
    results = []

    if query:
     results = ProductSellEntry.objects.filter(Q(product_name__icontains=query) | Q(description__icontains=query))
    return render(request, 'search_results.html', {'query': query, 'results': results})


def seller_profile(request, seller_id):
    seller = SellerProfile.objects.get(id=seller_id)
    return render(request, 'sellerprofile.html', context={"seller": seller})


def custom_logout(request):
    logout(request)
    return redirect('home_page')


def articles(request):
    
    article_list = Article.objects.all()
    return render(request, 'articles.html', context={"article_list": article_list})


def category_products(request, category_id):
    category = ProductCategory.objects.get(pk=category_id)
    products = ProductSellEntry.objects.filter(category=category)

    context = {
        'category': category,
        'products': products,

    }
    return render(request, 'category_products.html', context)


def feedback_hub(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment = request.POST.get('comment')

        if name and email and comment:
            Feedback.objects.create(name=name, email=email, comment=comment)
            messages.success(request, 'Thank you for your feedback!')
            return redirect('home_page')
        else:
            messages.error(request, 'Please fill in all the fields.')
    return render(request, 'feedbackHub.html')


def product_sell_entry(request):
    
    categories = ProductCategory.objects.all()
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        photo = request.FILES.get('photo')  # Get the uploaded photo file
        citizenship = request.POST.get('citizenship')
        product_name = request.POST.get('product_name')
        product_image = request.FILES.get('product_image')  # Get the uploaded product image file
        category_id = request.POST.get('category')  # Assuming you have a select field for category
        offered_price = request.POST.get('offered_price')
        description = request.POST.get('product_description')

        # Validate form data (add your own validation logic)
        if (
                first_name and last_name and email and photo and citizenship and
                product_name and product_image and category_id and offered_price and description
        ):
            # Convert category_id to an integer if necessary
            category_id = int(category_id)

            # Create a ProductSellEntry object with all the fields
            ProductSellEntry.objects.create(
                seller_profile=SellerProfile.objects.get(user=request.user),
                first_name=first_name,
                last_name=last_name,
                email=email,
                photo=photo,
                citizenship=citizenship,
                product_name=product_name,
                product_image=product_image,
                category_id=category_id,
                offered_price=offered_price,
                description=description,
                status=0,
            )
            messages.success(request, 'Product entry submitted successfully!')
            return redirect('home_page')
        else:
            messages.error(request, 'Please fill in all the required fields.')

    return render(request, 'product_sell_entry.html', {'categories': categories})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                if user.is_seller():
                    return redirect('product_sell_entry')
                return redirect('home_page')
            else:
                messages.error(request, 'Login failed. Please check your credentials.')
        else:
            messages.error(request, 'Please fill in all the required fields.')
    else:
        return render(request, 'login.html')

    return render(request, 'login.html')


def buyer_registration(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')

        if email and password and name:
            try:
                user = CustomUser.objects.create_user(email=email, username=email, password=password, user_type='buyer')
                buyer_profile = BuyerProfile.objects.create(user=user, name=name)
                buyer_profile.save()
                login(request, user)  # Log in the user immediately after registration
                messages.success(request, 'Registration successful!')
                return redirect('home_page')
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
        else:
            messages.error(request, 'Please fill in all the required fields.')

            # bf = BuyerProfile.objects.all()
    return render(request, 'buyerSignup.html')


def seller_registration(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        photo = request.FILES.get("photo")
        citizenship_card = request.FILES.get("citizenship_card")

        if email and password and first_name and last_name and address and dob and gender and photo and citizenship_card:
            try:
                user = CustomUser.objects.create_user(email=email, username=email, password=password,
                                                      user_type='seller')
                seller_profile = SellerProfile.objects.create(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    address=address,
                    dob=dob,
                    gender=gender,
                    photo=photo,
                    citizenship_card=citizenship_card
                )
                seller_profile.save()
                login(request, user)  # Log in the user immediately after registration
                messages.success(request, 'Registration successful!')
                return redirect('product_sell_entry')
            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
        else:
            messages.error(request, 'Please fill in all the required fields.')
    return render(request, 'sellerSignup.html')


def home(request):
    queryset = ProductSellEntry.objects.filter(status=1).order_by('-created_at')
    ctx = {"product_list": queryset}
    return render(request, 'home.html', context=ctx)





def videos(request):
    v = Video.objects.all()
    return render(request, 'videos.html', context={"v":v})

def chat(request):
    return render(request, 'chat.html')







# def video_list(request):
#     videos = Video.objects.all()
#     return render(request, 'video_list.html', {'videos': videos})


# def add_video(request):
#     if request.method == 'POST':
#         form = VideoForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('video_list')
#     else:
#         form = VideoForm()
#     return render(request, 'add_video.html', {'form': form})

