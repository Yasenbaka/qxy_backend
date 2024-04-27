import json

a = {"data": [{"count": "2", "price": "80", "coupon": "null", "commodity": "2024", "order_unique_id": 1714230940}]}

# 使用列表推导式来过滤掉id等于13的项
a['data'] = [item for item in a['data'] if item['order_unique_id'] != 1714230940]

print(a)

