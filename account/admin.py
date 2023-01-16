from django.contrib import admin
from django import forms

from django.contrib.auth.admin import UserAdmin as ClinicUserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import User

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('employee_number', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password mismatch!")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text= ("Raw passwords are not stored, so there is no way to see "
                  "this user's password, but you can change the password "
                  "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = User
        fields = ('employee_number', 'email')

        def clean_password(self):
            return self.initial["password"]


        
class UserAdmin(ClinicUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        (None, {'fields': ('password',)}),
        ('Personal Info', {'fields': ('email', )}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser','is_active','user_permissions' ,'groups')}),
        ('Roles', {'fields': ('is_doctor', 'is_labtech', 'is_reception')}),
        )

    add_fieldsets = (
            (None, {
                'classes': ('wide',),
                'fields': ('email', 'employee_number', 'password1', 'password2'),
            }),
        )

    list_display = ('employee_number', 'email', 'is_staff')
    search_fields = ('email',)
    ordering = ('email',)

    # filter_horizontal = ()


admin.site.register(User, UserAdmin)