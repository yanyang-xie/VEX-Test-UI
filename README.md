# VEX-Test-UI

使用Django1.8与Bootstrap3搭建VEX测试结果展示的系统

pip install -r requirment.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

--------------------调试阶段------------------
手工启动
python manage.py runserver 0.0.0.0:8000

或者采用supervisord
[program:vex-test-ui]
directory=/home/yanyang/VEX-Test-UI
user=root
command=python manage.py runserver 0.0.0.0:8000
process_name=vex-test-ui
numprocs=1
autostart=true
autorestart=true

--------------------生产环境阶段------------------
项目代码目录:/home/yanyang/VEXTestUI
执行uwsgi --ini config/uwsgi.init （可以启动supervisord去执行这个命令）
合并nginx.conf到/etc/nginx.conf

