# 快递流转系统

基于Django的快递流转系统，用于管理快递单的生成、物流跟踪和收件管理。

## 系统功能

### 发送方
- 完成快递单生成
- 投送管理
- 身份核查
- 查阅进程

### 物流方
- 接单管理
- 派单流程
- 转运流程记录生成
- 接收方身份验证

### 接收方
- 收件管理
- 验收流程
- 查询物流动向

## 技术栈

- 后端：Django 4.2.7
- 前端：HTML、CSS、JavaScript、Bootstrap 5
- 数据库：支持PostgreSQL和MySQL/MariaDB

## 安装说明

1. 克隆项目

```bash
git clone <repository-url>
cd express_system
```

2. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. 安装依赖

```bash
pip install -r requirements.txt
```

4. 配置数据库

编辑 `express_system/settings.py` 文件，配置数据库连接信息:

### PostgreSQL配置:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'express_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### MySQL/MariaDB配置:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'express_db',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}
```

5. 创建数据库和表

```bash
python manage.py makemigrations
python manage.py migrate
```

6. 创建超级用户

```bash
python manage.py createsuperuser
```

7. 运行开发服务器

```bash
python manage.py runserver
```

## 使用说明

1. 访问 `http://localhost:8000/` 进入系统首页
2. 注册不同角色的用户（发件人、收件人、物流人员）
3. 使用对应角色的功能

## MySQL/MariaDB设置

如需使用MySQL/MariaDB数据库，请查看 `setup_mysql.md` 文件获取详细设置指南。

## 扩展接口

系统提供了以下扩展接口，可用于自定义功能:

### API 接口
- `/api/shipments/` - 快递单API
- `/api/logistics/` - 物流记录API

### 自定义扩展
- 支持自定义物流事件类型
- 支持自定义状态流转规则
- 支持自定义通知方式和模板