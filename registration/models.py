from django.db import models

# User Model (Existing)
class UserRegistration(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=250)
    password = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Expense Model (New for WalletWatcher)
class Expense(models.Model):
    # Link expense to a specific user
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50) # e.g. Food, Transport
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"