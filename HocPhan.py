import time
import random
import os



import csv
import aiohttp
import asyncio
import json
async def send_to_google_form(id, mail, resu):
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdy1I_tbmyzY_rVJad_ijNwqegeuWCN4BgIVyT0UvtlGzFmGw/formResponse"
    form_payload = {
        'entry.61085827': f"'{str(id)}",
        'entry.1986856884': f'{mail}',
        'entry.1653873326': f'{resu}',
        'entry.1676601180': '4'
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(form_url, data=form_payload) as form_response:
                if form_response.status == 200:
                    print("Đã gửi thành công đến Google Forms.")
                else:
                    print(f"Lỗi khi gửi yêu cầu đến Google Forms: {form_response.status}")
        except Exception as e:
            print(f"Lỗi khi gửi yêu cầu đến Google Forms: {e}")

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

# Các hàm phụ trợ (my_btoa, rnd, sc, ec, gc) giữ nguyên.
# Dưới đây là phần chính liên quan đến `HocPhan` và xử lý bất đồng bộ.

class HocPhan:
    def __init__(self, id_to_hoc, email, auth):
        self.id_to_hoc = id_to_hoc
        self.email = email
        self.auth = auth
        self.is_thanh_cong = False
        self.result = ""

    def thongbao(self):
        if self.is_thanh_cong:
            if "Trùng TKB MH" not in self.result:
                print(f" ================================>>{self.id_to_hoc} + {self.result} + {self.email}")
        """else:
            print(f" {self.id_to_hoc} + {self.result} + {self.email}")"""



    def set_result(self, result):
        self.is_thanh_cong = True
        self.result = result

    async def xulydkmhsinhvien(self, session):
        if self.is_thanh_cong:
            return
        url = "https://thongtindaotao.sgu.edu.vn/dkmh/api/dkmh/w-xulydkmhsinhvien"
        payload = {
            "filter": {
                "id_to_hoc": f"{self.id_to_hoc}",
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
            "Idpc": "-7648466455965434478",
            "Origin": "https://thongtindaotao.sgu.edu.vn",
            "Referer": "https://thongtindaotao.sgu.edu.vn/",
            "host": "thongtindaotao.sgu.edu.vn",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "ua": f"{gc('dkmh/w-xulydkmhsinhvien', -9000)}"
        }

        while not self.is_thanh_cong:
            try:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        data = response_data.get("data", {})
                        if data.get("is_thanh_cong"):
                            self.is_thanh_cong = True
                            self.result = data.get("ket_qua_dang_ky", {}).get("ngay_dang_ky", "Không có thông tin ngày đăng ký")
                            self.thongbao()
                            await send_to_google_form(self.id_to_hoc,self.email,self.result)
                        else:
                            self.result = data.get('thong_bao_loi')
                            if "Trùng TKB MH" in self.result:
                                print(f" {self.id_to_hoc} + {self.result} + {self.email}")
                                self.is_thanh_cong = True
                                await send_to_google_form(self.id_to_hoc, self.email, self.result)

                            self.thongbao()
                    else:
                        self.result = f"Lỗi HTTP: {response.status}"
                        print(self.result + self.email)
            except Exception as e:
                self.result = f"Lỗi xảy ra: {e}"
                print(self.result + self.email)

async def main():
    hoc_phans = []

    # Đọc dữ liệu từ file CSV
    with open('data.csv', mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            hoc_phans.append(HocPhan(id_to_hoc=row['ID_HP'], email=row['EMAIL'], auth=row['auth']))

    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [hp.xulydkmhsinhvien(session) for hp in hoc_phans]
        await asyncio.gather(*tasks)

    for hp in hoc_phans:
        hp.thongbao()

if __name__ == "__main__":
    asyncio.run(main())
# Hàm gửi dữ liệu đến Google Forms

