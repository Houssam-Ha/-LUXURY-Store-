from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Order, Customer, BlogPost, Review, Category, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']

    fieldsets = (
        ('معلومات التصنيف', {
            'fields': ('name', 'slug', 'description')
        }),
        ('أبعاد الصور الموصى بها', {
            'fields': ('main_image_width', 'main_image_height', 'thumbnail_width', 'thumbnail_height'),
            'description': 'حدد الأبعاد المثالية للصور في هذا التصنيف'
        }),
    )


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'order', 'is_main']
    ordering = ['order']

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.verbose_name = "صور المنتج"
        formset.verbose_name_plural = "صور المنتج (يمكنك إضافة أكثر من صورة)"
        return formset


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price_display', 'original_price', 'discount_badge', 'stock', 'is_featured', 'is_active', 'created_at']
    list_filter = ['is_featured', 'is_active', 'category', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['-created_at']
    inlines = [ProductImageInline]

    fieldsets = (
        ('معلومات المنتج', {
            'fields': ('name', 'slug', 'description', 'category')
        }),
        ('الأسعار', {
            'fields': ('price', 'original_price', 'discount_percentage')
        }),
        ('الألوان والمقاسات', {
            'fields': ('colors', 'sizes')
        }),
        ('المخزون والحالة', {
            'fields': ('stock', 'is_featured', 'is_active')
        }),
        ('الصور', {
            'fields': ('main_image',),
            'description': '⚠️ الحجم المطلوب للصورة الرئيسية: 800×800px | الصور المصغرة: 400×500px. يمكنك إضافة صور إضافية في الأسفل.'
        }),
    )

    def price_display(self, obj):
        return f"{obj.price} درهم"
    price_display.short_description = "السعر"

    def original_price(self, obj):
        if obj.original_price:
            return f"{obj.original_price} درهم"
        return "-"
    original_price.short_description = "السعر الأصلي"

    def discount_badge(self, obj):
        if obj.discount_percentage > 0:
            color = 'green' if obj.discount_percentage < 20 else 'orange' if obj.discount_percentage < 50 else 'red'
            return format_html(
                f'<span style="color: {color}; font-weight: bold;">-{obj.discount_percentage}%</span>'
            )
        return "-"
    discount_badge.short_description = "الخصم"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer_info', 'product_info', 'total_price_display', 'status_badge', 'city', 'created_at']
    list_filter = ['status', 'city', 'created_at']
    search_fields = ['order_number', 'customer_name', 'customer_phone']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    ordering = ['-created_at']

    def customer_info(self, obj):
        return format_html(f"{obj.customer_name}<br><small>{obj.customer_phone}</small>")
    customer_info.short_description = "العميل"
    customer_info.allow_tags = True

    def product_info(self, obj):
        return format_html(f"{obj.product.name}<br><small>{obj.color} | {obj.size}</small>")
    product_info.short_description = "المنتج"
    product_info.allow_tags = True

    def total_price_display(self, obj):
        return f"{obj.total_price} درهم"
    total_price_display.short_description = "الإجمالي"

    def status_badge(self, obj):
        colors = {
            'pending': 'gray',
            'confirmed': 'blue',
            'shipped': 'orange',
            'delivered': 'green',
            'cancelled': 'red',
        }
        status_names = dict(Order.STATUS_CHOICES)
        color = colors.get(obj.status, 'gray')
        return format_html(
            f'<span style="background: {color}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px;">{status_names[obj.status]}</span>'
        )
    status_badge.short_description = "الحالة"


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'city', 'orders_count', 'total_spent_display', 'created_at']
    list_filter = ['city', 'created_at']
    search_fields = ['name', 'phone', 'email']
    ordering = ['-created_at']

    def total_spent_display(self, obj):
        return f"{obj.total_spent} درهم"
    total_spent_display.short_description = "إجمالي المشتريات"


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_published', 'published_at', 'author', 'created_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-published_at', '-created_at']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'product', 'rating_display', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'rating', 'created_at']
    search_fields = ['customer_name', 'comment', 'product__name']
    ordering = ['-created_at']

    def rating_display(self, obj):
        stars = "★" * obj.rating + "☆" * (5 - obj.rating)
        color = 'green' if obj.rating >= 4 else 'orange' if obj.rating >= 3 else 'red'
        return format_html(f'<span style="color: {color};">{stars}</span>')
    rating_display.short_description = "التقييم"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_tag', 'alt_text', 'order', 'is_main', 'created_at']
    list_filter = ['is_main', 'created_at']
    search_fields = ['product__name', 'alt_text']
    ordering = ['product', 'order']

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />', obj.image.url)
        return "-"
    image_tag.short_description = "الصورة"
