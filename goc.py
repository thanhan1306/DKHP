import json
import re
import random
import time
import base64
import requests
import pandas as pd

def open_array(filename):
  try:
    with open(filename, 'r', encoding='utf-8') as f:
      noi_dung = f.read()
      array = json.loads(noi_dung)
      return array
  except FileNotFoundError:
    print("Không tìm thấy file.")
    return None
  except json.JSONDecodeError:
    print("Lỗi giải mã JSON.")
    return None

def save_array(array, filename):
  with open(filename, 'w', encoding='utf-8') as f:
    json.dump(array, f, indent=4)

def my_btoa(s):
    # Bước 1: Chuyển chuỗi thành mảng byte
    bytes_data = [ord(c) for c in s]

    # Bước 2: Mã hóa Base64
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    base64_result = ''

    # Mã hóa base64 theo từng bộ 3 byte
    for i in range(0, len(bytes_data), 3):
        byte1 = bytes_data[i]
        byte2 = bytes_data[i + 1] if i + 1 < len(bytes_data) else 0
        byte3 = bytes_data[i + 2] if i + 2 < len(bytes_data) else 0

        base64_result += chars[byte1 >> 2]
        base64_result += chars[((byte1 & 3) << 4) | (byte2 >> 4)]
        base64_result += chars[((byte2 & 15) << 2) | (byte3 >> 6)]
        base64_result += chars[byte3 & 63]

    # Bước 3: Thêm dấu "=" nếu cần thiết (nếu độ dài không chia hết cho 3)
    if len(bytes_data) % 3 == 1:
        base64_result = base64_result[:-2] + '=='
    elif len(bytes_data) % 3 == 2:
        base64_result = base64_result[:-1] + '='

    return base64_result

def rnd(num):
    return random.randint(1, num)

def sc():
    return [
               58, 43, 197, 133, 4, 165, 110, 3, 44, 202, 186, 28, 118, 177, 32, 94,
               219, 6, 199, 27, 101, 191, 66, 115, 234, 120, 10, 236, 104, 108, 74, 247,
               68, 198, 62, 203, 17, 102, 185, 42
           ][-36:][:32]  # Cắt mảng như JS

# Hàm mã hóa tương tự JS (ec function)
def ec(str, key):
    # Chuyển đổi hàm `rk` và `sc` theo Python
    def rk(key):
        P = [4, 165, 110, 3, 44, 202, 186, 28, 118, 177, 32, 94, 219, 6, 199, 27, 101, 191, 66, 115, 234, 120, 10, 236, 104, 108, 74, 247, 68, 198, 62, 203]
        Q = key % 3 + 1
        return [P[(key + T * Q) % len(P)] for T in range(10)]

    # Phần chính của hàm ec
    Q = rk(key)[::-1]
    #print("K")
    #print(sc())
    R = [ord(c) for c in str]
    T = []
    while len(T) < len(R):
        T.extend(Q)
    return [U ^ T[V] for V, U in enumerate(R)]

# Hàm chính `gc` giống JS
def gc(P, k):
    # Cắt P nếu dài hơn 22 ký tự
    if len(P) > 22:
        P = P[:22]

    P = P.upper()  # Chuyển P thành chữ hoa giống JS
    #print(P)
    # Tính toán giá trị Q như trong JS
    offset = k
    current_time_millis = int(time.time() * 1000)  # Đảm bảo tính theo mili giây
    #print(current_time_millis)
    Q = str(rnd(89) + 10) + str(current_time_millis - offset) + str(rnd(89) + 10) + P
    #print(Q)
    R = rnd(31)
    #print(R)

    # Tạo mảng T như trong JS
    T = [R + 32] + ec(Q, R)
    #print(T)
    T = ''.join([chr(U) for U in T])
    #print(T)

    # Mã hóa Base64
    return my_btoa(T.encode('utf-8').decode("utf-8"))


