import json
import time
import random
from datetime import datetime, timedelta

import aiohttp
import asyncio
import logging


async def chuyennhomdhsp(id_to_hoc, mail, auth):
    url = "https://dkhpapi.hcmue.edu.vn/api/Regist/RegistScheduleStudyUnit?TurnID=27&Action=CHANGE&StudyProgramID=K487140202&RegistType=KH"
    payload = '[{"CurriculumID":"' + id_to_hoc + '","ScheduleStudyUnitAlias":"PRIM170601","CurriculumName":"Phát triển chương trình Tiểu học","StudyUnitID":"2421PRIM1706","TypeName":"Lý thuyết","Credits":0,"StudentQuotas":"10-50","StudyUnitTypeID":1,"MaxStudentNumber":null,"NumberOfStudents":48,"Schedules":" Thứ Hai, Tiết(7 - 10), A.413, ADV<br/> (10/02/2025 -> 12/05/2025)<br/> , Thứ Hai, Tiết(7 - 10), Online, ADV<br/> (10/02/2025 -> 12/05/2025)<br/> , Thứ Hai, Tiết(7 - 8), A.413, ADV<br/> (10/02/2025 -> 12/05/2025)<br/> ","ProfessorName":" Hồ Ngọc Khải","IsRegisted":false,"ListOfClassStudentID":"48.01.GDTH.A","NumberOfChilds":0,"FeeDebt":"","ParentID":"","UpdateDate":"12/05/2024 11:12:32","NumberRegistOfEmpty":"3","IsHocTrucTuyen":null,"isOpen":true,"isOpenChilrentTask":false}]'
    payload = json.loads(payload)
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Authorization": auth,
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://dkhpapi.hcmue.edu.vn",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, như Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "content-length": "802"
    }
    async with aiohttp.ClientSession() as session:
        for attempt in range(3):
            try:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        print(response)
                        data = response_data.get("message", {})
                        print(data)
                    else:
                        print(f"Lỗi http {mail}: {response.status}")
                        print(response)
            except Exception as e:
                print(f"Lỗi xảy ra -n{mail}: {e}")
            await asyncio.sleep(2)

