from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import LogisticsRecord
from shipments.models import Shipment

# Create your views here.

@login_required
def create_record(request, tracking_number):
    if request.user.user_type != 'staff':
        messages.error(request, '只有物流人员才能添加物流记录！')
        return redirect('shipments:shipment_detail', tracking_number=tracking_number)
    
    shipment = get_object_or_404(Shipment, tracking_number=tracking_number)
    
    if request.method == 'POST':
        logistics_record = LogisticsRecord.objects.create(
            shipment=shipment,
            handler=request.user,
            event_type=request.POST['event_type'],
            location=request.POST['location'],
            description=request.POST['description']
        )
        
        # 更新快递单状态
        if request.POST['event_type'] == 'pickup':
            shipment.status = 'picked_up'
        elif request.POST['event_type'] in ['transit', 'transfer']:
            shipment.status = 'in_transit'
        elif request.POST['event_type'] == 'delivery':
            shipment.status = 'in_transit'
        elif request.POST['event_type'] == 'delivered':
            shipment.status = 'delivered'
        shipment.save()
        
        messages.success(request, '物流记录添加成功！')
        return redirect('shipments:shipment_detail', tracking_number=tracking_number)
    
    return render(request, 'logistics/create_record.html', {'shipment': shipment})

@login_required
def record_list(request, tracking_number):
    shipment = get_object_or_404(Shipment, tracking_number=tracking_number)
    records = LogisticsRecord.objects.filter(shipment=shipment).order_by('-timestamp')
    return render(request, 'logistics/record_list.html', {'records': records, 'shipment': shipment})

@login_required
def task_list(request):
    if request.user.user_type != 'staff':
        messages.error(request, '只有物流人员才能查看任务列表！')
        return redirect('shipments:home')
    
    pending_shipments = Shipment.objects.filter(status='pending')
    in_transit_shipments = Shipment.objects.filter(status__in=['picked_up', 'in_transit'])
    
    context = {
        'pending_shipments': pending_shipments,
        'in_transit_shipments': in_transit_shipments
    }
    
    return render(request, 'logistics/task_list.html', context)
