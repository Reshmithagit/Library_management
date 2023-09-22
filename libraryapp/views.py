from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .models import Signup,Category,Addbook,LoginRequest,Cart,Notification, SignupRequestNotification,SignupRequest,AdminNotification,OverdueBookNotification,OverdueBook
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
import random
import string
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import BookRequest,ProblemReport
from django.http import JsonResponse
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
from django.dispatch import receiver
import datetime
from decimal import Decimal
from datetime import date
from django.db import transaction
from django.utils.html import strip_tags


# Create your views here.
def index(request):
    generated_password = request.GET.get('generated_password', '')
    generated_password = generate_password()
    ca=Category.objects.all()
    show=Addbook.objects.all()
    return render(request, 'index.html', {'generated_password': generated_password, 'ca':ca,'sh':show})

    


# def adminhome(request):
      
    
      
#       notifications = SignupRequestNotification.objects.filter(is_seen=False)
#       unread_count = notifications.count()
#       return render(request, 'adminhome.html', {'unread_count': unread_count, 'notifications': notifications})

def adminhome(request):#workin
   
        # Get all unread notifications for user signups
        notifications = SignupRequestNotification.objects.filter(user__is_staff=False, is_seen=False)
        unread_count = notifications.count()
        overdue_requests = BookRequest.objects.filter(status="Overdue")
        send_overdue_notifications(overdue_requests)

       

        # Mark the notifications as seen when they are displayed
        for notification in notifications:
            notification.is_seen = True
            notification.save()

        return render(request, 'adminhome.html', {'unread_count': unread_count, 'notifications': notifications, 'overdue_requests': overdue_requests})
   
    #   else:
    #      return render(request, 'adminhome.html')  

# def adminhome(request):
#     # Get all unread notifications for user signups
#     notifications = SignupRequestNotification.objects.filter(user__is_staff=False, is_seen=False)
#     unread_count = notifications.count()
    
#     overdue_requests = BookRequest.objects.filter(status="Overdue")

#     # Iterate through overdue requests and send email notifications
#     for request in overdue_requests:
#         # Check if the notification has already been sent for this request
#         if not request.notification_sent:
#             # Send an email notification to the user
#             subject = 'Book Overdue Notification'
#             message = f'Hello {request.user.username},\n\nThe book "{request.book.book_name}" you borrowed is overdue. Please return it as soon as possible to avoid fines.\n\nThank you!'
#             from_email = 'reshmithacr31@gmail.com'  # Change to your email address
#             recipient_list = [request.user.email]

#             send_mail(subject, message, from_email, recipient_list)

#             # Mark the notification as sent
#             request.notification_sent = True
#             request.save()

#     # Mark the notifications as seen when they are displayed
#     for notification in notifications:
#         notification.is_seen = True
#         notification.save()

#     return render(request, 'adminhome.html', {'unread_count': unread_count, 'notifications': notifications, 'overdue_requests': overdue_requests})

# def adminhome(request):
#     if request.user.is_authenticated and request.user.is_staff:
#         # Get all unread notifications for user signups
#         signup_notifications = SignupRequestNotification.objects.filter(user__is_staff=False, is_seen=False)
#         signup_unread_count = signup_notifications.count()

#         # Get all overdue rentals
#         today = date.today()
#         overdue_rentals =OverdueBookNotification.objects.filter(due_date__lt=today, returned=False)

#         # Create notifications for overdue rentals
#         for rental in overdue_rentals:
#             # Check if a notification already exists for this rental and user
#             existing_notification = OverdueBookNotification.objects.filter(
#                 user=rental.user,
#                 book_title=rental.book.title,
#                 due_date=rental.due_date,
#             ).first()

#             if not existing_notification:
#                 # Create a new notification
#                 notification = OverdueBookNotification.objects.create(
#                     user=rental.user,
#                     book_title=rental.book.title,
#                     due_date=rental.due_date,
#                 )

#                 # Send an email notification here (use Django's send_mail)

#         overdue_notifications = OverdueBookNotification.objects.filter(is_seen=False)

#         # Mark the notifications as seen when they are displayed
#         for notification in signup_notifications:
#             notification.is_seen = True
#             notification.save()

#         for notification in overdue_notifications:
#             notification.is_seen = True
#             notification.save()

#             # Send an email to the user
#             subject = 'Overdue Book Notification'
#             message = f'Hello {notification.user.username},\n\n' \
#                       f'This is to remind you that the book "{notification.book_title}" ' \
#                       f'is overdue. Please return it to the library as soon as possible.\n\n' \
#                       f'Thank you!'
#             from_email = 'reshmithacr311@gmail.com'  # Replace with your email address
#             recipient_list = [notification.user.email]  # Use the user's email address

#             send_mail(subject, message, from_email, recipient_list, fail_silently=False)

#         return render(request, 'adminhome.html', {
#             'signup_unread_count': signup_unread_count,
#             'overdue_unread_count': overdue_notifications.count(),
#             'signup_notifications': signup_notifications,
#             'overdue_notifications': overdue_notifications
#         })

@login_required(login_url='index') 
def addcategory(request):
    return render(request,'addcategory.html')
@login_required(login_url='index') 
def addcat(request):
    if request.method=='POST':
        cat=request.POST['cate']
        
        catg=Category(cat_name=cat)
        catg.save()
        messages.success(request,'Category Added Successfully')
        return redirect('addcategory')
@login_required(login_url='index')     
def addbooks(request):
    books=Category.objects.all()
    return render(request,'addbooks.html',{'book':books})
