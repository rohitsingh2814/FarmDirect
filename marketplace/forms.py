from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import FarmerProfile, CustomerProfile, Product


class ResetPasswordDirectForm(forms.Form):
    email = forms.EmailField(required=True, label="Registered Email")
    new_password = forms.CharField(
        widget=forms.PasswordInput,
        label="New Password",
        min_length=6,
        help_text="Enter at least 6 characters.",
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm New Password",
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if new_password and confirm_password and new_password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")
        return cleaned_data


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=[("customer", "Customer"), ("farmer", "Farmer")])
    farm_name = forms.CharField(max_length=120, required=False)
    location = forms.CharField(max_length=160, required=False)
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ["username", "email", "role", "password1", "password2", "farm_name", "location", "phone"]

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("role") == "farmer":
            if not cleaned.get("farm_name"):
                self.add_error("farm_name", "Farm name is required for farmer accounts.")
            if not cleaned.get("location"):
                self.add_error("location", "Farm location is required for farmer accounts.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            if self.cleaned_data["role"] == "farmer":
                FarmerProfile.objects.create(
                    user=user,
                    farm_name=self.cleaned_data["farm_name"],
                    location=self.cleaned_data["location"],
                    phone=self.cleaned_data.get("phone", ""),
                )
            else:
                CustomerProfile.objects.create(
                    user=user,
                    phone=self.cleaned_data.get("phone", ""),
                )
        return user


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "category",
            "description",
            "price",
            "discount_percent",
            "quantity_kg",
            "image",
            "is_trending",
            "is_available",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "price": forms.NumberInput(attrs={"min": "0.01", "step": "0.01"}),
            "discount_percent": forms.NumberInput(attrs={"min": "0", "max": "90", "step": "1"}),
            "quantity_kg": forms.NumberInput(attrs={"min": "0.01", "step": "0.01"}),
        }


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=120)
    phone = forms.CharField(max_length=20)
    delivery_address = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))