async def send_to_google_form(id, id_to_hoc, result, status):
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLScPSvuYFFJkqthsQN8nGmdi-hQOQU_2qQ98EkQPGb4TuG7QfA/formResponse"

    form_payload = {
        'entry.31662442': f"{str(id)}",
        'entry.955688115': f"{str(id_to_hoc)}",
        'entry.963488546': f'{status}',
        'entry.645101552': f'{result}',
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(form_url, data=form_payload) as form_response:
                if form_response.status == 200:
                    if status == "Thành công!":
                        print(f"Lenh: {id} đăng ký thành công {id} lúc {result}!")
                    elif status == "Trùng lịch!":
                        print(f"Lenh: {id} bị trùng lịch {result}!")
                    else:
                        print(f"Lenh: {id} hết slot {result}!")
                else:
                    print(f"Lỗi khi gửi yêu cầu đến Google Forms: {form_response.status}")
        except Exception as e:
            print(f"Lỗi khi gửi yêu cầu đến Google Forms: {e}")


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def my_btoa(s):
    bytes_data = [ord(c) for c in s]
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    base64_result = ''
    for i in range(0, len(bytes_data), 3):
        byte1 = bytes_data[i]
        byte2 = bytes_data[i + 1] if i + 1 < len(bytes_data) else 0
        byte3 = bytes_data[i + 2] if i + 2 < len(bytes_data) else 0
        base64_result += chars[byte1 >> 2]
        base64_result += chars[((byte1 & 3) << 4) | (byte2 >> 4)]
        base64_result += chars[((byte2 & 15) << 2) | (byte3 >> 6)]
        base64_result += chars[byte3 & 63]
    if len(bytes_data) % 3 == 1:
        base64_result = base64_result[:-2] + '=='
    elif len(bytes_data) % 3 == 2:
        base64_result = base64_result[:-1] + '='
    return base64_result

def rnd(num):
    return random.randint(1, num)

def ec(str, key):
    def rk(key):
        P = [4, 165, 110, 3, 44, 202, 186, 28, 118, 177, 32, 94, 219, 6, 199, 27, 101, 191, 66, 115, 234, 120, 10, 236, 104, 108, 74, 247, 68, 198, 62, 203]
        Q = key % 3 + 1
        return [P[(key + T * Q) % len(P)] for T in range(10)]
    Q = rk(key)[::-1]
    R = [ord(c) for c in str]
    T = []
    while len(T) < len(R):
        T.extend(Q)
    return [U ^ T[V] for V, U in enumerate(R)]

def gc(P, k):
    if len(P) > 22:
        P = P[:22]
    P = P.upper()
    offset = k
    current_time_millis = int(time.time() * 1000)
    Q = str(rnd(89) + 10) + str(current_time_millis - offset) + str(rnd(89) + 10) + P
    R = rnd(31)
    T = [R + 32] + ec(Q, R)
    T = ''.join([chr(U) for U in T])
    return my_btoa(T.encode('utf-8').decode("utf-8"))

class HocPhan:
    def __init__(self, id_to_hoc, id, auth, username = None, password = None):
        self.id_to_hoc = id_to_hoc
        self.id = id
        self.auth = auth
        self.username = username
        self.password = password
        self.ex = datetime.now() + timedelta(hours=1.5)
        self.is_thanh_cong = False
        self.result = ""

    def thongbao(self):
        if self.is_thanh_cong and "Trùng TKB MH" not in self.result:
            logging.info(f"Thành công: {self.id_to_hoc} - {self.result} - {self.id}")
        else:
            logging.warning(f"Không thành công: {self.id_to_hoc} - {self.result} - {self.id}")

    async def xulydkmhsinhvien(self, session):
        if self.is_thanh_cong:
            return
        url = "https://thongtindaotao.sgu.edu.vn/dkmh/api/dkmh/w-xulydkmhsinhvien"
        payload = {
            "filter": {
                "id_to_hoc": "-"+self.id_to_hoc,
                "is_checked": True,
                "sv_nganh": 1
            }
        }
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Authorization": self.auth,
            "Content-Type": "application/json",
            "ua": f"{gc('dkmh/w-xulydkmhsinhvien', -2132)}"
        }
        for attempt in range(3):
            try:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        data = response_data.get("data", {})
                        if data.get("is_thanh_cong"):
                            self.is_thanh_cong = True
                            self.result = data.get("ket_qua_dang_ky", {}).get("ngay_dang_ky", "Không có thông tin ngày đăng ký")
                            await send_to_google_form(self.id, self.id_to_hoc, self.result[:19], "Thành công!")
                            return
                        else:
                            self.result = data.get('thong_bao_loi', "Lỗi không xác định")
                            if "Trùng TKB MH" in self.result:
                                print(f" {self.id_to_hoc} + {self.result} + {self.id}")
                                self.is_thanh_cong = True
                                await send_to_google_form(self.id, self.id_to_hoc, self.result[4:34], "Trùng lịch!")
                            """if "Vui lòng" in self.result:
                                print(f" {self.id_to_hoc} + {self.result} + {self.id}")
                                await send_to_google_form(self.id, self.id_to_hoc, self.result, "Hết slot!")"""
                    elif response.status == 401:
                        print(f"{self.username} het han auth!")
                    else:
                        self.result = f"Lỗi HTTP: {response.status}"
            except Exception as e:
                self.result = f"Lỗi xảy ra: {e}"
            await asyncio.sleep(2)
        self.thongbao()

    async def login(self, session):
        if self.is_thanh_cong:
            return
        url = "https://thongtindaotao.sgu.edu.vn/api/auth/login"
        payload = {
            "username": self.username,
            "password": self.password,
            "grant_type": "password"
        }
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/x-www-form-urlencoded",
            "ua": f"{gc('auth/login', -2132)}"
        }
        for attempt in range(3):
            try:
                async with session.post(url, headers=headers, data=payload) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        self.auth = "bearer " + response_data["access_token"]
                        self.ex = datetime.now() + timedelta(hours=1.5)
                        print(f"{self.username}: Login Successful!")
                    else:
                        self.result = f"Lỗi HTTP login: {response.status}"
            except Exception as e:
                self.result = f"Lỗi xảy ra: {e}"
            await asyncio.sleep(2)
        self.thongbao()

    async def RegistSchedule(self, session):
        if self.is_thanh_cong:
            return
        url = "https://dkhpapi.hcmue.edu.vn/api/Regist/RegistScheduleStudyUnit?TurnID=51&Action=REGIST&StudyProgramID=K507420203&RegistType=KH"
        #url = "https://dkhpapi.hcmue.edu.vn/api/Regist/GetAllScheduleUnitAllowRegist"
        payload = [
            {
                "CurriculumID": self.id_to_hoc,
                "ScheduleStudyUnitAlias":self.id_to_hoc[4:],
                "CurriculumName":"Phương pháp học tập hiệu quả",
                "StudyUnitID":self.id_to_hoc[:12],
                "TypeName":"Lý thuyết",
                "Credits":0,
                "StudentQuotas":"15-50",
                "StudyUnitTypeID":1,
                "MaxStudentNumber": None,
                "NumberOfStudents":49,
                "Schedules":" Thứ Tư, Tiết(1 - 3), B.109, ADV<br/> (12/02/2025 -> 16/04/2025)<br/> , Thứ Tư, Tiết(1 - 3), Online, ADV<br/> (12/02/2025 -> 16/04/2025)<br/> ",
                "ProfessorName":" Đặng Ánh Hồng",
                "IsRegisted":False,
                "ListOfClassStudentID":"",
                "NumberOfChilds":0,
                "FeeDebt":"","ParentID":"",
                "UpdateDate":"12/20/2024 08:47:38",
                "NumberRegistOfEmpty":"1",
                "IsHocTrucTuyen":None,
                "isOpen": True,
                "isOpenChilrentTask":False
            }
        ]
        #payload = {"ReqParam1":"K507420203","ReqParam2":"KH","ReqParam3":"2421EDUC2801"}
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Authorization": self.auth,
            "Content-Type": "application/json",
            "Origin" : "https://dkhp.hcmue.edu.vn",
            "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
        }
        for attempt in range(3):
            try:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        print(response_data)
                        print(response)
                    elif response.status == 400:
                        response_data = await response.json()
                        print(response_data.get("message"," Khong co tin nhan"))
                    else:
                        print(f"Lỗi HTTP: {response.status}")
            except Exception as e:
                print(f"Lỗi xảy ra: {e}")
            await asyncio.sleep(2)




