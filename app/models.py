from django.db import models
from django.contrib.auth.models import User
# Create your models here.
STATE_CHOICES=(
    ('Andaman & Nicobar Islands','Andaman & Nicobar Islands'),
    ('Andhra Pardesh','Andhra Pardesh'),
    ('Arunchal Pardesh','Arunchal Pardesh'),
    ('Assam ','Assam'),
    ('Bihar','Bihar'),
    ('Chandighar','Chandighar'),
    ('Chattisghar','Chattisghar'),
    ('Dadea & Nagra Haveli','Dadea & Nagra Haveli'),
    ('Daman and Diu','Daman and Diu'),
    ('Delhi','Delhi'),
    ('Goa','Goa'),
    ('Gujrat','Gujrat'),
    ('Haryana','Haryana'),
    ('Himachal Pardesh','Himachal Pardesh'),
    ('jammu & Kashmir','jammu & Kashmir'),
    ('Jharkhand','Jharkhand'),
    ('Karnatak','Karnatak'),
    ('Kerala','Kerala'),
    ('Lakshadweep','Lakshadweep'),
    ('Madhya Pardesh','Madhya Pardesh'),
    ('Maharashtra','Maharashtra'),
    ('ManiPur','ManiPur'),
    ('Meghalaya','Meghalaya'),
    ('Nahaland','Nahaland'),
    ('odisa','odisa'),
    ('Puducherry','Puducherry'),
    ('Punjab','Punjab'),
    ('Rajsthan','Rajsthan'),
    ('Sikkim','Sikkim'),
    ('Tamil Nadu','Tamil Nadu'),
    ('Telangna','Telangna'),
    ('UttaraKhand','UttaraKhand'),
    ('Utter Pardesh','Utter Pardesh'),
    ('West Bengal','West Bengal'),
    
)


CATEGORY_CHOICES=(
    ('CR','Curd'),
    ('ML','Milk'),
    ('LS','Lassi'),
    ('MS','Milkshake'),
    ('PN','Paneer'),
    ('GH','Ghee'),
    ('IC','Ice-Creams'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    product_image = models.ImageField(upload_to='product')
    
    def __str__(self):
        return self.title

class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=100)
    
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
 
STATUS_CHOICES =(
    ('Accepeted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Pending','Pending'),
)   

class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_order_status = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    paid = models.BooleanField(default=False)
    
class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_data = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='pending')
    payment =  models.ForeignKey(Payment,on_delete=models.CASCADE,default="")
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price