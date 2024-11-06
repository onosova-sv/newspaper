from django.db import models
from datetime import datetime

# Create your models here.


class Product (models.Model):
    name = models.CharField(max_length=255, default = 'Default value')
    price = models.FloatField(default=0.0)
director = 'DI'
admin = 'AD'
cook = 'CO'
cashier = 'CA'
cleaner = 'CL'

POSITIONS = [
    (director, 'Директор'),
    (admin, 'Администратор'),
    (cook, 'Повар'),
    (cashier, 'Кассир'),
    (cleaner, 'Уборщик')
    ]
class Staff (models.Model):
    full_name = models.CharField(max_length = 255, default = 'Default value')
    position = models.CharField(max_length = 2, 
                            choices = POSITIONS, 
                            default = cashier)
    labor_contract = models.IntegerField(default=0)
    def get_last_name(self):
        return self.full_name.split()[0] 

class Order (models.Model): 
    time_in = models.DateTimeField(auto_now_add = True, null = True)
    time_out = models.DateTimeField(null = True)
    cost = models.FloatField(default = 0.0)
    pickup = models.BooleanField(default = False)    
    complete = models.BooleanField(default = False)
    staff = models.ForeignKey(Staff, on_delete = models.CASCADE, default = None)
    products = models.ManyToManyField(Product, through = 'PO')

    def finish_order(self):
        self.time_out = datetime.now()
        self.complete = True
        self.save()

    def get_duration(self):
        if self.complete:  # если завершён, возвращаем разность объектов
            return (self.time_out - self.time_in).total_seconds() // 60
        else:  # если ещё нет, то сколько длится выполнение
            return (datetime.now(timezone.utc) - self.time_in).total_seconds() // 60

class PO (models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, default = None)
    order = models.ForeignKey(Order, on_delete = models.CASCADE, default = None)
    _amount = models.IntegerField(default = 1)

    def product_sum(self):
        product_price = self.product.price
        return product_price * self.amount

    @property
    def amount(self):
        return self._amount




        
    