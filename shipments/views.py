from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Shipment
from django.conf import settings
import uuid

def home(request):
    return render(request, 'shipments/home.html')

@login_required
def create_shipment(request):
    if request.user.user_type != 'sender':
        messages.error(request, '只有发件人才能创建快递单！')
        return redirect('shipments:home')
    
    User = settings.AUTH_USER_MODEL
    user_list = User.objects.all()
    
    if request.method == 'POST':
        # 生成唯一的运单号
        tracking_number = str(uuid.uuid4().hex)[:12].upper()
        
        shipment = Shipment.objects.create(
            tracking_number=tracking_number,
            sender=request.user,
            receiver_id=request.POST['receiver'],
            weight=request.POST['weight'],
            description=request.POST['description'],
            pickup_address=request.POST['pickup_address'],
            delivery_address=request.POST['delivery_address']
        )
        messages.success(request, f'快递单创建成功！运单号：{tracking_number}')
        return redirect('shipments:shipment_detail', tracking_number=tracking_number)
    
    return render(request, 'shipments/create_shipment.html', {'user_list': user_list})

@login_required
def shipment_list(request):
    # 基本查询
    if request.user.user_type == 'staff' or request.user.is_superuser:
        queryset = Shipment.objects.all()
    else:
        queryset = Shipment.objects.filter(
            Q(sender=request.user) | Q(receiver=request.user)
        )
    
    # 搜索功能
    search_query = request.GET.get('search', '')
    if search_query:
        queryset = queryset.filter(
            Q(tracking_number__icontains=search_query) |
            Q(sender__username__icontains=search_query) |
            Q(receiver__username__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # 状态筛选
    status_filter = request.GET.get('status', '')
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    
    # 排序
    queryset = queryset.order_by('-created_at')
    
    # 分页
    paginator = Paginator(queryset, 10)  # 每页显示10条
    page_number = request.GET.get('page', 1)
    shipments = paginator.get_page(page_number)
    
    return render(request, 'shipments/shipment_list.html', {'shipments': shipments})

@login_required
def shipment_detail(request, tracking_number):
    shipment = get_object_or_404(Shipment, tracking_number=tracking_number)
    return render(request, 'shipments/shipment_detail.html', {'shipment': shipment})

@login_required
def confirm_receipt(request, tracking_number):
    shipment = get_object_or_404(Shipment, tracking_number=tracking_number)
    
    if request.user != shipment.receiver:
        messages.error(request, '只有收件人才能确认收货！')
        return redirect('shipments:shipment_detail', tracking_number=tracking_number)
    
    if shipment.status != 'delivered':
        messages.error(request, '只有已送达的快递才能确认收货！')
        return redirect('shipments:shipment_detail', tracking_number=tracking_number)
    
    shipment.status = 'completed'
    shipment.save()
    
    messages.success(request, '已确认收货，感谢您使用我们的服务！')
    return redirect('shipments:shipment_detail', tracking_number=tracking_number)
