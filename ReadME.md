# 基于Flask和Vue的前后端分离Web后台管理系统

后端使用Flask提供HTTP API，前端则基于 vueAdmin-template 模板二次开发。

# 开发环境

- Windows 10 x64
- IDE：VSCode
- Python 3.5.4
    - Flask==0.12.2
- NodeJS v6.9.5
- NPM 5.6.0

# 启动服务

## 后端

Windows PowerShell：

1. 安装虚拟环境

```
PS > cd backend
PS > python3 -m venv .venv
(venv) PS > pip3 install -r requirements.txt
```
2. 创建数据库和管理员

```sh
(venv) > python manage.py db_createfirst
drop the database?[y/n]: n
The database is created successfully!
Please Enter the superuser username:admin
Password:admin
Confirm password:admin
Superuser is created successfully!
```

3. 启动服务器

```sh
(venv) > python manage.py runserver
```

更多内容参见 `backend/ReadME.md`。

## 前端

Windows PowerShell：

```
cd frontend-admin

# 安装依赖包
npm install
# 建议不要用cnpm  安装有各种诡异的bug 可以通过如下操作解决npm速度慢的问题
npm install --registry=https://registry.npm.taobao.org

# 运行服务：localhost:9528
npm run dev
```

更多内容参见 `fromtend-admin/ReadME.md`。

