from django.db import models

class CuedApplicants(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return self.first_name + " " + self.last_name

class ProcessedApplicants(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    processed_date = models.DateTimeField(auto_now_add=True)
    credit_score = models.IntegerField(blank=True, null=True)
    employer = models.CharField(max_length=255, blank=True, null=True)
    annual_income = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    criminal_record = models.BooleanField(default=False)
    bankruptcies = models.IntegerField(default=0)

    def __str__(self):
        return self.first_name + " " + self.last_name

class Associates(models.Model):
    processed_applicant = models.ForeignKey(ProcessedApplicants, related_name='associates', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    relationship = models.CharField(max_length=255)

    def __str__(self):
        return self.name