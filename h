 @staticmethod
    def doc_file_khach_hang(filem):
        df = pd.read_csv(filem)
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
            User.ds_user.append(user)

    @staticmethod
    def doc_file_khach_hang1(filename):
        # Đọc dữ liệu từ file CSV (khách hàng)
        df = pd.read_csv(filename)

        for _, row in df.iterrows():
            email = str(row["EMAIL"])  # Chuyển email thành chuỗi
            username = str(row["USERNAME"])  # Chuyển username thành chuỗi
            password = str(row["PASSWORD"])  # Chuyển password thành chuỗi
            auth = row.get("AUTH", None)
            ex = row.get("EX", None)
            ds_mon = json.loads(row.get("id_mon", None))

            user = User(email, username, password, ds_mon)
            if ex and isinstance(ex, str):
                try:
                    ex_time = datetime.strptime(ex, "%d/%m/%Y %H:%M:%S")
                    if ex_time < datetime.now():
                        user.login()
                    else:
                        user.ex = ex
                except ValueError:
                    user.cap_nhat_ex()

            if user.doc_auth(auth) is False or ex is None:
                if user.login() is False:
                    print("Lỗi đăng nhập:" + email + "|" + username + "|" + password)

            User.ds_user.append(user)

    @staticmethod
    def doc_file_nhom_to(filepath):
        # Đọc dữ liệu từ file CSV (nhóm tổ)
        user_dict = {}
        with open(filepath, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                # Lấy email và các thông tin từ file CSV
                email = row["email"].strip()
                id_to_hoc = row["id_to_hoc"]
                is_thanh_cong = row["is_thanh_cong"].strip().lower() == "true"
                result = row.get("result", None)

                # Nếu email chưa có trong từ điển, tạo mới User
                if email not in user_dict:
                    user_dict[email] = User(email, username="default_username", password="default_password")

                # Thêm thông tin nhóm tổ vào danh sách
                user_dict[email].ds_nhom_to.append({
                    "id_to_hoc": id_to_hoc,
                    "is_thanh_cong": is_thanh_cong,
                    "result": result
                })

        # Gán danh sách người dùng vào ds_user
        for user in user_dict.values():
            User.ds_user.append(user)


        #print(f"Đã nạp {len(User.ds_user)} người dùng từ file.")

    @staticmethod
    def ghi_file(filename):
        # Chuyển danh sách User thành DataFrame
        data = [
            {
                "EMAIL": user.email,
                "USERNAME": str(user.username),
                "PASSWORD": str(user.password),
                "AUTH": user.auth,
                "EX": user.ex
            }
            for user in User.ds_user
        ]
        df = pd.DataFrame(data)

        # Ghi DataFrame vào file CSV
        df.to_csv(filename, index=False)
        print(f"Dữ liệu đã được ghi vào file {filename}.")

    @staticmethod
    def hien_thi_ds_user():
        # Tạo bảng
        table = PrettyTable()

        # Đặt tiêu đề cho bảng, bao gồm số thứ tự
        table.field_names = ["STT", "Email", "Username", "Password", "Ex", "Auth"]

        # Thêm các hàng dữ liệu vào bảng, cộng thêm số thứ tự
        for idx, user in enumerate(User.ds_user, 1):  # Bắt đầu từ số 1
            table.add_row([idx, user.email, user.username, user.password, user.ex, user.auth])

        # Hiển thị bảng
        print(table)

    def doc_auth(self, auth_token):
        if not isinstance(auth_token, str):
            auth_token = str(auth_token)  # Chuyển đổi thành chuỗi nếu cần
        if auth_token.startswith("bearer "):
            auth_token = auth_token[len("bearer "):]

        try:
            decoded_payload = jwt.decode(auth_token, options={"verify_signature": False})
            self.auth = "bearer " + auth_token
            #print(f"AUTH:{self.email}|{self.username}|{self.password} hop le")
            return True
            #print(f"Thông tin auth cho {self.email}: {self.auth}")
        except jwt.ExpiredSignatureError:
            print(f"Token của {self.email} đã hết hạn.")
            #print(f"AUTH:{self.email}|{self.username}|{self.password} hop le")
            return False
        except jwt.InvalidTokenError:
            print(f"Token của {self.email} không hợp lệ.")
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
        print(response)
        return False
import time
import random
import aiohttp
import asyncio
import logging

# Cấu hình logging để theo dõi lỗi và thông báo
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
    def __init__(self, id_to_hoc, email, auth):
        self.id_to_hoc = id_to_hoc
        self.email = email
        self.auth = auth
        self.is_thanh_cong = False
        self.result = ""

    def thongbao(self):
        if self.is_thanh_cong:
            logging.info(f"Thành công: {self.id_to_hoc} - {self.result} - {self.email}")
        else:
            logging.warning(f"Không thành công: {self.id_to_hoc} - {self.result} - {self.email}")

    async def xulydkmhsinhvien(self, session):
        url = "https://thongtindaotao.sgu.edu.vn/dkmh/api/dkmh/w-xulydkmhsinhvien"
        payload = {
            "filter": {
                "id_to_hoc": self.id_to_hoc,
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
        for attempt in range(3):  # Thử tối đa 3 lần
            try:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        data = response_data.get("data", {})
                        if data.get("is_thanh_cong"):
                            self.is_thanh_cong = True
                            self.result = data.get("ket_qua_dang_ky", {}).get("ngay_dang_ky", "Không có thông tin ngày đăng ký")
                            return
                        else:
                            self.result = data.get('thong_bao_loi', "Lỗi không xác định")
                    else:
                        self.result = f"Lỗi HTTP: {response.status}"
            except Exception as e:
                self.result = f"Lỗi xảy ra: {e}"
            await asyncio.sleep(2)  # Chờ 2 giây trước khi thử lại
        self.thongbao()

async def main():
    hoc_phans = []
    with open("data.txt", mode="r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = line.split('|')
            if len(data) < 3:
                logging.error(f"Dòng không hợp lệ (bỏ qua): {line}")
                continue
            hoc_phans.append(HocPhan(data[0], data[1], data[2]))

    timeout = aiohttp.ClientTimeout(total=300)
    semaphore = asyncio.Semaphore(5)

    async def with_semaphore(coro):
        async with semaphore:
            return await coro

    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [with_semaphore(hp.xulydkmhsinhvien(session)) for hp in hoc_phans]
        await asyncio.gather(*tasks)

    for hp in hoc_phans:
        hp.thongbao()

if __name__ == "__main__":
    asyncio.run(main())
async def main():
    hoc_phans = []
    with open("data", mode="r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

                # Tách dữ liệu theo dấu phẩy (hoặc thay bằng ký tự phù hợp với file của bạn)
            data = line.split('|')

            # Kiểm tra xem có đủ 3 phần tử không
            if len(data) < 3:
                print(f"Dòng không hợp lệ (bỏ qua): {line}")
                continue

            # Thêm vào danh sách HocPhan
            hoc_phans.append(HocPhan(data[0], data[1], data[2]))


    timeout = aiohttp.ClientTimeout(total=60)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        tasks = [hp.xulydkmhsinhvien(session) for hp in hoc_phans]
        await asyncio.gather(*tasks)

    for hp in hoc_phans:
        hp.thongbao()

if __name__ == "__main__":
    asyncio.run(main())
# Hàm gửi dữ liệu đến Google Forms
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