from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Post, Newsletter
from django.contrib.sites.models import Site


@receiver(post_save, sender=Post)
def send_newsletter_on_new_post(sender, instance, created, **kwargs):
    if created and instance.status == "published":
        subject = f"New Post: {instance.title}"
        current_site = Site.objects.get_current()
        domain = current_site.domain
        message = render_to_string(
            "new_post_notification.html", {"post": instance, "domain": domain}
        )
        subscribers = Newsletter.objects.values_list("email", flat=True)
        send_mail(
            subject,
            message,
            "info@ssaedi.ir",
            subscribers,
            fail_silently=False,
        )
