from django.db import models
from django.conf import settings
from shipments.models import Shipment

class LogisticsRecord(models.Model):
    EVENT_CHOICES = (
        ('pickup', '取件'),
        ('transit', '运输'),
        ('transfer', '中转'),
        ('delivery', '派送'),
        ('delivered', '送达'),
    )
    
    shipment = models.ForeignKey(
        Shipment,
        on_delete=models.CASCADE,
        related_name='logistics_records',
        verbose_name='快递单'
    )
    handler = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='handled_records',
        verbose_name='处理人员'
    )
    event_type = models.CharField(max_length=20, choices=EVENT_CHOICES, verbose_name='事件类型')
    location = models.CharField(max_length=100, verbose_name='地点')
    description = models.TextField(verbose_name='描述')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='时间戳')
    
    class Meta:
        verbose_name = '物流记录'
        verbose_name_plural = '物流记录'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['event_type']),
        ]
    
    def __str__(self):
        return f"{self.shipment.tracking_number} - {self.get_event_type_display()}"
