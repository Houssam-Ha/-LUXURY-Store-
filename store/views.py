from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
import json
from .models import Product, Order, BlogPost, Review, Category
from .forms import OrderForm


def home(request):
    """الصفحة الرئيسية - Homepage"""
    # جلب المنتجات المميزة
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:6]

    # جلب جميع التصنيفات
    categories = Category.objects.all()

    # جلب آخر المنتجات
    latest_products = Product.objects.filter(is_active=True).order_by('-created_at')[:4]

    context = {
        'featured_products': featured_products,
        'categories': categories,
        'latest_products': latest_products,
        'page_title': 'LUXARO - متجر الملابس الفاخر',
    }
    return render(request, 'home.html', context)


def hoodie_landing(request):
    """صفحة هودي Burberry - Product Landing Page"""
    # جلب المنتج المميز
    product = Product.objects.filter(is_featured=True, is_active=True).first()

    # جلب التقييمات الموافق عليها
    reviews = Review.objects.filter(is_approved=True)[:6]

    context = {
        'product': product,
        'reviews': reviews,
        'page_title': 'LUXARO - هودي Burberry الفاخر',
    }
    return render(request, 'landing_Hoodie.html', context)


def product_detail(request, slug):
    """تفاصيل المنتج"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    reviews = Review.objects.filter(product=product, is_approved=True)

    # منتجات مشابهة
    related_products = Product.objects.filter(
        is_active=True,
        is_featured=True
    ).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'reviews': reviews,
        'related_products': related_products,
        'page_title': product.name,
    }
    return render(request, 'product.html', context)


def checkout(request):
    """صفحة الدفع"""
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            return redirect('order_success', order_number=order.order_number)
    else:
        form = OrderForm()

    # جلب المنتج من الجلسة أو URL
    product_id = request.GET.get('product')
    product = None
    if product_id:
        product = Product.objects.filter(id=product_id, is_active=True).first()

    context = {
        'form': form,
        'product': product,
        'page_title': 'إتمام الطلب',
    }
    return render(request, 'checkout.html', context)


def order_success(request, order_number):
    """صفحة نجاح الطلب"""
    order = get_object_or_404(Order, order_number=order_number)
    context = {
        'order': order,
        'page_title': 'تم استلام طلبك',
    }
    return render(request, 'order_success.html', context)


def blog_list(request):
    """قائمة مقالات المدونة"""
    posts = BlogPost.objects.filter(is_published=True).order_by('-published_at', '-created_at')
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {
        'posts': posts,
        'page_title': 'المدونة - LUXARO',
    }
    return render(request, 'blog/list.html', context)


def blog_detail(request, slug):
    """تفاصيل المقال"""
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)

    # مقالات مشابهة
    related_posts = BlogPost.objects.filter(
        is_published=True
    ).exclude(id=post.id)[:3]

    context = {
        'post': post,
        'related_posts': related_posts,
        'page_title': post.title,
    }
    return render(request, 'blog/detail.html', context)


def about_us(request):
    """صفحة من نحن"""
    context = {
        'page_title': 'من نحن - LUXARO',
    }
    return render(request, 'about.html', context)


@csrf_exempt
@require_POST
def create_order_api(request):
    """API endpoint لإنشاء طلب"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = OrderForm(data)

            if form.is_valid():
                order = form.save()
                return JsonResponse({
                    'success': True,
                    'order_number': order.order_number,
                    'message': 'تم استلام طلبك بنجاح'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                }, status=400)

        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'بيانات غير صحيحة'
            }, status=400)

    return JsonResponse({'success': False}, status=405)


def search_products(request):
    """البحث عن المنتجات"""
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        is_active=True,
        name__icontains=query
    )[:10]

    results = [
        {
            'id': p.id,
            'name': p.name,
            'price': str(p.price),
            'slug': p.slug,
            'image': p.main_image.url if p.main_image else (p.images.first().image.url if p.images.first() else None)
        }
        for p in products
    ]

    return JsonResponse({'results': results})
