##  pony
鉴于Arukas上搭建的SS Docker总是自动更换IP和端口，遂花了一晚上时间招呼了此脚本。
+ 信息直接使用base64编码为 SS URL，移动端可直接导入
+ PC端可直接使用配置文件同时驾驭10匹小马
## Environments

+ Python 3.5+

![](./screen/webpage.png)

![](./screen/Screenshot.png)

## GettingStarted

---

#### 1. Install dependency 

```
pip install flask
pip install pillow
pip install qrcode
```
If you just want to try ths, just run 

```
python update.py
python app.py
```

#### 2. Deploy 

```
sudo apt install nginx
pip3 install gunicorn
```

```
#/etc/nginx/site-avalidable/default
server {
    listen 8080;
    server_name ss.hakale.cn;
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
  }

```
#### 3. Run
```shell
gunicorn app:app -D
```
