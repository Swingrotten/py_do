from django.db import models
from django.conf import settings

class Shipment(models.Model):
    STATUS_CHOICES = (
        ('pending', '待处理'),
        ('picked_up', '已取件'),
        ('in_transit', '运输中'),
        ('delivered', '已送达'),
        ('completed', '已完成'),
    )
    
    tracking_number = models.CharField(max_length=20, unique=True, verbose_name='运单号')
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_shipments',
        verbose_name='发件人'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_shipments',
        verbose_name='收件人'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    
    # 包裹信息
    weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='重量(kg)')
    description = models.TextField(verbose_name='包裹描述')
    
    # 地址信息
    pickup_address = models.TextField(verbose_name='取件地址')
    delivery_address = models.TextField(verbose_name='送达地址')
    
    # 时间信息
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    estimated_delivery = models.DateTimeField(null=True, blank=True, verbose_name='预计送达时间')
    
    class Meta:
        verbose_name = '快递单'
        verbose_name_plural = '快递单'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tracking_number']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"快递单号: {self.tracking_number}"
        
    def get_status_display_color(self):
        """返回状态对应的Bootstrap颜色类"""
        status_colors = {
            'pending': 'warning',
            'picked_up': 'info',
            'in_transit': 'primary',
            'delivered': 'success',
            'completed': 'secondary',
        }
        return status_colors.get(self.status, 'dark')
