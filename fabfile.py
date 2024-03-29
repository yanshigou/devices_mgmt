# -*- coding: utf-8 -*-

from datetime import datetime
from fabric.api import *
from fabvenv import virtualenv

# 登录用户和主机名：
env.user = 'ubuntu'
env.password = 'Cmx170904'
env.hosts = ['111.230.246.188']
pack_name = 'deploypack_devices_mgmt.tar.gz'


def pack():
    ' 定义一个pack任务 '
    # 打一个tar包：
    local('del %s' % pack_name)
    local('md ..\pack_tmp')
    local('xcopy /e /s .\* ..\pack_tmp')
    with lcd('..\pack_tmp'):
        local('tar -czvf ../devices_mgmt/%s --exclude *.pyc --exclude fabfile.py --exclude .git '
              '--exclude */__pycache__/ --exclude .git --exclude 00* --exclude *.tar.gz  ./*' % pack_name)
    local('rd /s /q ..\pack_tmp')


def deploy():
    ' 定义一个部署任务 '
    tag = datetime.now().strftime('%y.%m.%d_%H.%M.%S')
    print(env.host)
    hosttag = ''
    remote_work_dir = ''
    if env.host == '111.230.246.188':
        remote_work_dir = '/home/ubuntu/www/devices_mgmt/'
        hosttag = 'cmx'
    else:
        exit(1)

    remote_tmp_tar = '/tmp/%s' % pack_name
    run('rm -f %s' % remote_tmp_tar)
    # 上传tar文件至远程服务器：
    put(pack_name, remote_tmp_tar)
    # 备份远程服务器工程
    # back_tar_name = '/home/ubuntu/www/backup/cmxsite_backup_%s.tar.gz' % tag
    # run('tar -czvf %s /home/ubuntu/www/cmxsite/*' % back_tar_name)
    # 删除原有工程
    # run('rm -rf /home/ubuntu/www/cmxsite/*')
    # 解压：
    run('tar -xzvf %s -C %s' % (remote_tmp_tar, remote_work_dir))
    run('mv %sother/settings_%s.py %s/devices_mgmt/settings.py' % (remote_work_dir, hosttag, remote_work_dir))
    run('mv %sother/devices_mgmt_nginx_%s.conf %s/devices_mgmt_nginx.conf' % (remote_work_dir, hosttag, remote_work_dir))
    run('mv %sother/devices_mgmt_uwsgi_%s.ini %s/devices_mgmt_uwsgi.ini' % (remote_work_dir, hosttag, remote_work_dir))
    run('mv %sother/uwsgi_params_%s %s/uwsgi_params' % (remote_work_dir, hosttag, remote_work_dir))
    run('rm -rf %sother' % remote_work_dir)
    with cd(remote_work_dir):
        with virtualenv('/home/ubuntu/www/devices_mgmt/kkwork'):
            run('python manage.py makemigrations')
            run('python manage.py migrate')
            run('chmod a+x ./restart.sh')
            run('sh ./restart.sh', pty=False)
            # run('sudo service nginx restart')
            run('sleep 5')
