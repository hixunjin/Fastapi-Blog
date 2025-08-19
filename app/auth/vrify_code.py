import random,string,smtplib,redis
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

#配置Redis连接
r = redis.Redis(host='localhost',port=6379,db=0,decode_responses=True)

#使用 random 生随机验证码,默认为6位
def generate_code(length:int = 6):
    return ''.join(random.choices(string.digits,k=length))



#验证码存储到Redis中
def storage_code_to_redis(email:str,code:str):
    r.setex(f"verify:{email}",600,code)



#发送验证码
def send_code(email:str,code:str):
    """构造待发送邮件"""

    OriginEmail = "2197381455@qq.com"

    subject = "注册验证码"
    content = f"你的验证码是{code},有效时间位10分钟，请点击链接:http://127.0.0.1:8000/activate_user"
    message = MIMEText(content,'plain','utf-8')
    message['subject'] = Header(subject,'utf-8')
    message['Origin'] = OriginEmail
    message['to'] = email
    message['From'] = formataddr(["博客系统", OriginEmail])  # 发件人名称和邮箱

    #尝试构建SMTP服务器，并发送邮件

    try:
        #连接QQ邮箱服务器，端口号为  465
        server = smtplib.SMTP_SSL('smtp.qq.com',465)
        server.login(OriginEmail,'sgcaxewrbunaeadf')

        #发送邮件
        server.sendmail(OriginEmail,[email],message.as_string())
        server.quit()

    except Exception as e:
        raise RuntimeError(f"邮件发送失败:{e}")




#校验用户输入的验证码是否和Redis中的验证码一致，结果返回True/False
def verify_code(email:str,input_code:str)->bool:
    storaged_code = r.get(f"verify:{email}")
    return storaged_code == input_code



















