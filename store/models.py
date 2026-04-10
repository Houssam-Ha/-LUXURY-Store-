from django.db import models
from django.utils.text import slugify
import uuid


class Category(models.Model):
    """تصنيف المنتج"""
    name = models.CharField(max_length=100, verbose_name="اسم التصنيف")
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name="رابط التصنيف")
    description = models.TextField(blank=True, verbose_name="وصف التصنيف")

    # أبعاد الصور الموصى بها
    main_image_width = models.PositiveIntegerField(default=800, verbose_name="عرض الصورة الرئيسية")
    main_image_height = models.PositiveIntegerField(default=800, verbose_name="ارتفاع الصورة الرئيسية")
    thumbnail_width = models.PositiveIntegerField(default=400, verbose_name="عرض الصورة المصغرة")
    thumbnail_height = models.PositiveIntegerField(default=500, verbose_name="ارتفاع الصورة المصغرة")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    class Meta:
        verbose_name = "التصنيف"
        verbose_name_plural = "التصنيفات"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Product(models.Model):
    """منتج المتجر"""
    name = models.CharField(max_length=200, verbose_name="اسم المنتج")
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="رابط المنتج")
    description = models.TextField(blank=True, verbose_name="الوصف")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="السعر الحالي")
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="السعر الأصلي")
    discount_percentage = models.IntegerField(default=0, verbose_name="نسبة الخصم")

    # التصنيف
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name="التصنيف")

    # الألوان والمقاسات
    colors = models.JSONField(default=list, verbose_name="الألوان المتاحة")
    sizes = models.JSONField(default=list, verbose_name="المقاسات المتاحة")

    # المخزون
    stock = models.PositiveIntegerField(default=0, verbose_name="الكمية المتاحة")

    # الحالة
    is_featured = models.BooleanField(default=False, verbose_name="منتج مميز")
    is_active = models.BooleanField(default=True, verbose_name="نشط")

    # الصور
    main_image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="الصورة الرئيسية")

    # التواريخ
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ آخر تعديل")

    class Meta:
        verbose_name = "المنتج"
        verbose_name_plural = "المنتجات"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        # حساب نسبة الخصم تلقائياً
        if self.original_price and self.original_price > 0:
            self.discount_percentage = int(((self.original_price - self.price) / self.original_price) * 100)
        super().save(*args, **kwargs)


class Order(models.Model):
    """طلب العميل"""
    STATUS_CHOICES = [
        ('pending', 'قيد المعالجة'),
        ('confirmed', 'تم التأكيد'),
        ('shipped', 'تم الشحن'),
        ('delivered', 'تم التسليم'),
        ('cancelled', 'ملغي'),
    ]

    order_number = models.CharField(max_length=20, unique=True, verbose_name="رقم الطلب")

    # معلومات العميل
    customer_name = models.CharField(max_length=100, verbose_name="اسم العميل")
    customer_phone = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    customer_email = models.EmailField(blank=True, null=True, verbose_name="البريد الإلكتروني")
    customer_address = models.CharField(max_length=200, verbose_name="العنوان")
    city = models.CharField(max_length=50, verbose_name="المدينة")

    # تفاصيل الطلب
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders', verbose_name="المنتج")
    color = models.CharField(max_length=50, verbose_name="اللون المختار")
    size = models.CharField(max_length=10, verbose_name="المقاس المختار")
    quantity = models.PositiveIntegerField(default=1, verbose_name="الكمية")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="السعر الإجمالي")

    # الحالة
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="حالة الطلب")
    notes = models.TextField(blank=True, null=True, verbose_name="ملاحظات")

    # التواريخ
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الطلب")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ آخر تحديث")

    class Meta:
        verbose_name = "الطلب"
        verbose_name_plural = "الطلبات"
        ordering = ['-created_at']

    def __str__(self):
        return f"طلب #{self.order_number} - {self.customer_name}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            # إنشاء رقم طلب فريد
            date_part = self.created_at.strftime('%Y%m%d') if self.created_at else '20260101'
            random_part = uuid.uuid4().hex[:6].upper()
            self.order_number = f"LUX-{date_part}-{random_part}"
        super().save(*args, **kwargs)


class Customer(models.Model):
    """عميل المتجر"""
    name = models.CharField(max_length=100, verbose_name="الاسم")
    phone = models.CharField(max_length=20, unique=True, verbose_name="رقم الهاتف")
    email = models.EmailField(blank=True, null=True, verbose_name="البريد الإلكتروني")
    city = models.CharField(max_length=50, blank=True, verbose_name="المدينة")
    orders_count = models.PositiveIntegerField(default=0, verbose_name="عدد الطلبات")
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="إجمالي المشتريات")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التسجيل")

    class Meta:
        verbose_name = "العميل"
        verbose_name_plural = "العملاء"

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    """مقال المدونة"""
    title = models.CharField(max_length=200, verbose_name="العنوان")
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name="الرابط")
    excerpt = models.CharField(max_length=300, blank=True, verbose_name="نبذة مختصرة")
    content = models.TextField(verbose_name="المحتوى")
    author = models.CharField(max_length=100, default="LUXARO", verbose_name="الكاتب")

    image = models.ImageField(upload_to='blog/', blank=True, null=True, verbose_name="صورة المقال")

    is_published = models.BooleanField(default=False, verbose_name="منشور")
    published_at = models.DateTimeField(blank=True, null=True, verbose_name="تاريخ النشر")

    meta_description = models.CharField(max_length=160, blank=True, verbose_name="وصف SEO")
    meta_keywords = models.CharField(max_length=200, blank=True, verbose_name="كلمات مفتاحية")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ آخر تعديل")

    class Meta:
        verbose_name = "مقال"
        verbose_name_plural = "المقالات"
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)


class Review(models.Model):
    """تقييم العميل"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="المنتج")
    customer_name = models.CharField(max_length=100, verbose_name="اسم العميل")
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)], default=5, verbose_name="التقييم")
    comment = models.TextField(verbose_name="التعليق")
    is_approved = models.BooleanField(default=False, verbose_name="موافق عليه")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التقييم")

    class Meta:
        verbose_name = "التقييم"
        verbose_name_plural = "التقييمات"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer_name} - {self.product.name} ({self.rating} نجوم)"


class ProductImage(models.Model):
    """صورة المنتج"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="المنتج")
    image = models.ImageField(upload_to='products/', verbose_name="الصورة")
    alt_text = models.CharField(max_length=200, blank=True, verbose_name="وصف الصورة")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتيب العرض")
    is_main = models.BooleanField(default=False, verbose_name="صورة رئيسية")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")

    class Meta:
        verbose_name = "صورة المنتج"
        verbose_name_plural = "صور المنتجات"
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"صورة {self.order} - {self.product.name}"

    def save(self, *args, **kwargs):
        # إذا كانت هذه هي الصورة الرئيسية، اجعل جميع الصور الأخرى غير رئيسية
        if self.is_main:
            ProductImage.objects.filter(product=self.product, is_main=True).exclude(id=self.id).update(is_main=False)
        super().save(*args, **kwargs)
