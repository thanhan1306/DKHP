import json
import re
import random
import time
import base64
import concurrent.futures
import csv
import jwt
import asyncio
import aiohttp
import json
import logging
from tabulate import tabulate
from prettytable import PrettyTable
import requests
import pandas as pd
from datetime import datetime, timedelta

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


    def __init__(self, email, username, password, auth, ex, id_mon):
        self.email = email
        self.username = username
        self.password = password
        self.auth = auth
        self.ex = ex
        self.ds_nhom_to = id_mon
        self.idpc = "-7648466455965434478"
        self.ketqua = []
        self.auth = None
        self.ex = None
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
            self.ex = datetime.now() + 2
            self.refresh_token = response["refresh_token"]
            self.idpc = response["idpc"]
            self.name = response["name"]
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
                print(response.json())
                response_data = response.json()
                data = response_data.get("data", {})
                if data.get("is_thanh_cong"):
                    re = data.get("ket_qua_dang_ky", {}).get("ngay_dang_ky", "Không có thông tin ngày đăng ký")
                    print(f"Mail: {self.email} + {id_mon} + {re}")
                    """{'data': {'is_thanh_cong': False, 'thong_bao_loi': 'Cảnh báo: tài khoản của bạn không được đăng ký/hủy đăng ký ở thời điểm hiện tại.', 'is_chung_nhom_mon_hoc': False, 'is_show_nganh_hoc': False, 'ket_qua_dang_ky': {'id_kqdk': '0', 'ngay_dang_ky': '0001-01-01T00:00:00', 'is_da_rut_mon_hoc': False, 'enable_xoa': False, 'hoc_phi_tam_tinh': 0.0, 'id_dia_diem_thi': '0'}}, 'result': True, 'code': 200}
                                    """
                    return data.get("ket_qua_dang_ky", {}).get("ngay_dang_ky", "Không có thông tin ngày đăng ký")
                else:
                    return data.get('thong_bao_loi')

            else:
                print(response.status_code)
                return False
        except Exception as e:
            print(f"Lỗi xảy ra: {e}")
        return False

        """{'data': {'is_thanh_cong': False, 'thong_bao_loi': 'Cảnh báo: tài khoản của bạn không được đăng ký/hủy đăng ký ở thời điểm hiện tại.', 'is_chung_nhom_mon_hoc': False, 'is_show_nganh_hoc': False, 'ket_qua_dang_ky': {'id_kqdk': '0', 'ngay_dang_ky': '0001-01-01T00:00:00', 'is_da_rut_mon_hoc': False, 'enable_xoa': False, 'hoc_phi_tam_tinh': 0.0, 'id_dia_diem_thi': '0'}}, 'result': True, 'code': 200}

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            if response.status_code == 200:
                response_data = response.json()

                print(response_data)
                data = response_data.get("data", {})
                if data.get("is_thanh_cong"):
                    return data.get("ket_qua_dang_ky", {}).get("ngay_dang_ky", "Không có thông tin ngày đăng ký")
                else:
                    return False

            else:
                print(response.status_code)
                return False
        except Exception as e:
            print(f"Lỗi xảy ra: {e}")
        return False"""






"""user1 = User("3122410003", "Angia@1306")
#user1.login()
datas = open_array("ds_mon1.json")
df = pd.DataFrame(datas)
df.to_csv("DS_MON9_12.csv", index=False, encoding='utf-8-sig')"""
"""dsmon = [
{'id_mon': '-9059984572162929148', 'is_thanh_cong': False}
]
user1 = User("3123330021", "lieuan2304", dsmon)
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
            save_array(user1.ds_mon,"ds_mon.json")
            df = pd.DataFrame(user1.ds_mon)
            df.to_csv("DS_MON9_12.csv", index=False, encoding='utf-8-sig')
            save_array(user1.dsnhomto, "ds_nhom_to.json.json")
            df = pd.DataFrame(user1.dsnhomto)
            df.to_csv("DSNHOMTO9_12.csv", index=False, encoding='utf-8-sig')
            print("SUCCESS")
    elif i == "5":
        while True:
            user1.dk()
            print(user1.ds_mon)
    elif i == "0":
        break"""

# Chạy các bước
"""fileu = "User.csv"
filem ="ds_nhom_to_user.csv"
User.doc_file_khach_hang(fileu)
User.hien_thi_ds_user()
User.doc_file_nhom_to(filem)
for user in User.ds_user:
    print(user.email)
    print(user.ds_nhom_to)"""


def doc_file_khach_hang(filem):
    df = pd.read_csv(filem)
    ds_user =[]
    for index, row in df.iterrows():
        user = User(
            row['EMAIL'],
            row['USERNAME'],
            row['PASSWORD'],
            row['AUTH'],
            row['EX'],
            row['id_mon']
        )
        # Giả sử bạn có cách để phân bổ môn học (ds_nhom_to)
        user.ds_nhom_to = eval(row['id_mon'])  # Chuyển đổi chuỗi thành list (nếu cần)
        ds_user.append(user)
    return ds_user
"""filem ="User - Copy.csv"
df = pd.read_csv(filem)
ds = doc_file_khach_hang(filem)
for user in ds:
    user.login()
    print(user.email)
    print(user.ds_nhom_to)
    for mon in user.ds_nhom_to:
        user.xulydkmhsinhvien(mon)
"""


def process_users():
    filem = "User - Copy.csv"
    ds = doc_file_khach_hang(filem)
    ket_qua_tat_ca = []  # Danh sách lưu kết quả của tất cả user
    successful_users = []  # Danh sách lưu user thành công

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []

        # Đăng nhập cho mỗi user trước
        for user in ds:
            futures.append(executor.submit(user.login))

        # Chờ login xong cho tất cả người dùng
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                if result:
                    print(f"Login thành công cho {user.email}")
                else:
                    print(f"Login thất bại cho {user.email}")
            except Exception as e:
                print(f"Xảy ra lỗi khi login: {e}")

        # Sau khi login thành công, bắt đầu xử lý các môn học
        futures.clear()  # Xóa các futures cũ
        for user in ds:
            for mon in user.ds_nhom_to:
                futures.append(executor.submit(user.xulydkmhsinhvien, mon))

        # Chờ các môn học được xử lý xong
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                if result and result != "Không có thông tin ngày đăng ký":
                    ket_qua_tat_ca.append(result)  # Lưu kết quả vào danh sách
                    # Lưu user thành công nếu môn học đăng ký thành công
                    successful_users.append(user)
            except Exception as e:
                print(f"Xảy ra lỗi khi xử lý môn học: {e}")

    # Lưu kết quả vào file CSV
    df_ketqua = pd.DataFrame(ket_qua_tat_ca, columns=["KetQua"])
    df_ketqua.to_csv("ket_qua.csv", index=False, encoding='utf-8-sig')
    print("Đã lưu kết quả vào file ket_qua.csv")

    # Xóa người dùng đã thành công khỏi file gốc
    remove_successful_users_from_file(filem, successful_users)

def remove_successful_users_from_file(filem, successful_users):
    # Đọc lại file CSV
    df = pd.read_csv(filem)

    # Lọc các user thành công
    successful_emails = {user.email for user in successful_users}

    # Lọc ra những người dùng chưa thành công
    remaining_users = df[~df['EMAIL'].isin(successful_emails)]

    # Lưu lại file CSV với những người dùng chưa thành công
    remaining_users.to_csv(filem, index=False, encoding='utf-8-sig')
    print(f"Đã xóa các người dùng thành công khỏi {filem}.")

if __name__ == "__main__":
    process_users()




