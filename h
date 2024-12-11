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
