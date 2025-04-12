# MySQL/MariaDB数据库设置指南

## 1. 安装MySQL驱动

首先需要安装MySQL的Python驱动：

```bash
pip install mysqlclient
```

## 2. 创建数据库

连接到MySQL服务器并创建数据库：

```sql
CREATE DATABASE express_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## 3. 执行数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

## 4. 创建超级用户

```bash
python manage.py createsuperuser
```

## 注意事项

如果在安装mysqlclient时遇到问题，可能需要先安装相关的系统库：

### 在Ubuntu/Debian上：
```bash
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
```

### 在CentOS/RHEL上：
```bash
sudo yum install python3-devel mysql-devel
```

### 在Windows上：
从[这里](https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient)下载预编译的wheel文件，然后使用pip安装它：
```bash
pip install mysqlclient-1.4.6-cp39-cp39-win_amd64.whl
```
(根据您的Python版本选择适当的wheel文件) 