@login_required(login_url='index') 
def addbo(request):
    if request.method=='POST':
        bk=request.POST['bname']
        an=request.POST['aname']
        des=request.POST['desc']
        yop=request.POST['yop']
        lan=request.POST['lan']
        qty=request.POST['qty']
        price=request.POST['price']
        img=request.FILES.get('img')
        sel=request.POST['sel']
        cat=Category.objects.get(id=sel)
        cat.save()
        Book=Addbook(book_name=bk,author_name=an,description=des,year=yop,language=lan,qty=qty,price=price,image=img,add=cat)
        Book.save()
        messages.success(request,'Book Added Successfully')
        return redirect('addbooks')
    
            

# def userdetails(request):
#     details=Signup.objects.all()
#     return render(request,'userdetails.html',{'de':details})

@login_required(login_url='index') 
def userdetails(request):
    approved_users = Signup.objects.filter(approval_status='Approved')
    return render(request, 'userdetails.html', {'approved_users': approved_users})






def generate_password(length=6):
    characters = string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


# def reg(request):
#     if request.method == 'POST':
#         fname = request.POST['fname']
#         lname = request.POST['lname']
#         uname = request.POST['uname']
#         pswd = request.POST['pass']
#         cpswd = request.POST['cpass']
#         email = request.POST['email']
#         addr = request.POST['address']
#         dob = request.POST['dob']
#         cnum = request.POST['contact']
#         img = request.FILES.get('img')
        

#         if pswd == cpswd:
#             print("Passwords match")
#             if User.objects.filter(username=uname).exists():
#                 messages.info(request, 'This username already exists!!!!!!')
#                 return redirect('index')

#             else:
#                 print("Passwords do not match")
#                 user = User.objects.create_user(
#                     first_name=fname,
#                     last_name=lname,
#                     username=uname,
#                     password=pswd, 
#                     email=email)
#                 user.save()
#                 print("User saved")
#                 u=User.objects.get(id=user.id)
#                 print("User fetched from database")
#                 reg = Signup( Address=addr, contact=cnum, dob=dob, img=img,user=u)
#                 reg.save()
#                 print("Signup data saved")

#                 subject = 'Welcome to HR Books'
#                 message = f"Thank you for signing up!\nUsername: {uname}\nPassword: {pswd}"
#                 from_email = 'reshmithacr31@gmail.com'  # Replace with your email
#                 recipient_list = [email]
#                 send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#                 messages.success(request, 'Your registration was successful. You can now log in with your username and password.')
#                 return redirect('/')

#         else:
#             messages.info(request, 'Password incorrect')
#             return redirect('/')

#     return render(request, 'index.html')


