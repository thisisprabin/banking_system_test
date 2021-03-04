from django.db import models


__all__ = ["User", "Transaction", "Account"]


class User(models.Model):

    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email_id = models.CharField(max_length=320)
    otp = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name)


class Account(models.Model):

    account_number = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class Transaction(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    operation = models.IntegerField()  # 1 - Deposit, 2 - Withdraw, 3 - Enquiry
    transaction_date = models.DateTimeField(default=None)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
