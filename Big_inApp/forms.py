# forms.py
# from django import forms
# from .models import Video

# class VideoForm(forms.ModelForm):
#     class Meta:
#         model = Video
#         fields = ['title', 'video_id']



# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from .models import CustomUser, Feedback, ProductSellEntry
# from django import forms
#
#
# class BuyerRegistrationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ('email', 'password', 'user_type', 'name')
#
#     password = forms.CharField(
#         label="Password",
#         strip=False,
#         widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
#     )
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.user_type = 'buyer'
#         if commit:
#             user.save()
#         return user
#
#
# class SellerRegistrationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ('email', 'password', 'user_type', 'first_name', 'last_name', 'address', 'dob', 'gender', 'photo', 'citizenship_card')
#
#     password = forms.CharField(
#         label="Password",
#         strip=False,
#         widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
#     )
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.user_type = 'seller'
#         if commit:
#             user.save()
#         return user
#