def reg(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        uname = request.POST['uname']
        pswd = request.POST['pass']
        cpswd = request.POST['cpass']
        email = request.POST['email']
        addr = request.POST['address']
        dob = request.POST['dob']
        cnum = request.POST['contact']
        img = request.FILES.get('img')

        if pswd == cpswd:
            print("Passwords match")
            if User.objects.filter(email=email).exists():
                messages.info(request, 'A user with this email already exists!')
                return redirect('/')
            if User.objects.filter(username=uname).exists():
                messages.info(request, 'This username already exists!')
                return redirect('/')
            else:
                print("Passwords do not match")
                user = User.objects.create_user(
                    first_name=fname,
                    last_name=lname,
                    username=uname,
                    password=pswd,  
                    email=email)
                user.save()
                print("User saved")
                u=User.objects.get(id=user.id)
                print("User fetched from database")
                reg = Signup( Address=addr, contact=cnum, dob=dob, img=img,user=u)
                reg.save()
                print("Signup data saved")

                subject = 'Welcome to HR Books'
                message = f"Thank you for signing up!\nUsername: {uname}\nPassword: {pswd}"
                from_email = 'reshmithacr31@gmail.com'  
                recipient_list = [email]
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                messages.success(request, 'Your registration was successful. You can now log in with your username and password.')
                signup_notification = SignupRequestNotification(user=user)
                signup_notification.save()

                # signup_notification = SignupRequestNotification(user=user)
                # signup_notification.save()
                # notifications = SignupRequestNotification.objects.filter(is_seen=False)
                # unread_count = notifications.count()
                # return render(request, 'adminhome.html', {'unread_count': unread_count, 'notifications': notifications})
                                
              
                     


                # signup_notification = SignupRequestNotification(user=user)
                # signup_notification.save()
                # user_signup_signal.send(sender=reg)
                return redirect('/')
                

        else:
            messages.info(request, 'Password incorrect')
            return redirect('/')

    return render(request, 'index.html' )

    


def adminlogin(request):
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['pass']
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('adminhome')
            else:
                try:
                    signup = Signup.objects.get(user=user)
                    if signup.approval_status == 'Approved':
                        login(request, user)
                        messages.info(request, 'User login successful.')
                        return redirect('userhome')
                    else:
                        messages.info(request, 'Your login request is not approved yet.')
                        return redirect('index')
                except Signup.DoesNotExist:
                    messages.info(request, 'Your login request is not submitted yet.')
                    return redirect('index')
        else:
            messages.info(request, 'Invalid username & password')
            return redirect('index')
    else:
        return render(request, 'index.html')


def reset_password1(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found.'})

    return JsonResponse({'success': False, 'message': 'Invalid request.'})

# def reset_password1(request):
#     return render(request,'reset_password.html')
@login_required(login_url='index') 
def userhome(request):
    ca=Category.objects.all()
    show=Addbook.objects.all()
    return render(request,'userhome.html',{'ca':ca,'sh':show})

def logout1(request):
    auth.logout(request)
    return redirect('index')

@login_required(login_url='index') 
def showbook(request):
    books=Category.objects.all()
    bk=Addbook.objects.all()
    
    return render(request,'showbook.html',{'bk':books ,'buk':bk})


@login_required(login_url='index') 
def edit_user(request):
    ca=Category.objects.all()
    user_profile = Signup.objects.get(user=request.user)
    return render(request, 'edit_user.html', {'book': user_profile,'ca':ca})

@login_required(login_url='index') 
def edit_details(request, pk):
    if request.method == 'POST':
        book = Signup.objects.get(user=pk)
        user=User.objects.get(id=pk)
        user.first_name = request.POST['fname']
        user.last_name = request.POST['lname']
        user.username = request.POST['uname']
        user.email = request.POST['email']
        book.Address=request.POST['address']
        book.dob = request.POST['dob']
        book.contact = request.POST['contact']
        if 'img' in request.FILES:
            book.img = request.FILES.get('img')
        
        book.save()  
        user.save()
        messages.success(request, 'Details updated successfully.')
        return redirect('edit_user')
    
@login_required(login_url='index') 
def view_profile(request):
     ca=Category.objects.all()
     current_user=request.user.id
     user1=Signup.objects.get(user_id=current_user)
     return render(request,'view_profile.html',{'users':user1,'ca':ca})

@login_required(login_url='index') 
def editbook(request,pk):
   books=Addbook.objects.get(id=pk)
   cat=Category.objects.all()
   return render(request,'editbook.html',{'bk':books,'ca':cat})
@login_required(login_url='index') 
def editbook_details(request,pk):
     if request.method == 'POST':
        ebook = Addbook.objects.get(id=pk)
        ebook.book_name=request.POST['bookname']
        ebook.author_name = request.POST['author']
        ebook.description = request.POST['description']
        ebook.language=request.POST['lan']
        ebook.year=request.POST['year']
        ebook.qty=request.POST['qty']
        ebook.price=request.POST['price']
        cat=request.POST['category']
        cate=Category.objects.get(id=cat)
        cate.save()
        ebook.add=cate
        if 'img' in request.FILES:

         ebook.image = request.FILES.get('img') 
        
        ebook.save() 
      
        # messages.info(request, 'Details updated successfully.') 
        
        
        return redirect('showbook')
@login_required(login_url='index') 
def delete_user(request, pk):
    user = User.objects.filter(id=pk)
    
    if user is not None:
        user.delete()
        messages.success(request, 'User deleted successfully.')
    else:
        messages.error(request, 'User not found.')
    
    return redirect('userdetails') 

# def delete_book(request,pk):
#     book=Addbook.objects.get(id=pk)
#     if book is not None:
#         book.delete()
#         messages.success(request, 'Book deleted successfully.')

def delete_book(request, pk):
    try:
        book = Addbook.objects.get(id=pk)
        book.delete()
        messages.success(request, 'Book deleted successfully.')
    except Addbook.DoesNotExist:
        messages.error(request, 'Book not found.')
    
    return redirect('showbook') 

@login_required(login_url='index') 
def categorized_products(request, category_id):
    ca=Category.objects.all()
    categories = Category.objects.filter(id=category_id)
    
    if categories.exists():
        category = categories.first()
        books = Addbook.objects.filter(add=category)
        return render(request, 'categories.html', {'categories': [category], 'book': books,'ca':ca})
    else:
        
        return render(request, 'userhome.html')



# def search_books(request):
#     search_query = request.GET.get('q')
#     if search_query:
#         search_results = Addbook.objects.filter(book_name__icontains=search_query)
#     else:
#         search_results = []

#     return render(request, 'your_template.html', {'search_results': search_results})





@login_required(login_url='index') 
def bookcard(request,pk):
    bk=Addbook.objects.get(id=pk)
    
    return render(request,'bookcard.html',{'bk':bk})



def loginusers(request):
    us=Signup.objects.all()
    return render(request,'loginusers.html',{'us':us})

# def approve_user(request, signup_id):
#     signup = Signup.objects.get(pk=signup_id)
#     signup.approve_user()
    
#     # Send a notification to the user using the messaging framework
#     messages.success(request, 'Your account has been approved by the admin. You can now log in.')
    
#     return redirect('index')

def approve_user(request, signup_id):
    signup = get_object_or_404(Signup, pk=signup_id)
    
   
    signup.approval_status = 'Approved'
    signup.save()
    
 
    messages.success(request, 'User account has been approved by the admin.')
    # messages.info(request,f'{uname} wants to  signup ')
    
    return redirect('loginusers')

# def approve_user(request, signup_id):
#     signup = get_object_or_404(Signup, pk=signup_id)

  
#     signup.approval_status = 'Approved'
#     signup.save()


#     messages.success(request, 'User account has been approved by the admin.')


#     admin_message = f"User {signup.username} has signed up and been approved."
#     admin_username = "libraryadmin"  
#     admin_user = User.objects.get(username=admin_username)
#     admin_message_notification = Notification.objects.create(
#         user=admin_user,
#         message=admin_message
#     )

#     return redirect('loginusers')

@login_required
def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'notifications.html', {'notifications': user_notifications})






# def reject_user(request, signup_id):
#     signup = Signup.objects.get(pk=signup_id)
#     user = signup.user
#     user.delete()

#     signup.reject_user()

#     messages.warning(request, 'User has been rejected.')

#     return redirect('loginusers') 

from django.contrib import messages

def reject_user(request, signup_id):
    signup = Signup.objects.get(pk=signup_id)
    user = signup.user

    # Send an email to the rejected user
    subject = 'Your Account Request has been Rejected'
    message = f"Dear {user.username},\n\nYour account request has been rejected by the admin. If you have any questions, please contact us.\n\nRegards,\nThe HR Books Team"
    from_email = 'reshmithacr31@gmail.com'  
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

    # Delete the user
    user.delete()

    signup.reject_user()

    messages.warning(request, 'User has been rejected and an email has been sent to the user.')

    return redirect('loginusers')




# @login_required(login_url='index') 
def cart(request):
    ca=Category.objects.all()
    cart_items = Cart.objects.filter(user=request.user).select_related('book')  
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cartitems': cart_items, 'totalprice': total_price,'ca':ca})
# def increase_quantity(request, pk):
#     cart_item = Cart.objects.get(book__id=pk, user=request.user)
#     cart_item.quantity += 1
#     cart_item.save()
#     return redirect('cart')

# def decrease_quantity(request, pk):
#     cart_item = Cart.objects.get(book__id=pk, user=request.user)
#     if cart_item.quantity > 1:
#         cart_item.quantity -= 1
#         cart_item.save()
#     return redirect('cart')


# @login_required(login_url='index') 
# def cart_details(request, pk):
#     product = Addbook.objects.get(id=pk)
#     cart_item, created = Cart.objects.get_or_create(user=request.user, book=product)
#     if not created:
#         cart_item.quantity += 1
#         cart_item.save()
#     messages.success(request,'Product Added to Cart')
#     return redirect('userhome')


@login_required(login_url='index') 
def cart_details(request, pk):
    product = Addbook.objects.get(id=pk)
    cart_item, created = Cart.objects.get_or_create(user=request.user, book=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

        # Decrement the quantity from inventory
        with transaction.atomic():
            product.qty -= 1  
            product.save()

    messages.success(request, 'Product Added to Cart')
    return redirect('userhome')

@login_required(login_url='index') 
def increase_quantity(request, pk):
    cart_item = Cart.objects.get(book__id=pk, user=request.user)
    cart_item.quantity += 1
    cart_item.save()

    # Decrement the quantity from inventory
    with transaction.atomic():
        cart_item.book.qty -= 1  
        cart_item.book.save()

    return redirect('cart')

@login_required(login_url='index') 
def decrease_quantity(request, pk):
    cart_item = Cart.objects.get(book__id=pk, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()

       
        with transaction.atomic():
            cart_item.book.qty += 1  
            cart_item.book.save()

    return redirect('cart')


@login_required(login_url='index') 
def removecart(request, pk):
    product = Addbook.objects.get(id=pk)
    cart_item = Cart.objects.filter(user=request.user, book=product).first()
    
    if cart_item:
        cart_item.delete()
    messages.success(request,'Product Removed!')
    return redirect('cart')

@login_required(login_url='index')  
def proceedpay(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('book')  
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'proceedpay.html', {'cartitems': cart_items, 'totalprice': total_price})
    

# def search_books1(request):
#     search_query = request.GET.get('q', '')
   
#     books = Addbook.objects.filter(Q(book_name__icontains=search_query) | Q(author_name__icontains=search_query))
 
    
#     context = {
#         'books': books,
#         'search_query': search_query
#     }

#     return render(request, 'index.html', context)

# def search_books1(request):
#     search_query = request.GET.get('q', '')
   
#     sh = Addbook.objects.filter(Q(book_name__icontains=search_query) | Q(author_name__icontains=search_query))
    
 
#     context = {
#         'sh': sh,  
#         'search_query': search_query,
   
#     }
   
#     return render(request, 'index.html', context)



def search_books_ajax(request):
    search_query = request.GET.get('q', '')

    sh = Addbook.objects.filter(Q(book_name__icontains=search_query) | Q(author_name__icontains=search_query))

    # Convert the search results to a JSON format
    results = [{'book_name': book.book_name, 'author_name': book.author_name} for book in sh]

    return JsonResponse({'results': results})




@login_required(login_url='index') 


# def request_issue(request, pk):
#     try:
#         if request.method == 'POST':
#             book_id = request.POST.get('book_id')  # Use get() to avoid raising KeyError
#             book = Addbook.objects.get(pk=book_id)

#             # Check if the book is in stock
#             if book.qty <= 0:
#                 messages.error(request, 'This book is out of stock and cannot be requested for issue.')
#             else:
#                 # Create a book request with "Pending" status
#                 BookRequest.objects.create(user=request.user, book=book, status="Pending")
#                 messages.success(request, 'Book request sent successfully!')
#         else:
#             messages.error(request, 'Invalid request method.')
#     except Addbook.DoesNotExist:
#         messages.error(request, 'The requested book does not exist.')
#     except Exception as e:
#         print(f"Error: {e}")
#         messages.error(request, 'An error occurred while sending the book request.')

#     return redirect('userhome')
def request_issue(request, pk):
    try:
        if request.method == 'POST':
            book_id = request.POST.get('book_id')
            rental_period = request.POST.get('rental_period')

            try:
                rental_period = int(rental_period)
            except ValueError:
                rental_period = 7

            try:
                book = Addbook.objects.get(pk=book_id)

                if book.qty <= 0:
                    messages.error(request, 'This book is out of stock and cannot be requested for issue.')
                else:
                    # Debugging: Print values to check if they are set correctly
                    print(f"book_id: {book_id}, rental_period: {rental_period}")

                    # Calculate the due date based on the rental period
                    due_date = timezone.now() + timedelta(days=rental_period)

                    # Debugging: Print the calculated due date
                    print(f"Calculated due_date: {due_date}")

                    # Create a book request with "Pending" status and due date
                    BookRequest.objects.create(user=request.user, book=book, status="Pending", rental_period=rental_period, due_date=due_date)
                    messages.success(request, 'Book request sent successfully!')
            except Addbook.DoesNotExist:
                messages.error(request, 'The requested book does not exist.')
            except Exception as e:
                print(f"Error: {e}")
                messages.error(request, 'An error occurred while sending the book request.')

    except Exception as e:
        # Handle any other exceptions that might occur
        print(f"Error: {e}")
        messages.error(request, 'An error occurred while processing the request.')

    return redirect('userhome')


@login_required(login_url='index') 
def show_requestedbook(request):
    user = request.user
    ca=Category.objects.all()
    requested_books = BookRequest.objects.filter(user=user)
    context = {
        'requested_books': requested_books,
        'ca':ca
    }
    return render(request, 'show_requestedbook.html', context)

# def show_requestedbook(request):
#     ca = Category.objects.all()
#     user = request.user
#     requested_books = BookRequest.objects.filter(user=user, issued=False, status__in=['Pending', 'Approved'])
#     context = {
#         'requested_books': requested_books,
#         'ca': ca
#     }
#     return render(request, 'show_requestedbook.html', context)


@login_required(login_url='index') 
# def show_issuedbook(request):
#     user = request.user
#     ca=Category.objects.all()
#     issued_books = BookRequest.objects.filter(user=user, issued=True)  # Retrieve issued books for the logged-in user
#     for issued_book in issued_books:
#         # Calculate due date by adding 14 days to the request date
#         issued_book.due_date = issued_book.request_date + timedelta(days=14)
#     context = {
#         'issued_books': issued_books,
#         'ca':ca
#     }
#     return render(request, 'show_issuedbook.html', context)

def show_issuedbook(request):
    user = request.user
    ca = Category.objects.all()
    issued_books = BookRequest.objects.filter(user=user, issued=True).exclude(returned=True)

    for issued_book in issued_books:
        # Calculate due date based on the rental period
        due_date = issued_book.request_date + timedelta(days=issued_book.rental_period)
        issued_book.due_date = due_date

    context = {
        'issued_books': issued_books,
        'ca': ca
    }

    return render(request, 'show_issuedbook.html', context)

@login_required(login_url='index') 
def requestedbook(request):
    requested_books = BookRequest.objects.all()
    return render(request, 'requestedbook.html', {'requested_books': requested_books})

# @login_required(login_url='index') 
# def issue_book_request(request, request_id):
#     book_request = get_object_or_404(BookRequest, id=request_id)
    
#     print(f"Book request status: {book_request.status}")
#     print(f"Is Issued: {book_request.issued}")
#     print(f"Book quantity: {book_request.book.qty}")

#     if book_request.status == "Approved" and not book_request.issued:
#         try:
#             book_request.issued = True
#             book_request.save()
            
#             book_request.book.qty -= 1
#             book_request.book.save()

#             messages.success(request, 'Book issued successfully!')
#         except Exception as e:
#             messages.error(request, 'An error occurred while issuing the book.')
#             print(f"Error: {e}")
#     else:
#         messages.error(request, 'Book request cannot be issued.')
    
#     print(f"Issued status after update: {book_request.issued}")
#     print(f"Book quantity after update: {book_request.book.qty}")

#     return redirect('requestedbook')

@login_required(login_url='index') 
def issue_book_request(request, request_id):
    book_request = get_object_or_404(BookRequest, id=request_id)
    
    print(f"Book request status: {book_request.status}")
    print(f"Is Issued: {book_request.issued}")
    print(f"Book quantity: {book_request.book.qty}")

    if book_request.status == "Approved" and not book_request.issued:
        try:
            book_request.issued = True
            book_request.save()
            
            book_request.book.qty -= 1
            book_request.book.save()

            messages.success(request, 'Book issued successfully!')
        except Exception as e:
            messages.error(request, 'An error occurred while issuing the book.')
            print(f"Error: {e}")
    else:
        messages.error(request, 'Book request cannot be issued.')
    
    print(f"Issued status after update: {book_request.issued}")
    print(f"Book quantity after update: {book_request.book.qty}")

    return redirect('requestedbook')




@login_required(login_url='index') 
def issued_books(request):
    issued_books = BookRequest.objects.filter(status="Approved", issued_books__gt=0)
    return render(request, 'issued_books.html', {'issued_books': issued_books})

@login_required(login_url='index') 
# def approve_book_request(request, request_id):
#     book_request = get_object_or_404(BookRequest, id=request_id)
#     if book_request.status == "Pending":
#         book_request.status = "Approved"
#         book_request.save()
#         messages.success(request, 'Book request approved successfully!')
#     else:
#         messages.error(request, 'Book request cannot be approved.')

#     return redirect('requestedbook')


def approve_book_request(request, request_id):
    book_request = get_object_or_404(BookRequest, id=request_id)
    if book_request.status == "Pending":
        book_request.status = "Approved"
        book_request.save()
        messages.success(request, 'Book request approved successfully!')
    else:
        messages.error(request, 'Book request cannot be approved because it is not pending.')

    return redirect('requestedbook')



@login_required(login_url='index') 

# def show_returnedbook(request): #1st workin
#     returned_books = BookRequest.objects.filter(issued=False)
#     for returned_book in returned_books:
#         returned_book.due_date = returned_book.request_date + timedelta(days=14)
#     context = {'returned_books': returned_books}
#     return render(request, 'show_returnedbook.html', context)

# def show_returnedbook(request):#2nd workin
#     user = request.user 
#     ca = Category.objects.all() 
#     returned_books = BookRequest.objects.filter(issued=False)

#     for returned_book in returned_books:
#         # Calculate due date based on the rental period
#         due_date = returned_book.request_date + timedelta(days=returned_book.rental_period)
#         returned_book.due_date = due_date

#     context = {
#         'returned_books': returned_books,
#         'ca': ca  
#     }

#     return render(request, 'show_returnedbook.html', context)



# def show_returnedbook(request):#current
#     user = request.user 
#     ca = Category.objects.all()  
#     returned_books = BookRequest.objects.filter(issued=False)

#     for returned_book in returned_books:
#         # Calculate due date based on the rental period
#         due_date = returned_book.request_date + timedelta(days=returned_book.rental_period)
#         returned_book.due_date = due_date

#     issue_reports = ProblemReport.objects.filter(issued_book__in=returned_books)

#     context = {
#         'returned_books': returned_books,
#         'ca': ca,  
#         'issue_reports': issue_reports  
#     }

#     return render(request, 'show_returnedbook.html', context)


def show_returnedbook(request):
    user = request.user 
    ca = Category.objects.all()  

    # Filter returned books
    returned_books = BookRequest.objects.filter(returned=True)

    for returned_book in returned_books:
        # Calculate due date based on the rental period
        due_date = returned_book.request_date + timedelta(days=returned_book.rental_period)
        returned_book.due_date = due_date
        overdue_days = (timezone.now().date() - due_date).days
        returned_book.overdue_days = overdue_days  

    issue_reports = ProblemReport.objects.filter(issued_book__in=returned_books)

    context = {
        'returned_books': returned_books,
        'ca': ca,  
        'issue_reports': issue_reports  
    }
    
    return render(request, 'show_returnedbook.html', context)



# def show_returnedbook(request):#return date calculate
#     user = request.user 
#     ca = Category.objects.all()  
#     returned_books = BookRequest.objects.filter(returned=True)
#     for returned_book in returned_books:
#     # Calculate due date based on the rental period
#         due_date = returned_book.request_date + timedelta(days=returned_book.rental_period)
#         returned_book.due_date = due_date
        
#     # Check if return_date is not None
#     if returned_book.return_date:
#         # Calculate overdue_days as return_date - due_date
#         overdue_days = (returned_book.return_date.date() - due_date.date()).days
#         returned_book.overdue_days = overdue_days
#     else:
#         # Handle the case where return_date is None (book not yet returned)
#         returned_book.overdue_days = None  # or any appropriate value

# # The rest of your code remains the same

# # The rest of your code remains the same

#     issue_reports = ProblemReport.objects.filter(issued_book__in=returned_books)

#     context = {
#         'returned_books': returned_books,
#         'ca': ca,  
#         'issue_reports': issue_reports  
#     }
    
#     return render(request, 'show_returnedbook.html', context)


# @login_required(login_url='index') 
# def finepayment(request, book_request_id):
#     book_request = get_object_or_404(BookRequest, id=book_request_id)

#     if request.method == 'POST':
#         penalty = request.POST.get('penalty')
#         status = request.POST.get('status')

#         book_request.penalty = penalty
#         book_request.status = status
#         book_request.save()

#         # Redirect back to the same page or a relevant page
#         return redirect('show_returnedbook')  

#     return render(request, 'userhome.html', {'book_request': book_request})

@login_required(login_url='index') 
def user_penalty_details(request):
    ca=Category.objects.all()
    user = request.user
    books_with_penalty = BookRequest.objects.filter(user=user, penalty__gt=0)
    
    context = {
        'books_with_penalty': books_with_penalty,
        'ca':ca
    }
    
    return render(request, 'user_penalty_details.html', context)






# @login_required(login_url='index') 
# def return_book(request, issued_book_id):#workin
#     issued_book = get_object_or_404(BookRequest, id=issued_book_id)
#     if issued_book.issued and request.method == 'POST':
#         print('book issued')
#         penalty = request.POST.get('penalty')
#         status = request.POST.get('status')

#         issued_book.penalty = penalty
#         issued_book.status = status

#         issued_book.issued = False
#         issued_book.return_date = timezone.now()
#         issued_book.save()

#         returned_book = issued_book.book
#         returned_book.qty += 1
#         returned_book.save()

#         messages.success(request, 'The book has been successfully returned. Penalty Amount: {} Reason: {}'.format(penalty, status))

#         return redirect('show_issuedbook')

#     return render(request, 'userhome.html')

def return_book(request, issued_book_id):
    issued_book = get_object_or_404(BookRequest, id=issued_book_id)

    if issued_book.issued and request.method == 'POST':
        penalty = request.POST.get('penalty')
        status = request.POST.get('status')

        # Update penalty and status
        issued_book.penalty = penalty
        issued_book.status = status

        # Calculate the return date
        issued_book.return_date = timezone.now()

        # Set the book as returned
        issued_book.returned = True

        # Save the changes
        issued_book.save()

        # Increase the quantity of the returned book
        returned_book = issued_book.book
        returned_book.qty += 1
        returned_book.save()

        messages.success(request, 'The book has been successfully returned. Penalty Amount: {} Reason: {}'.format(penalty, status))
        
        return redirect('show_issuedbook')

    return render(request, 'userhome.html')


# def return_book(request, issued_book_id):
#     issued_book = get_object_or_404(BookRequest, id=issued_book_id)
#     if issued_book.issued and request.method == 'POST':
#         print('book issued')
#         penalty = request.POST.get('penalty')
#         status = request.POST.get('status')

#         issued_book.penalty = penalty
#         issued_book.status = status

#         issued_book.issued = False
#         issued_book.return_date = timezone.now()
#         issued_book.save()

#         returned_book = issued_book.book
#         returned_book.qty += 1
#         returned_book.save()

#         messages.success(request, 'The book has been successfully returned. Penalty Amount: {} Reason: {}'.format(penalty, status))

#         return redirect('show_issuedbook')

#     return render(request, 'userhome.html')

# def return_book(request, issued_book_id):
#     issued_book = get_object_or_404(BookRequest, id=issued_book_id)
#     if issued_book.issued and request.method == 'POST':
#         print('book issued')
#         penalty = request.POST.get('penalty')
#         status = request.POST.get('status')

#         issued_book.penalty = penalty
#         issued_book.status = status

#         issued_book.issued = False
#         issued_book.return_date = timezone.now()
#         issued_book.save()

#         returned_book = issued_book.book
#         returned_book.qty += 1
#         returned_book.save()

#         messages.success(request, 'The book has been successfully returned. Penalty Amount: {} Reason: {}'.format(penalty, status))

#         return redirect('show_issuedbook')

#     return render(request, 'userhome.html')


# def return_book(request, issued_book_id):
#     issued_book = get_object_or_404(BookRequest, id=issued_book_id)
    
#     if issued_book.issued and request.method == 'POST':
#         # Calculate overdue_days
#         due_date = issued_book.due_date  # Replace with the actual due date field name
#         return_date = timezone.now()
#         overdue_days = (return_date - due_date).days
        
#         penalty_rate = 1  # Replace with your actual penalty rate per day
        
#         # Calculate penalty based on overdue days and penalty rate
#         penalty = overdue_days * penalty_rate
        
#         status = request.POST.get('status')

#         issued_book.penalty = penalty
#         issued_book.status = status

#         issued_book.issued = False
#         issued_book.return_date = return_date
#         issued_book.save()

#         returned_book = issued_book.book
#         returned_book.qty += 1
#         returned_book.save()

#         messages.success(request, f'The book has been successfully returned. Penalty Amount: {} Reason: {}')

#         return redirect('show_issuedbook')

#     return render(request, 'userhome.html')





@login_required(login_url='index') 
def confirm_order(request):
    if request.method == 'POST':
        user = request.user

        # Send email
        subject = 'Order Confirmation'
        message = 'Your order has been confirmed. Thank you for your purchase!'
        from_email = 'reshmithacr31@gmail.com'
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        print(f"Email sent to {recipient_list}")

       

        messages.success(request, 'Order placed successfully')

        return redirect( 'userhome')

    return render(request, 'cart.html')


def about(request):
    return render(request,'about.html')








def penaltypayment(request):
    ca=Category.objects.all()
    return render(request,'penaltypayment.html',{'ca':ca})



# def report_problem(request, issued_book_id):
#     try:
#         issued_book = BookRequest.objects.get(id=issued_book_id)
#     except BookRequest.DoesNotExist:
#         messages.error(request, 'Issued book not found.')
#         return redirect('your_rented_books_page')  # Replace with the URL name for the rented books page

#     # Get problem type and description from the form submission
#     problem_type = request.POST.get('problem_type')
#     problem_description = request.POST.get('problem_description')

#     # Calculate fine amount based on problem type and additional charges (if any)
#     fine_amount = calculate_fine(issued_book, problem_type)

#     # Create a problem report entry
#     problem_report = ProblemReport(
#         user=request.user,
#         issued_book=issued_book,
#         problem_type=problem_type,
#         problem_description=problem_description,
#         fine_amount=fine_amount
#     )
#     problem_report.save()


#     return redirect('show_issuedbook')
def report_problem(request, issued_book_id):
    try:
        issued_book = BookRequest.objects.get(id=issued_book_id)
    except BookRequest.DoesNotExist:
        messages.error(request, 'Issued book not found.')
        return redirect('show_issuedbook')  

    if request.method == 'POST':
        # Get problem type and description from the form submission
        problem_type = request.POST.get('problem_type')
        problem_description = request.POST.get('problem_description')

        # Calculate fine amount based on problem type and additional charges 
        fine_amount = calculate_fine(issued_book, problem_type)

        # Create a problem report entry
        problem_report = ProblemReport(
            user=request.user,
            issued_book=issued_book,  
            problem_type=problem_type,
            problem_description=problem_description,
            fine_amount=fine_amount
        )
        problem_report.save()
        messages.success(request, 'Problem reported successfully.')

    return redirect('show_issuedbook')


# def calculate_fine(issued_book, problem_type):
#     if problem_type == 'lost':
#         # Calculate the fine for a lost book as the book's original price plus any additional charges
#         fine_amount = issued_book.book.price + issued_book.additional_charges
#     else:
       
        
#         # For other problem types (damage, overdue), use the predefined rates
#         fine_rates = {
#             'damage': 20,    # Fine amount for a damaged book
#             'overdue': 10,   # Fine amount for overdue return
            
            
#         }
#         fine_rate = fine_rates.get(problem_type, 0)  
#         fine_amount = issued_book.book.price + fine_rate
    
#     return fine_amount



# def calculate_fine(issued_book, problem_type):
#     if problem_type == 'lost':
#         # Calculate the fine amount for a lost book (e.g., original price + additional charges)
#         original_price = issued_book.book.price
#         additional_charges = Decimal('10.00')  # You can customize this value
#         fine_amount = original_price + additional_charges
#     elif problem_type == 'damage':
#         # Calculate the fine amount for a damaged book (e.g., based on the extent of damage)
#         damage_charge_per_page = Decimal('2.00')  # You can customize this value
#         damaged_pages = 10  # You can get this information from the user or other sources
#         fine_amount = damage_charge_per_page * damaged_pages
#     else:
#         # Handle other issue types if needed
#         fine_amount = Decimal('0.00')  # Default to no fine

#     return fine_amount



def calculate_fine(issued_book, problem_type):
    if problem_type == 'lost':
        # Calculate the fine amount for a lost book 
        original_price = issued_book.book.price
        additional_charges = Decimal('10.00')  
        fine_amount = original_price + additional_charges
    elif problem_type == 'damage':
        # Calculate the fine amount for a damaged book (
        damage_charge_per_page = Decimal('2.00')  
        damaged_pages = 10  
        fine_amount = damage_charge_per_page * damaged_pages
    elif problem_type == 'overdue':
        due_date = issued_book.due_date  # Remove .date()
        today = date.today()  # Get the current date without time
        if today >= due_date:
            # Calculate fine based on the number of days overdue
            days_overdue = (today - due_date).days
            overdue_charge_per_day = Decimal('10.00')  
            fine_amount = days_overdue * overdue_charge_per_day
        else:
            fine_amount = Decimal('0.00')

    return fine_amount

def problem_history(request):
    # Retrieve the user's problem reports from the database
    problem_reports = ProblemReport.objects.filter(user=request.user)

    return render(request, 'problem_history.html', {'problem_reports': problem_reports})




def mark_issue_as_paid(request, issue_id):
    try:
        issue_report = ProblemReport.objects.get(id=issue_id)
        # Mark the issue as paid in the database
        issue_report.is_paid = True
        issue_report.save()
        return JsonResponse({'status': 'success'})
    except ProblemReport.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Issue report not found'})



# def check_overdue_books(request):
#     # Get the current date and time
#     current_datetime = timezone.now()

#     # Identify overdue books
#     overdue_books = ProblemReport.objects.filter(due_date__lt=current_datetime)

#     notifications = []

#     for book_request in overdue_books:
#         # Calculate fine amount 
#         fine_amount = calculate_fine1(book_request.due_date, current_datetime)

#         # Create a ProblemReport instance for the overdue book
#         overdue = BookRequest(
#             user=book_request.user,
#             issued_book=book_request,
#             problem_type='Overdue',
#             problem_description='The book is overdue',
#             fine_amount=fine_amount
#         )
#         overdue.save()

#         # Create a notification message with username and book name
#         notification_message = f"{book_request.user.username} and {book_request.book.book_name}, book is overdue, please return it on time to avoid a penalty"
#         notifications.append(notification_message)

  

#     return render(request, 'adminhome.html', {'overdue_books': overdue_books, 'notifications': notifications})
# def check_overdue_books(request):#workin
#     # Get the current date and time
#     current_datetime = timezone.now()

#     # Identify overdue books
#     overdue_books = ProblemReport.objects.filter(due_date__lt=current_datetime)

#     notifications = []

#     for book_request in overdue_books:
#         # Check if the book is already marked as 'Overdue'
#         if book_request.status != 'Overdue':
#             # Calculate fine amount 
#             fine_amount = calculate_fine(book_request, 'overdue')

#             # Update the status and fine amount for the book request
#             book_request.status = 'Overdue'
#             book_request.fine_amount = fine_amount
#             book_request.save()

#             # Create a notification message with username and book name
#             notification_message = f"{book_request.user.username} and {book_request.book.book_name}, book is overdue, please return it on time to avoid a penalty"
#             notifications.append(notification_message)

#     return render(request, 'adminhome.html', {'overdue_books': overdue_books, 'notifications': notifications})


# def calculate_fine1(due_date, current_date):
#     # Convert date strings to date objects if needed
#     due_date = date.fromisoformat(due_date)
#     current_date = date.fromisoformat(current_date)

#     # Calculate the number of days overdue
#     days_overdue = (current_date - due_date).days

#     # Check if the book is overdue
#     if days_overdue > 0:
#         overdue_charge_per_day = Decimal('10.00')  
#         fine_amount = days_overdue * overdue_charge_per_day
#         return fine_amount
#     else:
#         return Decimal('0.00')
    





def check_overdue_books(request):
    # Get the current date and time
    current_datetime = timezone.now()

    # Identify overdue books
    overdue_books = BookRequest.objects.filter(due_date__lt=date.today(), returned=False)

    notifications = []

    for book_request in overdue_books:
      
        if book_request.status != 'Overdue':
            # Calculate fine amount
            fine_amount = calculate_fine(book_request, 'overdue')

            # Update the status and fine amount for the book request
            book_request.status = 'Overdue'
            book_request.fine_amount = fine_amount
            book_request.save()

            # Create a notification message with username and book name
            notification_message = f"{book_request.user.username} and {book_request.book.book_name}, book is overdue, please return it on time to avoid a penalty"
            notifications.append(notification_message)
            subject = 'Book Overdue Notification'
            message = f'Hello,\n\nThe book "{book_request.book.book_name}" you borrowed is overdue. Please return it as soon as possible to avoid fines.\n\nThank you!'
            from_email = 'reshmitha31@gmail.com'
            recipient_list = [book_request.user.email]

            send_mail(subject, message, from_email, recipient_list)

            return render(request, 'adminhome.html', {'overdue_books': overdue_books, 'notifications': notifications})




# def send_overdue_notifications(overdue_requests):
#     """
#     Send overdue book notifications to users.
#     """
#     for request in overdue_requests:
      
#         if not request.user.email:
#             continue

#         subject = "Overdue Book Notification"
#         message = f"Dear {request.user.username},\n\nYour book request for '{request.book.book_name}' is overdue. Please return it as soon as possible to avoid penalties."
#         from_email = "reshmithacr31@gmail.com"  
#         recipient_list = [request.user.email]

#         send_mail(subject, message, from_email, recipient_list)




def send_overdue_notifications(request):
    """
    Send overdue book notifications to users and mark requests as notified.
    """
    # Filter overdue requests that haven't been notified
    overdue_requests = BookRequest.objects.filter(status="Overdue", notification_sent=False)

    for request in overdue_requests:
        if not request.user.email:
            continue

        # Compose the notification email
        subject = "Overdue Book Notification"
        message = f"Dear {request.user.username},\n\nYour book request for '{request.book.book_name}' is overdue. Please return it as soon as possible to avoid penalties."
        from_email = "reshmithacr31@gmail.com"
        recipient_list = [request.user.email]

        # Send the notification email
        send_mail(subject, message, from_email, recipient_list)

        # Mark the request as notified
        request.notified = True
        request.save()

    # You can return a response or perform additional actions as needed
    # For example, you can redirect to a page or return a JSON response
    # to indicate the success of sending notifications.
