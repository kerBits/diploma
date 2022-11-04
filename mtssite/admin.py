from django import forms
from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

# Register your models here.
from .models import News, CustomUser, Office, ProdCodes, Product, ProductsInOffice

@admin.register(ProductsInOffice)
class ProductsInOfficeAdmin(admin.ModelAdmin):
    model = ProductsInOffice

    list_display = (
        'product',
        'office_id',
        'quantity',
    )

    list_filter = (
        'product',
    )

    list_editable = (
        'quantity',
    )

    search_fields = (
        'office_id',
    )

    ordering = ('office_id', )


@admin.register(ProdCodes)
class ProdCodesAdmin(admin.ModelAdmin):
    model = ProdCodes

    list_display = (
        'id',
        'code',
        'type',
    )

    list_filter = (
        'code',
        'type',
    )

    list_editable = (
        'code',
        'type',
    )

    search_fields = (
        'code',
        'type'
    )

    ordering = ('code',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product

    list_display = (
        'id',
        'prod_name',
        'code',
        'manufacturer',
        'description',
    )

    list_filter = (
        'prod_name',
        'code',
    )

    list_editable = (
        'prod_name',
        'code',
        'manufacturer',
        'description',
    )

    search_fields = (
        'prod_name',
        'manufacturer',
    )

    ordering = ('prod_name',)


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    model = Office

    list_display = (
        'id',
        'officename',
        'officeaddress',
        'officeheadinfo',
    )

    list_filter = (
        'officename',
    )

    list_editable = (
        'officename',
        'officeaddress',
        'officeheadinfo',
    )

    search_fields = (
        'officename',
        'officeaddress',
    )

    ordering = ('officename',)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    model = News

    list_display = (
        "id",
        "title",
        "subtitle",
        "slug",
        "publish_date",
        "published",
    )

    list_filter = (
        "published",
        "publish_date",
    )
    list_editable = (
        "title",
        "subtitle",
        "slug",
        "publish_date",
        "published",
    )
    search_fields = (
        "title",
        "subtitle",
        "slug",
        "body",
    )
    prepopulated_fields = {
        "slug" : (
            "title",
            "subtitle",
        )
    }
    date_hierarchy = "publish_date"
    save_on_top = True
  

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('personnel_number', 'email', 'fio')

    def clean_password(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=("Password"),
        help_text=("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = CustomUser
        fields = ('personnel_number', 'password', 'email', 'fio', 'shop_number', 'is_active', 'is_admin')


class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('personnel_number', 'fio', 'shop_number', 'is_active', 'is_admin')
    list_filter = ('shop_number',)
    fieldsets = (
        (None, {'fields': ('personnel_number', 'password')}),
        ('Personal info', {'fields': ('fio', 'email', 'shop_number')}),
        ('Permissions', {'fields': ('is_admin', 'groups', '')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('personnel_number', 'email', 'fio', 'shop_number', 'password1', 'password2'),
        }),
    )

    search_fields = ('personnel_number', 'shop_number', 'fio',)
    ordering = ('fio',)
    filter_horizontal = ()


admin.site.register(CustomUser, UserAdmin)