class User:
    def __init__(self, username, password, ds_mon = []):
        self.username = username
        self.password = password
        self.ds_mon = ds_mon
        self.ketqua = []
        self.auth = None
        self.offset = -2132

    def login(self):
        url = "https://thongtindaotao.sgu.edu.vn/api/auth/login"
        payload = f"username={self.username}&password={self.password}&grant_type=password"
        # Headers
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "vi,en-US;q=0.9,en;q=0.8,en-GB;q=0.7",
            "Content-length" : "59",
            "Content-Type": "text/plain",
            "Idpc": "0",
            "Origin": "https://thongtindaotao.sgu.edu.vn",
            "Referer": "https://thongtindaotao.sgu.edu.vn/",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "ua": f"{gc("auth/login", self.offset)}",
      }

        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            response = response.json()
            self.auth = "bearer " + response["access_token"]
            self.refresh_token = response["refresh_token"]
            self.idpc = response["idpc"]
            self.name = response["name"]
            return True
        return False

    def lockqsv(self):
        url = "https://thongtindaotao.sgu.edu.vn/dkmh/api/sms/w-locketquaduyetsinhvien"
        payload = '{"ma_sv":"' + self.username + '"}'
        # Headers
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "vi,en-US;q=0.9,en;q=0.8,en-GB;q=0.7",
            "Authorization" : self.auth,
            "Content-length": "22",
            "Content-Type": "application/json",
            "Idpc": f"{self.idpc}",
            "Origin": "https://thongtindaotao.sgu.edu.vn",
            "Referer": "https://thongtindaotao.sgu.edu.vn/",
            "sec-ch-ua": '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "ua": f"{gc("sms/w-locketquaduyetsinhvien", self.offset)}",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        }

        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            response = response.json()
            self.code = response["code"]
            return response["code"]
        return None

    def locdkloc(self):
        url = "https://thongtindaotao.sgu.edu.vn/dkmh/api/dkmh/w-locdsdieukienloc"
        payload = ''
        # Headers
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "vi,en-US;q=0.9,en;q=0.8,en-GB;q=0.7",
            "Authorization": self.auth,
            "Content-length": "0",
            "Content-Type": "text/plain",
            "Idpc": f"{self.idpc}",
            "Origin": "https://thongtindaotao.sgu.edu.vn",
            "Referer": "https://thongtindaotao.sgu.edu.vn/",
            "sec-ch-ua": '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "ua": f"{gc("dkmh/w-locdsdieukienloc", self.offset)}",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        }

        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            self.locmon = response.json()
            return True
        return False

    def locdsnhomto(self):
        url = "https://thongtindaotao.sgu.edu.vn/dkmh/api/dkmh/w-locdsnhomto"
        payload = '{"is_CVHT":false,"additional":{"paging":{"limit":99999,"page":1},"ordering":[{"name":"","order_type":""}]}}'
        # Headers
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "vi,en-US;q=0.9,en;q=0.8,en-GB;q=0.7",
            "Authorization": self.auth,
            "Content-length": "107",
            "Content-Type": "application/json",
            "Idpc": f"{self.idpc}",
            "Origin": "https://thongtindaotao.sgu.edu.vn",
            "Referer": "https://thongtindaotao.sgu.edu.vn/",
            "sec-ch-ua": '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "ua": f"{gc("dkmh/w-locdsnhomto", self.offset)}",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        }

        response = requests.post(url, headers=headers, data=payload)
        if response.status_code == 200:
            response = response.json()
            self.dsnhomto = response["data"]['ds_nhom_to']
            self.ds_mon = response["data"]['ds_mon_hoc']
            self.dskhoa = response["data"]['ds_khoa']
            return True
        return False

    def xulydkmhsinhvien(self, id_mon):
        url = "https://thongtindaotao.sgu.edu.vn/dkmh/api/dkmh/w-xulydkmhsinhvien"
        payload = {
            "filter": {
                "id_to_hoc": f"{id_mon}",
                "is_checked": True,
                "sv_nganh": 1
            }
        }

        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "vi,en-US;q=0.9,en;q=0.8,en-GB;q=0.7",
            "Connection": "keep-alive",
            "Authorization": self.auth,
            "Content-Type": "application/json",
            "Idpc": f"{self.idpc}",
            "Origin": "https://thongtindaotao.sgu.edu.vn",
            "Referer": "https://thongtindaotao.sgu.edu.vn/",
            "host": "thongtindaotao.sgu.edu.vn",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "ua": f"{gc('dkmh/w-xulydkmhsinhvien', self.offset)}"
        }

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                response_data = response.json()
                data = response_data.get("data", {})
                if data.get("is_thanh_cong"):
                    """{'data': {'is_thanh_cong': False, 'thong_bao_loi': 'Cảnh báo: tài khoản của bạn không được đăng ký/hủy đăng ký ở thời điểm hiện tại.', 'is_chung_nhom_mon_hoc': False, 'is_show_nganh_hoc': False, 'ket_qua_dang_ky': {'id_kqdk': '0', 'ngay_dang_ky': '0001-01-01T00:00:00', 'is_da_rut_mon_hoc': False, 'enable_xoa': False, 'hoc_phi_tam_tinh': 0.0, 'id_dia_diem_thi': '0'}}, 'result': True, 'code': 200}
                                    """
                    return data.get("ket_qua_dang_ky", {}).get("ngay_dang_ky", "Không có thông tin ngày đăng ký")
                else:
                    return False

            else:
                print(response.status_code)
                return False
        except Exception as e:
            print(f"Lỗi xảy ra: {e}")
        return False

    def getdsmon(self):
        if self.auth is not None:
            if self.lockqsv():
                if self.locdkloc():
                    if self.locdsnhomto():
                        return self.dsnhomto
                    else:
                        print("Lỗi lấy ds môn!")
                else:
                    print("Lỗi lấy dk lọc!")
            else:
                print("Lỗi duyệt sinh viên!")
        else:
            print("Lỗi token trống!")
        return None

    def timmon(self):
        if self.dsnhomto is not None:
            for i in self.dsnhomto:
                if i['id_to_hoc'] == "-8187864983186726526":
                    return i['sl_cl']

    def dk(self):
        for i in self.ds_mon:
            if i['is_thanh_cong'] == False:
                check = self.xulydkmhsinhvien(i['id_mon'])
                print(check)
                if check != False:
                    i['is_thanh_cong'] = check





