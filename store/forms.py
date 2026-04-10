from django import forms
from .models import Order, Customer, Review


class OrderForm(forms.ModelForm):
    """نموذج إنشاء طلب جديد"""

    class Meta:
        model = Order
        fields = [
            'customer_name',
            'customer_phone',
            'customer_email',
            'customer_address',
            'city',
            'product',
            'color',
            'size',
            'quantity',
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'الاسم الكامل',
                'required': True,
            }),
            'customer_phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'رقم الهاتف (06XXXXXXXX)',
                'required': True,
                'pattern': r'^0[5-7]\d{8}$',
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'البريد الإلكتروني (اختياري)',
            }),
            'customer_address': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'العنوان الكامل',
                'required': True,
            }),
            'city': forms.Select(attrs={
                'class': 'form-input',
                'required': True,
            }),
            'product': forms.Select(attrs={
                'class': 'form-input',
                'required': True,
            }),
            'color': forms.Select(attrs={
                'class': 'form-input',
                'required': True,
            }),
            'size': forms.Select(attrs={
                'class': 'form-input',
                'required': True,
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': 1,
                'max': 5,
                'value': 1,
            }),
        }


class CustomerForm(forms.ModelForm):
    """نموذج تسجيل عميل جديد"""

    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'city']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'الاسم الكامل',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'رقم الهاتف',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'البريد الإلكتروني',
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'المدينة',
            }),
        }


class ReviewForm(forms.ModelForm):
    """نموذج إضافة تقييم"""

    class Meta:
        model = Review
        fields = ['customer_name', 'rating', 'comment']
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'اسمك',
            }),
            'rating': forms.Select(attrs={
                'class': 'form-input',
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'اكتب تعليقك...',
                'rows': 4,
            }),
        }
