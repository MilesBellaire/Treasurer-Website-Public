from email.policy import default
from django.db import models
from datetime import date as d
from django.contrib.auth.models import User


class ReimbursementRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)
    date = models.DateField(default=d.today)
    reason = models.CharField(max_length=300)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    payable_to = models.CharField(max_length=50)
    receipt = models.ImageField(upload_to="main/files/receipts", blank=True, null=True)

    def __str__(self):
        retval = self.user.first_name + " " + self.user.last_name + " requested $" + str(self.amount) + " paid to " + self.payable_to + " on " + str(self.date) + " for " + self.reason + " and has "
        if not self.approved: retval += "not "
        retval += "been approved"
        return retval