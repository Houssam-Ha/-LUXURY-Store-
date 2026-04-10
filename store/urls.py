from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    # الصفحة الرئيسية
    path('', views.home, name='home'),

    # صفحة هودي Burberry
    path('products/hoodie/', views.hoodie_landing, name='hoodie_landing'),

    # صفحات المنتجات
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),

    # الدفع والطلبات
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/<str:order_number>/', views.order_success, name='order_success'),

    # API
    path('api/orders/', views.create_order_api, name='create_order_api'),
    path('api/search/', views.search_products, name='search_products'),

    # المدونة
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),

    # من نحن
    path('about/', views.about_us, name='about_us'),
]
