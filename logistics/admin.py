from django.contrib import admin
from .models import LogisticsRecord

@admin.register(LogisticsRecord)
class LogisticsRecordAdmin(admin.ModelAdmin):
    list_display = ['shipment', 'event_type', 'handler', 'location', 'timestamp']
    list_filter = ['event_type', 'timestamp']
    search_fields = ['shipment__tracking_number', 'handler__username', 'location', 'description']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'
    
    fieldsets = (
        ('基本信息', {'fields': ('shipment', 'event_type', 'handler')}),
        ('详细信息', {'fields': ('location', 'description')}),
        ('时间信息', {'fields': ('timestamp',)}),
    )
    
    list_per_page = 25
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        # 非超级管理员只能看到自己处理的物流记录
        if hasattr(request.user, 'user_type') and request.user.user_type == 'staff':
            return queryset.filter(handler=request.user)
        return queryset.none()
