from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=12)  
    description = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.email})"  
    

class Trainer(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=25, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15)  
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    experience = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.experience} years of experience"
    

class Membership_Plan(models.Model):
    plan = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.plan} - ₹{self.price}"

class Enrollment(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Overdue', 'Overdue'),
    ]

    fullname = models.CharField(max_length=100)
    email = models.EmailField()
    gender = models.CharField(max_length=25, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=15)
    dob = models.DateField()
    select_membership = models.ForeignKey(Membership_Plan, on_delete=models.CASCADE)
    select_trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    reference = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField()
    emergency_contact = models.CharField(max_length=15)
    date_of_joining = models.DateField(auto_now_add=True, null=False, blank=False)
    payment_status = models.CharField(max_length=100, choices=PAYMENT_STATUS_CHOICES, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.fullname} - {self.email}"

    def save(self, *args, **kwargs):
        # Automatically set the price from the membership plan
        if not self.price and self.select_membership:
            self.price = self.select_membership.price

        # Automatically set payment status to 'Pending' if it's not provided
        if not self.payment_status:
            self.payment_status = 'Pending'

        super().save(*args, **kwargs)
    


    




