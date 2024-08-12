
from .models import Category
# context_processors.py

def navbar_categories(request):
    # Retrieve your categories data here, for example from a model
    categories = Category.objects.all()
    return {'navbar_categories': categories}
