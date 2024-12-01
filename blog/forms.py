from django import forms
from blog.models import Newsletter


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": " Email Here..."}
            ),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Newsletter.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already subscribed.")
        return email
