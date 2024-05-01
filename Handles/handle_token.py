"""
在这个Python方法中，你可以直接处理有关token解码和反馈相关内容！（代码解耦合）
    在handle_token方法中，提供了基础的处理逻辑和匹配逻辑。
使用时，你需要在任意Django应用中引入：
    from Handle.handle_token import *
创始于：2024/04/25 张玺龙 技术开发部 部门经理
修改于：
    2024/04/26 张玺龙 技术开发部 部门经理
    2024/04/27 张玺龙 技术开发部 部门经理
    2024/04/29 张玺龙 技术开发部 部门经理
"""

from django.conf import settings
from Constants.code_status import CodeStatus
import jwt

jwt_key = settings.SIMPLE_JWT['SIGNING_KEY']
jwt_alg = settings.SIMPLE_JWT['ALGORITHM']

token_details = CodeStatus().TokenCommunication().TokenDetailsStatus


def token_no_use():
    return {
        'judge': 0,
        'code': token_details.TOKEN_NO_USE[0],
        'message': token_details.TOKEN_NO_USE[1]
    }


def handle_token(token: str, user_rule: str, token_type: str = None) -> dict:
    if (token is None or len(token) == 0 or token.count('.') != 2 or
            user_rule is None or user_rule == '' or len(user_rule) == 0):
        return {
            'judge': 0,
            'code': token_details.TOKEN_VALUE_ERROR[0],
            'message': token_details.TOKEN_VALUE_ERROR[1]
        }
    try:
        decode_token = jwt.decode(token, jwt_key, algorithms=[jwt_alg])
    except jwt.exceptions.ExpiredSignatureError:
        return {
            'judge': 0,
            'code': token_details.TOKEN_EXPIRED_SIGNATURE_ERROR[0],
            'message': token_details.TOKEN_EXPIRED_SIGNATURE_ERROR[1]
        }
    except jwt.exceptions.DecodeError:
        return {
            'judge': 0,
            'code': token_details.TOKEN_DECODE_ERROR[0],
            'message': token_details.TOKEN_DECODE_ERROR[1]
        }
    except jwt.exceptions.InvalidTokenError:
        return {
            'judge': 0,
            'code': token_details.TOKEN_INVALID_ERROR[0],
            'message': token_details.TOKEN_INVALID_ERROR[1]
        }
    except jwt.PyJWTError:
        return {
            'judge': 0,
            'code': token_details.TOKEN_UNKNOWN_ERROR[0],
            'message': token_details.TOKEN_UNKNOWN_ERROR[1]
        }
    else:
        if user_rule == 'customer':
            try:
                if decode_token['rule'] == user_rule:
                    if token_type is None:
                        return {
                            'judge': 0,
                            'code': token_details.TOKEN_EFFECTIVE_BUT_UNKNOWN_RULE[0],
                            'message': token_details.TOKEN_EFFECTIVE_BUT_UNKNOWN_RULE[1]
                        }
                    if decode_token['type'] == token_type:
                        return {
                            'judge': 1,
                            'code': token_details.TOKEN_EFFECTIVE[0],
                            'message': token_details.TOKEN_EFFECTIVE[1],
                            'openid': decode_token['openid']
                        }
                    if decode_token['type'] == token_type:
                        return {
                            'judge': 1,
                            'message': '刷新令牌合法有效！',
                            'access_token': decode_token['access_token']
                        }
            except KeyError:
                return token_no_use()
            return token_no_use()
        if user_rule == 'admin':
            try:
                if decode_token['rule'] == user_rule:
                    return {
                        'judge': 1,
                        'code': token_details.TOKEN_EFFECTIVE[0],
                        'message': f'超级管理员{token_details.TOKEN_EFFECTIVE[1]}',
                        'account': decode_token['account']
                    }
            except KeyError:
                return token_no_use()
            return token_no_use()
        if user_rule == 'observer':
            try:
                if decode_token['rule'] == user_rule:
                    return {
                        'judge': 1,
                        'code': token_details.TOKEN_EFFECTIVE[0],
                        'message': f'观察者{token_details.TOKEN_EFFECTIVE[1]}',
                        'account': decode_token['account']
                    }
            except KeyError:
                return token_no_use()
            return token_no_use()
        return {
            'judge': 0,
            'message': '令牌没有被正确处理！'
        }
