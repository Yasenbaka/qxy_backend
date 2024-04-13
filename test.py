import time

import jwt

from datetime import timedelta


def get_timedelta():
    time_now = timedelta(days=1)

    print(timedelta(days=1))


class MyJwt(object):
    def __init__(self):
        self.expires_time = 2
        self.key = 'asdasd'
        self.algorithm = 'HS256'

    def encode_token(self, payload):
        payload['exp'] = int(time.time()) + self.expires_time
        print('exp', payload['exp'])
        token = jwt.encode(payload, self.key, algorithm=self.algorithm)
        return token

    def decode_token(self, token):
        print('now time', time.time())
        try:
            print('进入decode方法try')
            pl = jwt.decode(token, self.key, algorithms=[self.algorithm])
            print('deTokenPl', pl)
            exp = int(pl['exp'])
            print(exp)
        except jwt.exceptions.DecodeError as e:
            # 如果令牌无效或签名不匹配，将会抛出DecodeError异常
            print(f"JWT解码失败: {e}")
        except jwt.exceptions.ExpiredSignatureError:
            # 如果令牌已过期，将会抛出ExpiredSignatureError异常
            print("JWT已过期")
        except jwt.exceptions.InvalidTokenError:
            # 如果令牌格式不正确或包含无效声明，将会抛出InvalidTokenError异常
            print("无效的JWT")

        return payload


if __name__ == '__main__':
    get_timedelta()
    # # 用户字典
    # payload = {'user_id': 1, 'username': 'admin'}
    #
    # # 初始化类
    # mj = MyJwt()
    #
    # # 生成token，加密字典
    # token = mj.encode_token(payload)
    # print(f"token: {token}")
    # # 解析token，解析字典
    # time.sleep(5)
    # token += bytes(1)
    # pyload = mj.decode_token(token)
    # print(f"pyload: {pyload}")
