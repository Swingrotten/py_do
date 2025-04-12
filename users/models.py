from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('sender', '发件人'),
        ('receiver', '收件人'),
        ('staff', '物流人员'),
        ('admin', '管理员'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='sender', verbose_name='用户类型')
    phone = models.CharField(max_length=15, blank=True, verbose_name='电话号码')
    address = models.TextField(blank=True, verbose_name='地址')
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
