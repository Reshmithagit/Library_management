from django.db import models
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal
from datetime import date
# Create your models here.

class Signup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    Address = models.CharField(max_length=255)
    contact = models.CharField(max_length=10)
    dob = models.DateField()
    img = models.ImageField(upload_to='images/')


    STATUS_CHOICES = (
        ('Pending Approval', 'Pending Approval'),
        ('Approved', 'Approved'),
    )
    approval_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending Approval')
    
    def save(self, *args, **kwargs):
        if self.pk is None:  
            self.approval_status = 'Pending Approval'
        super(Signup, self).save(*args, **kwargs)
    
    def approve_user(self):
        self.approval_status = 'Approved'
        self.save()
    def reject_user(self):
        self.approved = False
        self.save()

    def reject_user(self):
        self.delete()  
     
class LoginRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False) 

    def __str__(self):
        return f"Login request for {self.user}"



class Category(models.Model):
    cat_name=models.CharField(max_length=255)
   
class Addbook(models.Model):
    add=models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    book_name=models.CharField(max_length=255)
    author_name=models.CharField(max_length=255)
    description=models.CharField(max_length=255) 
    year=models.IntegerField(null=True)
    qty=models.IntegerField(null=True)
    price=models.IntegerField(null=True)
    image=models.ImageField(upload_to="images/",null=True)
    LANGUAGE_CHOICES = (
        ('Malayalam', 'Malayalam'),
        ('English', 'English'),
        ('Other', 'Other'),
    )
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='Malayalam')


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    book = models.ForeignKey(Addbook, on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
            return self.quantity * self.book.price 
   

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)



class SignupRequest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class SignupRequestNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='signup_notifications')
    is_seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class BookRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Addbook, on_delete=models.CASCADE)
    request_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")],default='Pending')
    issued = models.BooleanField(default=False)
    penalty = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    rental_period = models.PositiveIntegerField() 
    due_date = models.DateField()  # Automatically calculated due date
    overdue = models.CharField(max_length=20)  
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    returned = models.BooleanField(default=False) 
    return_date = models.DateTimeField(null=True, blank=True)
    notification_sent = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        if not self.request_date:
            self.request_date = timezone.now().date()

        if not self.rental_period:
            self.rental_period = 1  # Use a default value if rental_period is not set

        # Calculate due date based on request date and rental period
        self.due_date = self.request_date + timezone.timedelta(days=self.rental_period)

        # Extract the date part of the due date and current date
        due_date = self.due_date
        today = timezone.now().date()  # Get the current date without time

        if today >= due_date:
            # Calculate fine based on the number of days overdue
            days_overdue = (today - due_date).days
            overdue_charge_per_day = Decimal('10.00')  # Adjust the fine amount per day as needed
            fine_amount = days_overdue * overdue_charge_per_day
            self.status = "Overdue"
            self.overdue = "Overdue"

            # Create an OverdueBook instance
            OverdueBook.objects.create(
                user=self.user,
                book_request=self,
                due_date=self.due_date,
                days_overdue=days_overdue,
                fine_amount=fine_amount
            ) 
        else:
            fine_amount = Decimal('0.00')
            self.status = "Approved"  # Change the status to "Approved" when not overdue
            self.overdue = "Not Overdue"  # Set 'overdue' to "Not Overdue" when not overdue

        self.fine_amount = fine_amount 

        super(BookRequest, self).save(*args, **kwargs)
    
    
class ProblemReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issued_book = models.ForeignKey(BookRequest, on_delete=models.CASCADE)
    problem_type = models.CharField(max_length=20)
    problem_description = models.TextField()
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.user.username} - {self.problem_type}"
    


class AdminNotification(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


class OverdueBookNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    book_title = models.CharField(max_length=255)  
    due_date = models.DateField() 
    is_seen = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.user.username}'s overdue book notification"



class OverdueBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_request = models.ForeignKey(BookRequest, on_delete=models.CASCADE)
    due_date = models.DateField()
    days_overdue = models.PositiveIntegerField()
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Overdue Book: {self.book_request.book.book_name} - Due Date: {self.due_date}"