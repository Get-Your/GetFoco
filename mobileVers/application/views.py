from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate, logout
#from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from.models import User

from django.db import IntegrityError

from .forms import UserForm, AddressForm, EligibilityForm, programForm
from .backend import addressCheck, validateUSPS, broadcast_email, broadcast_sms, qualification


formPageNum = 6

# Notes: autofill in empty rows for users who don't fill out all of their info?


# TODO: Grace - possibly make a function that automatically returns next step of the page?
# Should all of these view functions look up at this one function and figure out where they need to go next
# based on which page they are on?

# TODO: Grace - add user authorization for next pages

# first index page we come into
def index(request):
    logout(request)
    print(request.user)
    return render(request, 'application/index.html',)

def address(request):
    if request.method == "POST": 
        form = AddressForm(request.POST or None)
        print(form.data)
        if form.is_valid():
            dict = validateUSPS(form)
            try:
                instance = form.save(commit=False)
                instance.user_id = request.user
                #addressResult returns true or false, use this as logic for leading to available.html/notavailable.html
                addressResult = addressCheck(dict['AddressValidateResponse']['Address']['Address2'],)
                if addressResult == True:
                    instance.n2n = True
                    print("n2n instance is true")
                else:
                    instance.n2n = False
                    print("n2n instance is false")
                instance.sanitizedAddress = dict['AddressValidateResponse']['Address']['Address2'], 
                instance.sanitizedAddress2 = dict['AddressValidateResponse']['Address']['Address1'], 
                instance.sanitizedCity = dict['AddressValidateResponse']['Address']['City'], 
                instance.sanitizedState = dict['AddressValidateResponse']['Address']['State'], 
                instance.sanitizedZipCode = int(dict['AddressValidateResponse']['Address']['Zip5'])

                instance.save()
            except IntegrityError:
                print("User already has information filled out for this section")

            return redirect(reverse("application:addressCorrection"))
    else:
        form = AddressForm()
    return render(request, 'application/address.html', {
        'form':form,
        'step':2,
        'request.user':request.user,
        'formPageNum':formPageNum,
    })

def addressCorrection(request):
    return render(request, 'application/addressCorrection.html',  {
        'step':2,
        'formPageNum':formPageNum,
        'program_string': request.user.addresses.address + " " + request.user.addresses.address2 + " " + request.user.addresses.city + " " + request.user.addresses.state + " " + str(request.user.addresses.zipCode),
        'program_string_2': request.user.addresses.sanitizedAddress + " " + request.user.addresses.sanitizedAddress2 + " " + request.user.addresses.sanitizedCity + " " + request.user.addresses.sanitizedState + " " + str(request.user.addresses.sanitizedZipCode),
    })

def n2n(request):
    if request.user.addresses.n2n == True:
        return redirect(reverse("application:available"))
    else:
        return redirect(reverse("application:finances")) 


def account(request):
    if request.method == "POST": 
        # maybe also do some password requirements here too
        form = UserForm(request.POST)
        if form.is_valid():
            # Add Error MESSAGE IF THEY DIDN"T WRITE CORRECT THINGS TO SUBMIT
            # Make sure password isn't getting saved twice
            print(form.data)
            try:
                user = form.save()
                login(request,user)
                print("userloggedin")
            except AttributeError:
                print("user error, login not saved, user is: " + str(user))
            return redirect(reverse("application:address"))
    else:
        form = UserForm()
    return render(request, 'application/account.html', {
        'form':form,
        'step':1,
        'formPageNum':formPageNum,
    })


def finances(request):
    if request.method == "POST": 
        form = EligibilityForm(request.POST)
        if form.is_valid():
            print(form.data)
            try:
                instance = form.save(commit=False)
                # NOTE FOR ANDREW: This was that stupid line that caused user auth to not work 
                instance.user_id = request.user
            #take dependent information, compare that AMI level number with the client's income selection and determine if qualified or not, flag this
                if form['grossAnnualHouseholdIncome'].value() == 'Below $19,800':
                    print("GAHI is below 19,800")
                    if qualification(form['dependents'].value(),) >= 19800:
                        instance.qualified = True
                    else:
                        instance.qualified = False
                elif form['grossAnnualHouseholdIncome'].value() == '$19,800 ~ $32,800':
                    print("GAHI is between 19,800 and 32,800")
                    if 19800 <= qualification(form['dependents'].value(),) <= 32800:
                        instance.qualified = True
                    else:
                        instance.qualified = False
                elif form['grossAnnualHouseholdIncome'].value() == 'Over $32,800':
                    print("GAHI is above 32,800")
                    if qualification(form['dependents'].value(),) >= 32800:
                        instance.qualified = True
                    else:
                        instance.qualified = False                        
                    
                print(instance.qualified)
                instance.save()
                if instance.qualified == True:
                    return redirect(reverse("application:mayQualify"))
                else:
                    return redirect(reverse("application:programs"))
            except IntegrityError:
                print("User already has information filled out for this section")
        else:
            print(form.data)
    else:
        form = EligibilityForm()
    return render(request, 'application/finances.html', {
        'form':form,
        'step':3,
        'formPageNum':formPageNum,
    })

def programs(request):
    if request.method == "POST": 
        form = programForm(request.POST)
        if form.is_valid():
            print(form.data)
            print(request.session)
            try:
                instance = form.save(commit=False)
                instance.user_id = request.user
                instance.save()
                #logic goes here, if SNAP / PSD not checked 
                    #return redirect(reverse("dashboard:manualVerifyIncome"))
                #else:
                return redirect(reverse("dashboard:files"))
            except IntegrityError:
                print("User already has information filled out for this section")
            #enter upload code here for client to upload images
            return redirect(reverse("application:available"))
    else:
        form = programForm()
    return render(request, 'application/programs.html', {
        'form':form,
        'step':4,
        'formPageNum':formPageNum,
    })

def available(request):
    return render(request, 'application/de_available.html',)

def notAvailable(request):
    return render(request, 'application/de_notavailable.html',)


def mayQualify(request):
    return render(request, 'application/mayQualify.html',)

