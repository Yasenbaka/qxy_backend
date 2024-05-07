# 定义失败状态码的偏移量
STATUS_SEC_FAILURE_OFFSET: int = 1000
STATUS_THIRD_FAILURE_OFFSET: int = 10


def failure_status(success_status):
    return success_status[0] + STATUS_THIRD_FAILURE_OFFSET, f'{success_status[1].replace("成功", "失败")}'


class CodeStatus:
    UNKNOWN_OR_MESSING_PARAMETER = 90000, '未知或缺少必要参数！'

    class BasicCommunication:
        class FaBBasicCommunication:
            STATUS_FIR = 10000
            STATUS_SEC = 000

            ALL_VIEW_ASSETS_SUCCESS = 0 + STATUS_FIR + STATUS_SEC, '获取全部界面资源成功'
            ALL_VIEW_THEME_ASSETS_SUCCESS = 1 + STATUS_FIR + STATUS_SEC, '获取界面主题资源成功'
            ALL_VIEW_COLOR_SUCCESS = 2 + STATUS_FIR + STATUS_SEC, '获取界面配色参数成功'

            ALL_VIEW_ASSETS_FAILURE = failure_status(ALL_VIEW_ASSETS_SUCCESS)
            ALL_VIEW_THEME_ASSETS_FAILURE = failure_status(ALL_VIEW_THEME_ASSETS_SUCCESS)
            ALL_VIEW_COLOR_FAILURE = failure_status(ALL_VIEW_COLOR_SUCCESS)

            MISSING_KEY = 3 + STATUS_FIR + STATUS_SEC, '缺少必要的键'
            MISSING_VALUE = 4 + STATUS_FIR + STATUS_SEC, '缺少必要的值或值的类型不正确'

        class UserArchive:
            STATUS_FIR = 10000
            STATUS_SEC = 100
            USER_ARCHIVE_SUCCESS = 0 + STATUS_FIR + STATUS_SEC, '用户信息功能成功'
            USER_ARCHIVE_REGISTER_SUCCESS = 1 + STATUS_FIR + STATUS_SEC, '用户信息注册成功'
            USER_ARCHIVE_LOGIN_SUCCESS = 2 + STATUS_FIR + STATUS_SEC, '用户信息登录成功'
            USER_ARCHIVE_REVISE_SUCCESS = 3 + STATUS_FIR + STATUS_SEC, '用户信息修改成功'
            USER_ARCHIVE_FREEZE_SUCCESS = 4 + STATUS_FIR + STATUS_SEC, '用户信息冻结成功'
            USER_ARCHIVE_REFREEZE_SUCCESS = 5 + STATUS_FIR + STATUS_SEC, '用户信息解冻成功'
            USER_ARCHIVE_DELETE_SUCCESS = 6 + STATUS_FIR + STATUS_SEC, '用户信息注销成功'
            USER_ARCHIVE_NOT_FOUND = 7 + STATUS_FIR + STATUS_SEC, '用户信息无法找到'
            USER_ARCHIVE_FOUNDED = 8 + STATUS_FIR + STATUS_SEC, '用户信息成功找到'

            USER_ARCHIVE_FAILURE = failure_status(USER_ARCHIVE_SUCCESS)
            USER_ARCHIVE_REGISTER_FAILURE = failure_status(USER_ARCHIVE_REGISTER_SUCCESS)
            USER_ARCHIVE_LOGIN_FAILURE = failure_status(USER_ARCHIVE_LOGIN_SUCCESS)
            USER_ARCHIVE_REVISE_FAILURE = failure_status(USER_ARCHIVE_REVISE_SUCCESS)
            USER_ARCHIVE_FREEZE_FAILURE = failure_status(USER_ARCHIVE_FREEZE_SUCCESS)
            USER_ARCHIVE_REFREEZE_FAILURE = failure_status(USER_ARCHIVE_REFREEZE_SUCCESS)
            USER_ARCHIVE_DELETE_FAILURE = failure_status(USER_ARCHIVE_DELETE_SUCCESS)
            USER_ARCHIVE_NOT_FOUND_FAILURE = failure_status(USER_ARCHIVE_NOT_FOUND)
            USER_ARCHIVE_FOUNDED_FAILURE = failure_status(USER_ARCHIVE_FOUNDED)

            USER_COUPON_SUCCESS_GET = 20 + STATUS_FIR + STATUS_SEC, '用户优惠券获取成功'
            USER_COUPON_SUCCESS_DELETE = 21 + STATUS_FIR + STATUS_SEC, '用户优惠券删除成功'
            USER_CART_SUCCESS_ADD = 22 + STATUS_FIR + STATUS_SEC, '用户购物车添加成功'
            USER_CART_SUCCESS_DELETE = 23 + STATUS_FIR + STATUS_SEC, '用户购物车删除成功'
            USER_ORDER_CREATE_SUCCESS = 24 + STATUS_FIR + STATUS_SEC, '用户订单创建成功'
            USER_ORDER_DELETE_SUCCESS = 25 + STATUS_FIR + STATUS_SEC, '用户订单删除成功'
            USER_PAYMENT_SUCCESS = 26 + STATUS_FIR + STATUS_SEC, '用户付款成功'
            USER_ORDER_SEARCH_SUCCESS_BUT_NO_ITEM = 27 + STATUS_FIR + STATUS_SEC, '用户订单获取成功，但没有订单'
            USER_ORDER_SEARCH_SUCCESS = 28 + STATUS_FIR + STATUS_SEC, '用户订单获取成功'
            USER_CART_SUCCESS_FOUND = 29 + STATUS_FIR + STATUS_SEC, '用户购物车成功检索'

            USER_COUPON_FAILURE_GET = failure_status(USER_COUPON_SUCCESS_GET)
            USER_COUPON_FAILURE_DELETE = failure_status(USER_COUPON_SUCCESS_DELETE)
            USER_CART_FAILURE_ADD = failure_status(USER_CART_SUCCESS_ADD)
            USER_CART_FAILURE_DELETE = failure_status(USER_CART_SUCCESS_DELETE)
            USER_ORDER_CREATE_FAILURE = failure_status(USER_ORDER_CREATE_SUCCESS)
            USER_ORDER_DELETE_FAILURE = failure_status(USER_ORDER_DELETE_SUCCESS)
            USER_PAYMENT_FAILURE = failure_status(USER_PAYMENT_SUCCESS)
            USER_ORDER_SEARCH_FAILURE_BUT_NO_ITEM = failure_status(USER_ORDER_SEARCH_SUCCESS_BUT_NO_ITEM)
            USER_ORDER_SEARCH_FAILURE = failure_status(USER_ORDER_SEARCH_SUCCESS)
            USER_CART_FAILURE_FOUND = failure_status(USER_CART_SUCCESS_FOUND)

            USER_APPLICATION_REFUND_SUCCESS = 40 + STATUS_FIR + STATUS_SEC, '用户申请退款成功'
            USER_REVOKE_REFUND_SUCCESS = 41 + STATUS_FIR + STATUS_SEC, '用户撤销退款成功'
            USER_APPLICATION_EXCHANGE_COMMODITY_SUCCESS = 42 + STATUS_FIR + STATUS_SEC, '用户申请换货成功'
            USER_REVOKE_EXCHANGE_COMMODITY_SUCCESS = 43 + STATUS_FIR + STATUS_SEC, '用户撤销换货成功'
            USER_APPLICATION_SERVICE_SUCCESS = 44 + STATUS_FIR + STATUS_SEC, '用户申请售后介入成功'
            USER_REVOKE_SERVICE_SUCCESS = 45 + STATUS_FIR + STATUS_SEC, '用户撤销售后介入成功'
            USER_CONFIRM_RECEIPT_SUCCESS = 46 + STATUS_FIR + STATUS_SEC, '用户确认收货成功'

            USER_APPLICATION_REFUND_FAILURE = failure_status(USER_APPLICATION_REFUND_SUCCESS)
            USER_REVOKE_REFUND_FAILURE = failure_status(USER_REVOKE_REFUND_SUCCESS)
            USER_APPLICATION_EXCHANGE_COMMODITY_FAILURE = failure_status(USER_APPLICATION_EXCHANGE_COMMODITY_SUCCESS)
            USER_REVOKE_EXCHANGE_COMMODITY_FAILURE = failure_status(USER_REVOKE_EXCHANGE_COMMODITY_SUCCESS)
            USER_APPLICATION_SERVICE_FAILURE = failure_status(USER_APPLICATION_SERVICE_SUCCESS)
            USER_REVOKE_SERVICE_FAILURE = failure_status(USER_REVOKE_SERVICE_SUCCESS)
            USER_CONFIRM_RECEIPT_FAILURE = failure_status(USER_CONFIRM_RECEIPT_SUCCESS)

        class Commodity:
            STATUS_FIR = 10000
            STATUS_SEC = 200
            COM_DETAILS_GET_SUCCESS = 0 + STATUS_FIR + STATUS_SEC, '获取商品详情信息成功'
            COM_LIST_VIEW_DATA_GET_SUCCESS = 1 + STATUS_FIR + STATUS_SEC, '获取商品列表界面数据成功'
            COM_3DMODEL_GET_SUCCESS = 2 + STATUS_FIR + STATUS_SEC, '获取商品3D模型成功'

            COM_DETAILS_GET_FAILURE = failure_status(COM_DETAILS_GET_SUCCESS)
            COM_LIST_VIEW_DATA_GET_FAILURE = failure_status(COM_LIST_VIEW_DATA_GET_SUCCESS)
            COM_3DMODEL_GET_FAILURE = failure_status(COM_3DMODEL_GET_SUCCESS)

    class AdminCommunication:
        class Commodity:
            STATUS_FIR = 20000
            STATUS_SEC = 000
            COM_ADD_SUCCESS = 0 + STATUS_FIR + STATUS_SEC, '商品添加成功'
            COM_CHANGE_SUCCESS = 1 + STATUS_FIR + STATUS_SEC, '商品修改成功'
            COM_DELETE_SUCCESS = 2 + STATUS_FIR + STATUS_SEC, '商品删除成功'

            COM_ADD_FAILURE = failure_status(COM_ADD_SUCCESS)
            COM_CHANGE_FAILURE = failure_status(COM_CHANGE_SUCCESS)
            COM_DELETE_FAILURE = failure_status(COM_DELETE_SUCCESS)

    class TokenCommunication:
        class TokenIssuance:
            STATUS_FIR = 30000
            STATUS_SEC = 000
            TOKEN_ISSUE_SUCCESS = 0 + STATUS_FIR + STATUS_SEC, '令牌签发成功'
            TOKEN_PROVING_SUCCESS = 1 + STATUS_FIR + STATUS_SEC, '令牌验证成功'
            TOKEN_AUTHENTICATION_SUCCESS = 2 + STATUS_FIR + STATUS_SEC, '令牌鉴权成功'
            TOKEN_EXCHANGE_SUCCESS = 3 + STATUS_FIR + STATUS_SEC, '令牌兑换成功'
            TOKEN_ISSUE_FOREVER_SUCCESS = 4 + STATUS_FIR + STATUS_SEC, '令牌终身有效签发成功'

            TOKEN_ISSUE_FAILURE = failure_status(TOKEN_ISSUE_SUCCESS)
            TOKEN_PROVING_FAILURE = failure_status(TOKEN_PROVING_SUCCESS)
            TOKEN_AUTHENTICATION_FAILURE = failure_status(TOKEN_AUTHENTICATION_SUCCESS)
            TOKEN_EXCHANGE_FAILURE = failure_status(TOKEN_EXCHANGE_SUCCESS)
            TOKEN_ISSUE_FOREVER_FAILURE = failure_status(TOKEN_ISSUE_FOREVER_SUCCESS)

        class TokenDetailsStatus:
            STATUS_FIR = 30000
            STATUS_SEC = 100
            TOKEN_EFFECTIVE = 0 + STATUS_FIR + STATUS_SEC, '令牌合法有效！'
            TOKEN_VALUE_ERROR = 1 + STATUS_FIR + STATUS_SEC, '你看看你Token传的什么玩意？'
            TOKEN_EXPIRED_SIGNATURE_ERROR = 2 + STATUS_FIR + STATUS_SEC, '令牌过期！'
            TOKEN_DECODE_ERROR = 3 + STATUS_FIR + STATUS_SEC, '令牌解码失败！'
            TOKEN_INVALID_ERROR = 4 + STATUS_FIR + STATUS_SEC, '令牌非法！'
            TOKEN_UNKNOWN_ERROR = 5 + STATUS_FIR + STATUS_SEC, '令牌严重致命错误！'
            TOKEN_EFFECTIVE_BUT_UNKNOWN_RULE = 6 + STATUS_FIR + STATUS_SEC, '令牌合法，但无法理解令牌规则！'
            TOKEN_MISSING_NECESSARY_VALUE = 7 + STATUS_FIR + STATUS_SEC, '缺少制作令牌的必要值！'
            TOKEN_DESTROY = 8 + STATUS_FIR + STATUS_SEC, '令牌危险！合法但应该销毁！'
            TOKEN_NO_USE = 9 + STATUS_FIR + STATUS_SEC, '该令牌不适配当前使用场景！'
