from .models import ProductCategory


def categories(request):
    # Retrieve all categories from the database
    categories = ProductCategory.objects.all()
    return {'categories': categories}
