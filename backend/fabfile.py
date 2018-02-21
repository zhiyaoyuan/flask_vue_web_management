# coding=utf-8
# filename: fabfile.py
"""
Fabric自动化部署Flask应用
把该文件放在Flask app同级文件夹即可。

Python3 install: pip3 install fabric3

Windows下tar打包可以使用Cygwin，并安装tar命令
Cygwin官网：http://www.cygwin.com/

- 查看所有fab命令：
  fab -l 

- 第一次上传代码：
  fab push
  fab updatedep
  fab updateenv

- 更新代码：
  fab push

- 部署到Supervisor：
  fab deploy_sup

- 部署到Nginx：
  fab deploy_nginx
  OR
  fab deploy_nginx:1    # 部署并重启

"""

import os
import time
import platform
from fabric.api import *
from fabric.contrib.console import confirm

nowTime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

##########################################################################
# 配置

# 主机参数
# 登录用用户名、密码和主机：
env.hosts = ['127.0.0.1']  # 如果有多个主机，fabric会自动依次部署
env.user = 'root'
#env.password = ""


# 打包文件名
APP_NAME = "app"
TAR_PACK = APP_NAME + "-" + nowTime + ".tar.gz"  # app_20180123150715.tar.gz
TAR_PACK_RM = APP_NAME + "-*.tar.gz"  # 匹配旧的压缩包

# 远程服务器文件夹
REMOTE_DIR = APP_NAME
REMOTE_TAR = REMOTE_DIR + "/" + TAR_PACK

# 依赖文件
REQUIREMENTS_FILE = "requirements.txt"

# 需要打包的文件和文件夹
#TAR_FILES = ['*.py', 'static/*', 'templates/*', 'favicon.ico']
TAR_FILES = ['*.py', "*.ini", "*.sh", "*.conf",
             REQUIREMENTS_FILE, "app/*", "deploy/*"]

# 虚拟环境文件夹名称
VENV_DIR = "venv"


# 部署参数

DEPLOY_DIR = REMOTE_DIR + "/deploy"
# supervisor配置文件
SUPERVISOR_CONFIG_FILE = "supervisor_config_app.ini"
# 部署到Supervisor文件夹的配置文件名
SUPERVISOR_DEPLOY_NAME = "supervisor_config_" + APP_NAME + ".ini"
# 服务器放置Supervisor配置文件的文件夹路径
SUPERVISOR_PATH = "/etc/supervisord.d/"

# app的Nginx配置文件
NGINX_CONFIG_FILE = "nginx_config_app.conf"
NGINX_DEPLOY_NAME = "nginx_config_" + APP_NAME + ".conf"
NGINX_PATH = "/etc/nginx/conf.d/"

##########################################################################


def pack(pack_name=TAR_PACK):
    """
    本地代码打包
    """
    with settings(warn_only=True):  # 用来忽略某些不存在的文件
        local("rm -f " + TAR_PACK_RM)   # 首先删除旧的tar包
        local("tar -cvzf " + pack_name +
              " --exclude='*.tar.gz' --exclude='fabfile.py' --exclude=*.pyc %s" %
              ' '.join(TAR_FILES)
              )


def upload(pack_name=TAR_PACK):
    """
    本地代码压缩包上传
    """
    # 检查远程服务器文件夹
    ret = run("ls")
    if REMOTE_DIR not in ret:
        # mkdir(REMOTE_DIR)
        run("mkdir %s" % REMOTE_DIR)

    # 进入工程目录
    with cd(REMOTE_DIR):
        # 删除远程服务器tar包
        with settings(warn_only=True):
            #run('rm -f %s' % TAR_PACK)
            run('rm -f %s' % TAR_PACK_RM)

        # 上传tar文件至远程服务器
        put(TAR_PACK, TAR_PACK)
        # 解压
        with settings(warn_only=True):
            run("tar -xvzf %s" % TAR_PACK)
        # 改变权限
        run("chmod 775 -R ./*")


def push(venv_dir=VENV_DIR, pack_name=TAR_PACK):
    """
    本地代码打包并上传
    """
    # updatedep(venv_dir)
    pack(pack_name)
    upload(pack_name)


def createenv(venv_dir=VENV_DIR):
    """
    远程服务器创建虚拟环境
    """
    # 进入工程目录
    with cd(REMOTE_DIR):
        # 检查文件夹
        ls = run("ls")
        if venv_dir in ls:
            ret = confirm(venv_dir + "文件夹存在，是否删除重建？")
            if ret:
                run("rm -r ./" + venv_dir)
        run("python3 -m venv ./" + venv_dir)
        # 检测虚拟环境下的pip3
        run("./" + venv_dir + "/bin/pip3 -V")


def updateenv(venv_dir=VENV_DIR):
    """
    更新远程服务器虚拟环境（如果venv不存在则询问是否创建）
    """
    with cd(REMOTE_DIR):
        # 检查文件夹
        ls = run("ls")

        # 判断服务器端虚拟环境是否存在
        if venv_dir not in ls:
            ret = confirm(venv_dir + "不存在，是否创建？")
            if not ret:
                return  # 不创建则退出
            run("python3 -m venv ./" + venv_dir)

        # 检测虚拟环境下的pip3
        run("./" + venv_dir + "/bin/pip3 -V")

        # 更新本地依赖文件
        updatedep(venv_dir)
        # 上传依赖文件
        put(REQUIREMENTS_FILE, REQUIREMENTS_FILE)

        run("./" + venv_dir + "/bin/pip3 install -r " + REQUIREMENTS_FILE)


def updatedep(venv_dir=VENV_DIR):
    """
    更新本地依赖文件
    """
    if "Windows" == platform.system():
        pip = os.path.join(".", venv_dir, "Scripts", "pip.exe")
        ret = os.path.exists(pip)
        if not ret:
            print("pip不存在！")
            return
        local(pip + " -V")  # 验证pip路径
        local(pip + " freeze > " + REQUIREMENTS_FILE)


def deploy_sup(option="cp"):
    """
    部署app到Supervisor
    """
    with cd(DEPLOY_DIR):
        # 检查文件
        ls = run("ls")
        if SUPERVISOR_CONFIG_FILE not in ls:
            print(SUPERVISOR_CONFIG_FILE + "文件不存在！")
            return

        deploy_path = os.path.join(SUPERVISOR_PATH, SUPERVISOR_DEPLOY_NAME)
        sudo("rm -f " + deploy_path)
        if "cp" == option:
            sudo("cp " + SUPERVISOR_CONFIG_FILE + " " + deploy_path)
        elif "ln" == option:
            sudo("ln -s " + SUPERVISOR_CONFIG_FILE + " " + deploy_path)

        # Supervisor加载新的配置
        sudo("supervisorctl update")


def deploy_nginx(reload=False):
    """
    部署app到nginx
    """
    with cd(DEPLOY_DIR):

        # 检查文件
        ls = run("ls")
        if NGINX_CONFIG_FILE not in ls:
            print(NGINX_CONFIG_FILE + "文件不存在！")
            return

        deploy_path = os.path.join(NGINX_PATH, NGINX_DEPLOY_NAME)
        sudo("rm -f " + deploy_path)
        sudo("cp " + NGINX_CONFIG_FILE + " " + deploy_path)

        ret = sudo("sudo nginx -t")   # 检查Nginx的配置
        if reload and ("ok" in ret):
            sudo("service nginx reload")


def deploy(mod):
    """
    部署
    """
    if "sup" == mod:
        deploy_sup()
    elif "nginx" == mod:
        deploy_nginx()


def clean():
    with settings(warn_only=True):
        local('rm -f %s' % TAR_PACK_RM)
