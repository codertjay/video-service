from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.conf import settings

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

MEMBERSHIP_CHOICES = (
    ('Enterprise', 'ent'),
    ('Professional', 'pro'),
    ('Free', 'free')
)


class Membership(models.Model):
    slug = models.SlugField(unique=True)
    membership_type = models.CharField(choices=MEMBERSHIP_CHOICES
                                       , max_length=30, default='Free')
    price = models.IntegerField(default=15)
    stripe_plan_id = models.CharField(max_length=43)

    def __str__(self):
        return self.membership_type


# this is the first model which is created because i use signal
class UserMembership(models.Model):
    user = models.OneToOneField(User
                                , on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=43)
    membership = models.ForeignKey(Membership
                                   , on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username


def post_save_usermembership_create(sender, instance, created, *args, **kwargs):
    """this post save i use it to create a usermembersip once a user has being created"""
    if created:
        UserMembership.objects.get_or_create(user=instance)
    user_membership, created = UserMembership.objects.get_or_create(user=instance)

    if user_membership.stripe_customer_id is None or user_membership.stripe_customer_id == '':
        """ creating a stripe id for a user using his email"""
        # Todo : i need to change the customer id from my stripe api key to the one i
        #  commented
        # new_customer_id = stripe.Customer.create(email=instance.email)
        new_customer_id = stripe.api_key
        user_membership.stripe_customer_id = new_customer_id
        user_membership.save()


"""this is the signal that is being called"""
post_save.connect(post_save_usermembership_create, sender=User)


class Subscription(models.Model):
    user_membership = models.ForeignKey(UserMembership, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=40)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_membership.user.username
