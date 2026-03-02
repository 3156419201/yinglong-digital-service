import os
import hashlib
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup

# 配置 QQ 邮箱 SMTP
QQ_EMAIL = "3156419201@qq.com"
QQ_AUTH_CODE = os.getenv("QQ_AUTH_CODE", "")  # QQ 邮箱授权码
RECEIVE_EMAIL = "3156419201@qq.com"

def send_email_notification(subject, body):
    """发送邮件通知"""
    try:
        msg = MIMEMultipart()
        msg['From'] = QQ_EMAIL
        msg['To'] = RECEIVE_EMAIL
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # 连接 QQ 邮箱 SMTP 服务器
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        server.login(QQ_EMAIL, QQ_AUTH_CODE)
        server.sendmail(QQ_EMAIL, RECEIVE_EMAIL, msg.as_string())
        server.quit()
        
        print(f"[邮件已发送] 发送到: {RECEIVE_EMAIL}")
        return True
    except Exception as e:
        print(f"[邮件发送失败] {e}")
        return False

def monitor_crac_qinghai():
    """监测 CRAC 网站青海省报名信息"""
    url = "http://www.crac.org.cn/"
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; Bot/1.0)"}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')
        
        # 移除脚本和样式标签
        for s in soup(["script", "style", "noscript"]):
            s.extract()
        
        text = soup.get_text(separator=" ", strip=True)
        
        # 计算当前页面的哈希值
        current_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
        
        # 读取上次保存的哈希值
        hash_file = "last_hash_qinghai.txt"
        last_hash = ""
        
        if os.path.exists(hash_file):
            with open(hash_file, "r", encoding="utf-8") as f:
                last_hash = f.read().strip()
        
        # 检查关键词：报名、青海
        keywords = ["报名", "青海"]
        keyword_found = any(k in text for k in keywords)
        
        # 检测页面是否有变化且包含关键词
        if current_hash != last_hash and keyword_found:
            print(f"[检测到变化] 页面内容有更新，且包含青海报名相关信息")
            snippet = text[:800].replace("\n", " ")
            
            subject = "CRAC 青海省报名通知 - 页面有更新"
            body = f"检测到 CRAC 网站 (http://www.crac.org.cn/) 青海省报名相关页面有更新。\n\n页面摘要:\n{snippet}\n\n请及时查看网站了解详情。"
            
            send_email_notification(subject, body)
        else:
            print(f"[无新变化] 页面内容未变或未发现青海报名信息")
        
        # 保存当前哈希值以供下次比较
        with open(hash_file, "w", encoding="utf-8") as f:
            f.write(current_hash)
            
    except Exception as e:
        print(f"[错误] 监测失败: {e}")

if __name__ == "__main__":
    monitor_crac_qinghai()