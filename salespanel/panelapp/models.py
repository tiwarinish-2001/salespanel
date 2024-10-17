from django.db import models # type: ignore

# Create your models here.
# class ClientData(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     phonenumber = models.CharField(max_length=15)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     investigate_date = models.DateField(null=True, blank=True)
#     schedule_date = models.DateField(null=True, blank=True)
#     lead = models.CharField(max_length=100)
#     response = models.TextField()
#     assigned_user = models.CharField(max_length=15)
#     description = models.TextField(null=True, blank=True)  # Added description field

#     def __str__(self):
#         return self.name
    
class ClientData(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phonenumber = models.CharField(max_length=15)
    company_name = models.CharField(max_length=100, null=True, blank=True)  # Added company_name field
    location = models.CharField(max_length=100, null=True, blank=True)  # Added location field
    timestamp = models.DateTimeField(auto_now_add=True)
    investigate_date = models.DateField(null=True, blank=True)
    schedule_date = models.DateField(null=True, blank=True)
    lead = models.CharField(max_length=100)
    response = models.TextField()
    assigned_user = models.CharField(max_length=15)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    

# class UserSubmits(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField()
#     phonenumber = models.CharField(max_length=15)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     investigate_date = models.DateField(null=True, blank=True)
#     schedule_date = models.DateField(null=True, blank=True)
#     lead = models.CharField(max_length=100)
#     response = models.TextField()
#     assigned_user = models.CharField(max_length=15)
#     reviewed = models.IntegerField(default=0)
#     description = models.TextField(null=True, blank=True)  # Added description field

#     def __str__(self):
#         return self.name
class UserSubmits(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phonenumber = models.CharField(max_length=15)
    company_name = models.CharField(max_length=100, null=True, blank=True)  # Added company_name field
    location = models.CharField(max_length=100, null=True, blank=True)  # Added location field
    timestamp = models.DateTimeField(auto_now_add=True)
    investigate_date = models.DateField(null=True, blank=True)
    schedule_date = models.DateField(null=True, blank=True)
    lead = models.CharField(max_length=100)
    response = models.TextField()
    assigned_user = models.CharField(max_length=15)
    reviewed = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    
    
# class UserClientInteraction(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.EmailField()
#     phonenumber = models.CharField(max_length=15)
#     investigate_date = models.DateField(null=True, blank=True)
#     schedule_date = models.DateField(null=True, blank=True)
#     lead = models.CharField(max_length=255, null=True, blank=True)
#     response = models.TextField(null=True, blank=True)
#     assigned_user = models.CharField(max_length=255)
#     description = models.TextField(null=True, blank=True)  # Added description field

#     def __str__(self):
#         return f"{self.name} - {self.phonenumber}"

class UserClientInteraction(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phonenumber = models.CharField(max_length=15)
    company_name = models.CharField(max_length=100, null=True, blank=True)  # Added company_name field
    location = models.CharField(max_length=100, null=True, blank=True)  # Added location field
    investigate_date = models.DateField(null=True, blank=True)
    schedule_date = models.DateField(null=True, blank=True)
    lead = models.CharField(max_length=255, null=True, blank=True)
    response = models.TextField(null=True, blank=True)
    assigned_user = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.phonenumber}"

