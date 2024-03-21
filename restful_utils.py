from flask import jsonify

class HttpCode(object):
    ok = 200
    un_auth_error = 401
    params_error = 400
    server_error = 500

def restful_result(code, message, data):
    return jsonify({"code": code, "message": message, "data": data or {}})

def success(message="", data=None):
    """
    正确返回
    :return:
    """
    return restful_result(code=HttpCode.ok, message=message, data=data)