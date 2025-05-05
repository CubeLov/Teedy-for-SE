# -*- coding: utf-8 -*-
import hashlib
import hmac
import json
import sys
import time
from datetime import datetime
from datetime import timezone
from http.client import HTTPSConnection


def translate_text(text, source_lang="auto", target_lang="zh"):
    """
    调用腾讯云翻译API翻译文本

    参数:
      text: 要翻译的文本内容
      source_lang: 源语言代码，默认为'auto'(自动检测)
      target_lang: 目标语言代码，默认为'zh'(中文)

    返回:
      翻译后的文本字符串
    """
    secret_id = "Your secret id"
    secret_key = "Your secret key"
    token = ""

    service = "tmt"
    host = "tmt.tencentcloudapi.com"
    region = "ap-guangzhou"
    version = "2018-03-21"
    action = "TextTranslate"

    request_data = {
        "SourceText": text,
        "Source": source_lang,
        "Target": target_lang,
        "ProjectId": 0
    }
    payload = json.dumps(request_data)

    # API签名过程
    algorithm = "TC3-HMAC-SHA256"
    timestamp = int(time.time())
    date = datetime.fromtimestamp(timestamp, timezone.utc).strftime("%Y-%m-%d")

    # 步骤 1：拼接规范请求串
    http_request_method = "POST"
    canonical_uri = "/"
    canonical_querystring = ""
    ct = "application/json; charset=utf-8"
    canonical_headers = "content-type:%s\nhost:%s\nx-tc-action:%s\n" % (ct, host, action.lower())
    signed_headers = "content-type;host;x-tc-action"
    hashed_request_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    canonical_request = (http_request_method + "\n" +
                         canonical_uri + "\n" +
                         canonical_querystring + "\n" +
                         canonical_headers + "\n" +
                         signed_headers + "\n" +
                         hashed_request_payload)

    # 步骤 2：拼接待签名字符串
    credential_scope = date + "/" + service + "/" + "tc3_request"
    hashed_canonical_request = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
    string_to_sign = (algorithm + "\n" +
                      str(timestamp) + "\n" +
                      credential_scope + "\n" +
                      hashed_canonical_request)

    # 步骤 3：计算签名
    def sign(key, msg):
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    secret_date = sign(("TC3" + secret_key).encode("utf-8"), date)
    secret_service = sign(secret_date, service)
    secret_signing = sign(secret_service, "tc3_request")
    signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

    # 步骤 4：拼接 Authorization
    authorization = (algorithm + " " +
                     "Credential=" + secret_id + "/" + credential_scope + ", " +
                     "SignedHeaders=" + signed_headers + ", " +
                     "Signature=" + signature)

    # 步骤 5：构造并发起请求
    headers = {
        "Authorization": authorization,
        "Content-Type": "application/json; charset=utf-8",
        "Host": host,
        "X-TC-Action": action,
        "X-TC-Timestamp": str(timestamp),
        "X-TC-Version": version
    }
    if region:
        headers["X-TC-Region"] = region
    if token:
        headers["X-TC-Token"] = token

    try:
        req = HTTPSConnection(host)
        req.request("POST", "/", headers=headers, body=payload.encode("utf-8"))
        resp = req.getresponse()
        response_content = resp.read().decode('utf-8')


        response_json = json.loads(response_content)

        # 提取翻译结果
        if 'Response' in response_json and 'TargetText' in response_json['Response']:
            return response_json['Response']['TargetText']
        else:
            return "翻译失败: " + response_content
    except Exception as err:
        return "错误: " + str(err)

