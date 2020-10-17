from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView

import stripe
from .models import Membership,UserMembership, Subscription




def get_user_membership(request):
    """this function is checking if the userMembership exist or if the user have
    membership if he have it return the user membership"""
    user_membership_qs = UserMembership.objects.filter(
        user=request.user)
    if user_membership_qs.exists():
        return user_membership_qs.first()
    else:
        return None

def get_user_subscription(request):
    """this function is checking if a user has a subscription if he have it
     return the user subscription """
    user_subscription_qs = Subscription.objects.filter(
        user_membership=get_user_membership(request))
    if user_subscription_qs.exists():
        user_subscription = user_subscription_qs.first()
        return user_subscription
    return None


def get_selected_membership(request):
    """this function is use to get what the user select on the hidden form
    i created but NOTE: it is only applicable to gthe user that has already
    select membership"""
    membership_type = request.session['selected_membership_type']
    """it returns a string so we are using filter to turn it to an object"""
    selected_membership_qs = Membership.objects.filter(
        membership_type= membership_type)
    if selected_membership_qs.exists():
        return selected_membership_qs.first()
    return None


class MembershipSelectView(LoginRequiredMixin,ListView):
    models = Membership
    queryset = Membership.objects.all()
    template_name = 'memberships/membership_list.html'

    def get_context_data(self, *args, **kwargs):
        """i created a function at the top to handle the user current membership plan to
        show when  the submit button to display in the html by overiding and adding
         my own context"""
        context = super().get_context_data(**kwargs)
        current_membership = get_user_membership(self.request)
        context['current_membership']= str(current_membership.membership)
        return context

    def post(self,request,**kwargs):
        """this request.POST.get('membership_type') is the value of the input which i
        gave to the name of the hidden input on the form"""
        global selected_membership
        #Todo : i need to remove this global if my code is having error
        selected_membership_type = request.POST.get('membership_type')
        print(selected_membership_type)
        user_membership = get_user_membership(self.request)
        user_subscription = get_user_subscription(self.request)

        # here i am filtering by what i got from the form which the user submitted
        selected_membership_qs = Membership.objects.filter(
            membership_type= selected_membership_type
        )
        if selected_membership_qs.exists():
            selected_membership = selected_membership_qs.first()

        '''
        ===========
        VALIDATION
        ===========
        '''
        """ checking if the user membership is equalt to the one he chose from the form if it is
        he would be redirected with a message """
        if user_membership.membership == selected_membership:
            if user_subscription != None:
                messages.info(self.request,'You already have this membership .Your\
                                          next payment is due {}'
                              .format('get this value get this value from stripe'))
                return HttpResponseRedirect(self.request.META.get('HTTP_REFER'))


            # assign to the session
            request.session['selected_membership_type'] = selected_membership.membership_type

            return HttpResponseRedirect(reverse('memberships:payment'))



def paymentView(request):
    """in here i am using the functions i created at the top to get user membership
    the selected membership then i imported settings to use my publishableKey"""
    user_membership = get_user_membership(request)
    selected_membership = get_selected_membership(request)
    publishKey = settings.STRIPE_PUBLISHABLE_KEY

    context = {
        'publishKey':publishKey,
        'selected_membership':selected_membership
    }
    return render(request,'memberships/membership_payment.html',context)






