from .models import Signup

def counter(request):
    count = 0
    user = request.user  # Assuming you want to access the current user

    # Count the number of objects that meet your criteria
    var = Signup.objects.filter(role='user', status=0)
    count = var.count()

    # You can also count var1 if it's defined and meets certain criteria
    # var1 = YourModel.objects.filter(...)  # Replace YourModel and filter criteria
    # count += var1.count()

    return {'count': count}



# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BookRequest, OverdueBook
from decimal import Decimal
from django.utils import timezone

@receiver(post_save, sender=BookRequest)
def calculate_overdue_books(sender, instance, **kwargs):
    if instance.status == 'Approved' and not instance.issued:
        due_date = instance.due_date
        today = timezone.now().date()

        if today > due_date:
            days_overdue = (today - due_date).days
            overdue_charge_per_day = Decimal('10.00')  # Adjust the fine amount per day as needed
            fine_amount = days_overdue * overdue_charge_per_day
            instance.status = "Overdue"
            instance.overdue = "Overdue"
            instance.fine_amount = fine_amount
            instance.save()

            # Create an OverdueBook instance
            OverdueBook.objects.create(
                user=instance.user,
                book_request=instance,
                due_date=instance.due_date,
                days_overdue=days_overdue,
                fine_amount=fine_amount
            )
