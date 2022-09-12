from re import L
from tokenize import String
from typing import List
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from .models import ReimbursementRequest as rr
from django.contrib.auth.models import User
from .forms import SubmitRequest, TrackSpending
from django.core.mail import send_mail

# Create your views here.
Privlaged = ['President', 'Captain', 'Vice-President', 'Treasurer', 'Equipment Manager']

def title(response):
    if response.user.is_authenticated:
        return HttpResponseRedirect("/request/")
    return render(response, "main/title.html", {})

def current_requests(response):
    if not response.user.is_authenticated:
        return HttpResponseRedirect("/login")

    # Determine Order of Requests
    reversed = False
    rev = ""
    order = "date"
    if response.method == "POST":
        if "Sorting" in response.POST:
            if "order" in response.POST:
                reversed = True
                rev = ""
            elif "reverse" in response.POST:
                reversed = False
                rev = "-"

            order = response.POST.get('Sorting','')
        else:
            email_title = 'Reimbursement Request ' 
            email_message = 'Your Reimbursement Request has been '
            email_messagep2 = '.\nIf you have any problems or concerns please contact\n'
            email_messagep2 += response.user.first_name + ' ' + response.user.last_name + '(' + response.user.email + ')\n'
            email_messagep2 += 'Thank you'

            if "Approved" in response.POST:
                id = response.POST.get("Approved")
                email_message += "approved" + email_messagep2
                email_title += "Approved"
                rr.objects.filter(pk=int(id)).update(approved=True)
            elif "Declined" in response.POST:
                id = response.POST.get("Declined")
                email_title += "Declined"
                email_message += "declined" + email_messagep2
                rr.objects.filter(pk=int(id)).update(declined=True)

            send_mail(email_title, email_message, 'lsurowingtreasury@gmail.com', [rr.objects.get(id=int(id)).user.email], fail_silently=False) # This only send to milesbellaire456



    if response.user.is_staff:
        items = rr.objects.order_by(rev+order)
    else:
        items = response.user.reimbursementrequest_set.order_by(rev+order)


    return render(response, "main/current-requests.html", {"requests":items, "is_staff":response.user.is_staff, "reversed":reversed, "order":order, "Order":order.capitalize()})

def request(response):
    if not response.user.is_authenticated:
        return HttpResponseRedirect("/login")
    if response.method == "POST":
        print(response.POST)
        print(response.FILES)
        form = SubmitRequest(response.POST, response.FILES)
        if form.is_valid():
            r_request = rr(user=response.user, reason=form.cleaned_data["reason"], amount=form.cleaned_data["amount"], payable_to=form.cleaned_data["payable_to"], receipt=form.cleaned_data.get("receipt"))
            r_request.save()

            email_message = response.user.first_name + ' ' + response.user.last_name + ' has submited a new reimbursement request.\n'
            email_message += 'They have requested $' + str(r_request.amount) + ' for ' + r_request.reason
            staff_list = []
            for user in User.objects.all():
                if user.is_staff:
                    staff_list.append(user.email)
            send_mail('Reimbursement Request Received', email_message, 'lsurowingtreasury@gmail.com', staff_list, fail_silently=False)

            return HttpResponseRedirect("/current-requests/")
    else:
        form = SubmitRequest()
    return render(response, "main/request.html", {"form":form})

def budget_tracking(response):
    if not response.user.is_authenticated or not response.user.is_staff:
        return HttpResponseRedirect("/login")
    return render(response, "main/budget_tracking.html", {})

def tracking(response):
    if not response.user.is_authenticated or not response.user.is_staff:
        return HttpResponseRedirect("/login")
    if response.method == "POST":
        form = TrackSpending(response.POST)
        if form.is_valid():
            print(response.POST)
    else:
        form = TrackSpending()
    return render(response, "main/tracking.html", {"form":form})

def pivot_table(response):
    if not response.user.is_authenticated or not response.user.is_staff:
        return HttpResponseRedirect("/login")
    return render(response, "main/pivot_table.html", {})

def spreadsheet(response):
    if not response.user.is_authenticated or not response.user.is_staff:
        return HttpResponseRedirect("/login")
    return render(response, "main/spreadsheet.html", {})

def purchase_request(response):
    if not response.user.is_authenticated or not user_is_(Privlaged, response.user):
        return HttpResponseRedirect("/login")
    return render(response, "main/spreadsheet.html", {})

def receipts(response):
    if not response.user.is_authenticated:
        return HttpResponseRedirect("/login")
    return render(response, "main/receipt.html", {})


def user_is_(groups, user):
    return user.groups.filter(name__in=groups).exists()