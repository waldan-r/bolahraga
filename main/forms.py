from django.forms import ModelForm
from main.models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 
                  'price', 
                  'description', 
                  'thumbnail',
                  'stock',
                  'category',
                  'is_featured',]