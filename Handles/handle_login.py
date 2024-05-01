from Handles.handle_token import handle_token
from wx_users.models import WxUsers

from Constants.code_status import CodeStatus


def handle_customer(token_type: str, token, user_rule: str = 'customer'):
    if (token == "" or token is None or len(token) == 0
            or user_rule == "" or user_rule is None or len(user_rule) == 0
            or token_type == "" or token_type is None or len(token) == 0):
        return {
            'judge': 0,
            'data': CodeStatus().UNKNOWN_OR_MESSING_PARAMETER
        }
    if token_type not in ['access_token', 'refresh_token']:
        return {
            'judge': 0,
            'data': CodeStatus().BasicCommunication().UserArchive().USER_ARCHIVE_NOT_FOUND
        }
    decode_token = handle_token(token, user_rule, token_type)
    if not decode_token['judge']:
        return {
            'judge': 0,
            'code': decode_token['code'],
            'message': decode_token['message']
        }
    try:
        openid = decode_token['openid']
    except KeyError:
        return {
            'judge': 0,
            'data': CodeStatus().TokenCommunication().TokenDetailsStatus().TOKEN_UNKNOWN_ERROR
        }
    try:
        WxUsers.objects.get(openid=openid)
    except WxUsers.DoesNotExist:
        return {
            'judge': 0,
            'data': CodeStatus().BasicCommunication().UserArchive().USER_ARCHIVE_NOT_FOUND
        }
    return {
        'judge': 1,
        'data': CodeStatus().BasicCommunication().UserArchive().USER_ARCHIVE_FOUNDED,
        'openid': openid
    }
