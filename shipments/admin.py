from django.contrib import admin
from .models import Shipment

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['tracking_number', 'sender', 'receiver', 'status', 'weight', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at']
    search_fields = ['tracking_number', 'sender__username', 'receiver__username', 'description']
    readonly_fields = ['tracking_number', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('基本信息', {'fields': ('tracking_number', 'status')}),
        ('用户信息', {'fields': ('sender', 'receiver')}),
        ('包裹信息', {'fields': ('weight', 'description')}),
        ('地址信息', {'fields': ('pickup_address', 'delivery_address')}),
        ('时间信息', {'fields': ('created_at', 'updated_at', 'estimated_delivery')}),
    )
    
    list_per_page = 20
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # 编辑现有对象
            return self.readonly_fields
        return []  # 创建新对象时没有只读字段
