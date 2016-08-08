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
vi /etc/supervisord.conf
[program:vex-test-ui]
directory=/home/yanyang/VEXTestUI
user=root
command=python manage.py runserver 0.0.0.0:8000
process_name=vex-test-ui
numprocs=1
autostart=true
autorestart=true

--------------------生产环境阶段------------------
项目代码目录:/home/yanyang/VEXTestUI
执行uwsgi --ini config/uwsgi.ini （可以启动supervisord service去维护项目运行),执行后看看状态ps -ef | grep uwsgi
合并nginx.conf到/etc/nginx.conf之后重启nginx

采用supervisord启动
vi /etc/supervisord.conf
[program:vextestui]
directory=/home/yanyang/VEXTestUI
user=root
command=uwsgi --ini /home/yanyang/VEXTestUI/config/uwsgi.ini
process_name=vextestui
numprocs=1
autostart=true
autorestart=true
stopsignal=QUIT

注意:supervisord默认管理的是非守护进程的程序，如果采用守护进程用supervisord启动的话，会出现backoff的错误或者exit too fast的错误。当需要采用supervisord进行守护程序的时候，在uwsgi配置文件或者参数中必须不能设置daemonize=/var/log/vextestui.log(此时的log文件使用的是setting.py中的log文件设置)

--------------------压力测试----------------------
ab -c 100 -n 6000 http://127.0.0.1/
Percentage of the requests served within a certain time (ms)
  50%    549
  66%    566
  75%    575
  80%    582
  90%    600
  95%    614
  98%    634
  99%    648
 100%    711 (longest request)
