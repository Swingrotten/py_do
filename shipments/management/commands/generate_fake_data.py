import random
import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from shipments.models import Shipment
from logistics.models import LogisticsRecord
import uuid
from faker import Faker

User = get_user_model()
fake = Faker('zh_CN')  # 使用中文

class Command(BaseCommand):
    help = '生成测试数据'

    def add_arguments(self, parser):
        parser.add_argument('--users', type=int, default=20, help='要创建的用户数量')
        parser.add_argument('--shipments', type=int, default=50, help='要创建的快递单数量')
        parser.add_argument('--records', type=int, default=100, help='要创建的物流记录数量')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('开始生成测试数据...'))
        
        # 创建超级用户
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123456',
                user_type='admin'
            )
            self.stdout.write(self.style.SUCCESS(f'创建了超级用户: {admin.username}'))
        
        # 生成用户
        users_count = options['users']
        self._create_users(users_count)
        
        # 生成快递单
        shipments_count = options['shipments']
        self._create_shipments(shipments_count)
        
        # 生成物流记录
        records_count = options['records']
        self._create_logistics_records(records_count)
        
        self.stdout.write(self.style.SUCCESS('数据生成完成!'))

    def _create_users(self, count):
        user_types = ['sender', 'receiver', 'staff']
        existing_count = User.objects.count()
        
        # 确保至少有一个每种类型的用户
        for user_type in user_types:
            if not User.objects.filter(user_type=user_type).exists():
                username = f"{user_type}_user"
                User.objects.create_user(
                    username=username,
                    email=f"{username}@example.com",
                    password="password123",
                    user_type=user_type,
                    phone=fake.phone_number(),
                    address=fake.address(),
                    first_name=fake.first_name(),
                    last_name=fake.last_name()
                )
                count -= 1
                self.stdout.write(self.style.SUCCESS(f'创建了{user_type}用户'))
        
        # 创建剩余随机用户
        for i in range(count):
            user_type = random.choice(user_types)
            username = f"{user_type}_{existing_count + i + 1}"
            User.objects.create_user(
                username=username,
                email=f"{username}@example.com",
                password="password123",
                user_type=user_type,
                phone=fake.phone_number(),
                address=fake.address(),
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
        
        self.stdout.write(self.style.SUCCESS(f'创建了{count}个用户'))

    def _create_shipments(self, count):
        senders = User.objects.filter(user_type='sender')
        receivers = User.objects.filter(user_type='receiver')
        
        if not senders or not receivers:
            self.stdout.write(self.style.ERROR('没有足够的发件人或收件人!'))
            return
        
        statuses = ['pending', 'picked_up', 'in_transit', 'delivered', 'completed']
        
        for i in range(count):
            sender = random.choice(senders)
            receiver = random.choice(receivers)
            status = random.choice(statuses)
            
            # 创建日期在过去30天内随机
            days_ago = random.randint(0, 30)
            created_date = timezone.now() - datetime.timedelta(days=days_ago)
            
            # 预计送达日期在创建日期后1-7天
            est_delivery = created_date + datetime.timedelta(days=random.randint(1, 7))
            
            shipment = Shipment.objects.create(
                tracking_number=str(uuid.uuid4().hex)[:12].upper(),
                sender=sender,
                receiver=receiver,
                status=status,
                weight=round(random.uniform(0.1, 20.0), 2),
                description=fake.paragraph(),
                pickup_address=sender.address or fake.address(),
                delivery_address=receiver.address or fake.address(),
                created_at=created_date,
                estimated_delivery=est_delivery
            )
            
            # 手动更新创建时间，因为auto_now_add会覆盖我们的设置
            Shipment.objects.filter(id=shipment.id).update(created_at=created_date)
        
        self.stdout.write(self.style.SUCCESS(f'创建了{count}个快递单'))

    def _create_logistics_records(self, count):
        shipments = Shipment.objects.all()
        staff_users = User.objects.filter(user_type='staff')
        
        if not shipments or not staff_users:
            self.stdout.write(self.style.ERROR('没有快递单或物流人员!'))
            return
        
        event_types = ['pickup', 'transit', 'transfer', 'delivery', 'delivered']
        locations = [
            '北京分拣中心', '上海转运中心', '广州物流站', '深圳仓库', 
            '成都配送点', '武汉中转站', '杭州集散地', '南京营业部',
            '重庆分拣中心', '西安物流点', '天津中转站', '青岛配送中心'
        ]
        
        for i in range(count):
            shipment = random.choice(shipments)
            handler = random.choice(staff_users)
            event_type = random.choice(event_types)
            location = random.choice(locations)
            
            # 时间戳在快递单创建时间后，但不超过现在
            created_at = shipment.created_at
            now = timezone.now()
            timestamp = created_at + datetime.timedelta(
                seconds=random.randint(0, int((now - created_at).total_seconds()))
            )
            
            record = LogisticsRecord.objects.create(
                shipment=shipment,
                handler=handler,
                event_type=event_type,
                location=location,
                description=fake.paragraph(),
                timestamp=timestamp
            )
            
            # 手动设置时间戳
            LogisticsRecord.objects.filter(id=record.id).update(timestamp=timestamp)
        
        # 根据物流记录更新快递单状态
        for shipment in shipments:
            records = LogisticsRecord.objects.filter(shipment=shipment).order_by('timestamp')
            if records.exists():
                latest_record = records.last()
                
                # 根据最新记录更新状态
                if latest_record.event_type == 'pickup':
                    new_status = 'picked_up'
                elif latest_record.event_type in ['transit', 'transfer']:
                    new_status = 'in_transit'
                elif latest_record.event_type == 'delivery':
                    new_status = 'in_transit'
                elif latest_record.event_type == 'delivered':
                    new_status = 'delivered'
                else:
                    new_status = shipment.status
                
                # 使用订单状态覆盖自动生成的状态，保持一致性
                Shipment.objects.filter(id=shipment.id).update(status=new_status)
        
        self.stdout.write(self.style.SUCCESS(f'创建了{count}条物流记录')) 