"""user1 = User("3122410003", "Angia@1306")
#user1.login()
datas = open_array("ds_mon1.json")
df = pd.DataFrame(datas)
df.to_csv("DS_MON9_12.csv", index=False, encoding='utf-8-sig')"""
dsmon = [
{'id_mon': '-9059984572162929148', 'is_thanh_cong': False}
]
user1 = User("3122410003", "Angia@1306")
"""user2 = User("3122410003", "Angia@1306")
user2.login()
user2.locdsnhomto()
print(user2.auth)
user2.xulydkmhsinhvien("-5799348462041320401")"""
while True:
    i = input("Nhap lua chon:")
    if i == "1":
        if user1.login():
            print("SUCCESS")
    elif i == "2":
        if user1.lockqsv():
            print("SUCCESS")
    elif i == "3":
        if user1.locdkloc():
            print("SUCCESS")
    elif i == "4":
        if user1.locdsnhomto():
            save_array(user1.ds_mon,"ds_mon18_12_24.json")
            df = pd.DataFrame(user1.ds_mon)
            df.to_csv("DS_MON9_12.csv", index=False, encoding='utf-8-sig')

            save_array(user1.dsnhomto, "ds_nhom_to18_12_24.json")
            df = pd.DataFrame(user1.dsnhomto)
            df.to_csv("DSNHOMTO18_12_24.csv", index=False, encoding='utf-8-sig')
            print("SUCCESS")
    elif i == "5":
        while True:
            user1.dk()
            print(user1.ds_mon)
    elif i == "0":
        break