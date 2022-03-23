from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, UserForm, UserProfileForm

from .models import Account, UserProfile
from orders.models import Order, OrderProduct
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from carts.views import _cart_id
from carts.models import Cart, CartItem
import requests

# Create your views here.
    #if the request contain all the field values 
def register(request):
    if request.method == 'POST':
         form = RegistrationForm(request.POST)
         if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            
            #create user profile 
            #the user.id is generated when we register the user 
            profile = UserProfile()
            profile.user_id = user.id
            profile.save()
            #the user profile created but its empty we have just the user  
            # user avtivation
            current_site= get_current_site(request)
            mail_subject= 'please activate your account'
            message= render_to_string('accounts/account_verification_email.html',{
               'user':user,
               'domain':current_site,
               'uid':urlsafe_base64_encode(force_bytes(user.pk)),#encoding the user primary key
               'token':default_token_generator.make_token(user),#token generator is the library it has the make token and check token functions we'ere pass the user itself inside this make token function to create a token for this particular user
                })#we write here the email content 
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
           # messages.success(request,'Thank you for registration with us ,we have sent you a verification email to your address .please verify it')
            return redirect('/accounts/login/?command=verification&email='+email)
            

    else:
        form= RegistrationForm()
  
    context={'form':form,}
    return render(request,'accounts/register.html',context)

def login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        
        user=auth.authenticate(email=email,password=password)
        if user is not None:
            try:
                #before i login i'm gonna check if there is cart_item 
                cart= Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists :
                    #all the cart items inside the cart_id
                    cart_item=CartItem.objects.filter(cart=cart)
                    #getting the product variation by cart_id
                    product_variation = []
                    for item in cart_item:
                        #take all the variations inside the cart
                        variation=item.variations.all()
                        product_variation.append(list(variation))
                        
                        #get the cart items from the user to access his product variations
                        
                        
                        cart_item = CartItem.objects.filter( user=user)
                        ex_var_list = []
                        id = []
                        for item in cart_item:
                         existing_variation = item.variations.all()
                         ex_var_list.append(list(existing_variation))
                         id.append(item.id)
                         
                         #product_variation=[1,2,3,4,6]
                         #ex_var_list=[4,6,5]
                         #we check if there is something exist from product_variation in ex_var_list
                         for pr in product_variation:
                            if pr in ex_var_list:
                                 # index give us the possetion where is the common item 
                                 index= ex_var_list.index(pr)
                                 item_id= id[index]
                                 item= CartItem.objects.get(id=item_id)
                                 item.quantity+=1
                                 #assign the user to the item
                                 item.user=user
                                 item.save()
                            else:
                                cart_item= CartItem.objects.filter(cart=cart)
                                
                    # assigning the user into the cart_item
                                for item in cart_item:
                                  item.user= user
                                  item.save()

            except:
                pass
            auth.login(request,user)
            messages.success(request,'you are now logged in')
            url = request.META.get('HTTP_REFERER')#http referer grap the previous url from where i came
            try:
                query=requests.utils.urlparse(url).query
                #next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)#if i want to do checkout and i wasnt login //after i logedin it takes me to the page after checkout page
            except:
                return redirect('dashboard')

        else :
            messages.error(request,'invalid login credentials')
            return redirect('login')

    return render(request,'accounts/login.html')


#chick if we  first log in 
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request,'you are logged out')
    return redirect('login')




def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()#give us primary key of the user 
        user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):#we want to take the user from the token 
        user.is_active=True
        user.save()
        messages.success(request,'Congragulation your account is activated')
        return redirect('login')
    else:
        messages.error(request,'invalid activation link')
        return redirect('register`')
  
  
@login_required(login_url='login')
def dashboard(request):
   orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
   orders_count = orders.count()

  # userprofile = UserProfile.objects.get(user_id=request.user.id)
   context = {
        'orders_count': orders_count,
       # 'userprofile': userprofile,
    }
   return render(request, 'accounts/dashboard.html', context)



def forgotpassword(request):
    if request.method== 'POST':
        email=request.POST['email']
        if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email__exact=email)
            #reset password email
            current_site= get_current_site(request)
            mail_subject= 'Reset your password'
            message= render_to_string('accounts/reset_password_email.html',{
               'user':user,
               'domain':current_site,
               'uid':urlsafe_base64_encode(force_bytes(user.pk)),#encoding the user primary key
               'token':default_token_generator.make_token(user),#token generator is the library it has the make token and check token functions we'ere pass the user itself inside this make token function to create a token for this particular user
                })#we write here the email content 
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'password reaet email has been sent to your email address')
            return redirect('login')
        else:
            messages.error(request,'Account doesnt exist')
            return redirect('forgotpassword')
    return render(request,'accounts/forgotpassword.html')


def resetpassword_validate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()#give us primary key of the user 
        user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):#we want to take the user from the token 
       #save the uid inside the session , i need this uid to reset password
       request.session['uid']=uid
       messages.success(request,'please reset your password')
       return redirect('resetPassword')
    else:
        messages.error(request,'this link has been expired')
        return redirect('login')
    
    
    
def resetPassword(request):
    if request.method=='POST':
        password= request.POST['password']
        confirm_password= request.POST['confirm_password']
        
        if password== confirm_password:
            uid=request.session.get('uid')# i have the uid inside the session when i get the uid i get the user 
            user = Account.objects.get(pk=uid)
            user.set_password(password)#set_password well hash the password 
            user.save()
            messages.success(request,'password reset successful')
            return redirect('login')

        else:
            messages.error(request,'password do not match')
            return redirect('resetPassword')
    else:  
      return render(request,'accounts/resetPassword.html')
    
    
    
    
    
@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'accounts/my_orders.html', context)



@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)#we pass instance because we want to update the user profile not to create new one 
        profile_form = UserProfileForm(request.POST, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/edit_profile.html', context)





@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        #request.post[''] we take this information from the template that the user write
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)# user.username we have this inside the account model/ixact is case sensitive 

        if new_password == confirm_password:
            success = user.check_password(current_password)#check the old password if its right 
            if success:
                user.set_password(new_password)#set_password its builled in function it takes the password and hash it 
                user.save()
                # auth.logout(request)
                messages.success(request, 'Password updated successfully.')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('change_password')
    return render(request, 'accounts/change_password.html')



@login_required(login_url='login')
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)#order__order_number this from app orders model orderproduct insdie it we have order and its foreignkey with order model inside order model we have order_number
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'accounts/order_detail.html', context)

