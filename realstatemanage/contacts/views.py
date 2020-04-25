from django.shortcuts import render,redirect
from .models import Contacts
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User
# Create your views here.
def contact(request):
    if request.method=='POST':
        listing_id=request.POST['listing_id']
        listing=request.POST['listing']
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        message=request.POST['message']
        user_id=request.POST['user_id']
        realtor_email=request.POST['realtor_email']
        if request.user.is_authenticated:
            user_id=request.user.id
            has_contacted=Contacts.objects.all().filter(listing_id=listing_id,user_id=user_id)
            if has_contacted:
                messages.error(request,'You have already made an enquiry for this listing')
                return redirect('/listing/' + listing_id)

        contact=Contacts(listing_id=listing_id,listing=listing,name=name,email=email,phone=phone,message=message,user_id=user_id)
        contact.save()
        send_mail(
            'Property Listing inquiry',
            'There has been an inquiry for '+listing+'.',
            'samarthvaru111@gmail.com',[str(realtor_email)],fail_silently=False
        )
        messages.success(request,'Your request has been sent, your realtor will contact you soon.')
        return redirect('/listing/'+listing_id)