async def main():
    processed_ids = set()  # Lưu các `id_to_hoc` đã xử lý thành công
    while True:
        hoc_phans = []
        #hoc_phans = [HocPhan("2421PRIM170602","BE NGUYEN","bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJJZCI6IjQ4LjAxLjkwMS4xNTUiLCJOYW1lIjoiVHLhuqduIE5n4buNYyBUaOG6o28gTmd1ecOqbiIsIlJvbGUiOiJTViIsIlN0dWR5UHJvZ3JhbUlkcyI6Iks0ODcxNDAyMDIiLCJuYmYiOjE3MzM5NjYzNTEsImV4cCI6MTczMzk3MzU1MSwiaWF0IjoxNzMzOTY2MzUxLCJpc3MiOiJQU0NVSVNBcGkiLCJhdWQiOiJoY211ZSJ9.XD-rhPxyzuoR0duShvYaV7sW2Nd1BRASef6FkdZ9CbY",True)]
        with open("data", mode="r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                data = line.split('|')
                """if len(data) < 3:
                    logging.error(f"Dòng không hợp lệ (bỏ qua): {line}")
                    continue"""
                # Nếu id_to_hoc đã được xử lý, bỏ qua
                if data[0] in processed_ids:
                    continue
                hoc_phans.append(HocPhan(data[0], data[1], data[2]))

        if not hoc_phans:
            logging.info("Không còn phần tử để xử lý.")
            await asyncio.sleep(5)  # Chờ 10 giây trước khi kiểm tra lại
            continue

        timeout = aiohttp.ClientTimeout(total=300)
        semaphore = asyncio.Semaphore(14)

        async def with_semaphore(coro):
            async with semaphore:
                return await coro

        async with aiohttp.ClientSession(timeout=timeout) as session:
            tasks = [with_semaphore(hp.xulydkmhsinhvien(session)) for hp in hoc_phans]
            #tasks = [with_semaphore(hp.RegistSchedule(session)) for hp in hoc_phans]
            await asyncio.gather(*tasks)

        # Cập nhật danh sách đã xử lý thành công
        for hp in hoc_phans:
            if hp.is_thanh_cong:
                processed_ids.add(hp.id_to_hoc)

        logging.info("Chờ 10 giây trước khi thực hiện lần tiếp theo...")
        await asyncio.sleep(0.5)  # Chờ 10 giây trước khi chạy lại

if __name__ == "__main__":
    asyncio.run(main())