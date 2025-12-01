import requests

BASE = "http://127.0.0.1:5000/"
# data = [{"likes": 10, "name": "an", "views": 100},
#         {"likes": 8, "name": "tim", "views": 2000},
#         {"likes": 6, "name": "bob", "views": 85},
#         {"likes": 4, "name": "kim", "views": 76},
#         {"likes": 2, "name": "john", "views": 130},
#         {"likes": 9, "name": "jack", "views": 67},
#         {"likes": 5, "name": "rob", "views": 19},
#         {"likes": 3, "name": "ken", "views": 42}]
# for i, item  in enumerate(data):
#     response = requests.put(BASE + "video/" + str(i), json=item)
#     print("Status:", response.status_code)
#     print("Text:", response.text)


response=requests.patch(BASE + "video/2", json={"views":1})
print(response.text)