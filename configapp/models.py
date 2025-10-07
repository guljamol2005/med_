from django.db import models

class Client(models.Model):
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.full_name

class Employee(models.Model):
    full_name = models.CharField(max_length=255)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.full_name

class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, related_name='orders')
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id} - {self.client}'


class Product(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0)  
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
