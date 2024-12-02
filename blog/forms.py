from django import forms
from django_summernote.widgets import SummernoteWidget
from blog.models import Newsletter, Post, Comment, Contact


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


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "category",
            "image",
            "thumbnail",
            "tags",
            "status",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": SummernoteWidget(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "thumbnail": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "tags": forms.SelectMultiple(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user:
            instance.author = user
        if commit:
            instance.save()
        return instance


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Comment", "rows": 5}
            ),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["first_name", "email", "phone_number", "subject", "message"]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "First Name"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
            "phone_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Phone Number"}
            ),
            "subject": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Subject"}
            ),
            "message": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Message", "rows": 5}
            ),
        }
