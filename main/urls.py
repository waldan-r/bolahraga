from django.urls import path
from main.views import *


app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('add-product/', add_product, name='add_product'),
    path('product/<str:id>/', show_product, name='show_product'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:product_id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:product_id>/', show_json_by_id, name='show_json_by_id'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('product/<uuid:id>/edit', edit_product, name='edit_product'),
    path('delete/<uuid:pk>/', delete_product, name='delete_product'),
    path('get-product-json/', get_product_json, name='get_product_json'),
    path('add-product-ajax/', add_product_ajax, name='add_product_ajax'), 
    path('get-product/<uuid:pk>/', get_product_for_edit, name='get_product_for_edit'),
    path('update-product-ajax/<uuid:pk>/', update_product_ajax, name='update_product_ajax'),
    path('login-ajax/', login_ajax, name='login_ajax'),
    path('register-ajax/', register_ajax, name='register_ajax'),
    path('json/', show_json, name='show_json'), 
    path('create-flutter/', create_product_flutter, name='create_product_flutter'),
]