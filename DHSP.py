import requests

def login():
    url = "https://dkhpapi.hcmue.edu.vn/api/Authen/Authenticate"
    payload = {"username":"48.01.901.155","password":"Ng110913060611"}
    # Headers
    headers = {
        "origin": "https://dkhp.hcmue.edu.vn",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "content-type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Host": "dkhpapi.hcmue.edu.vn",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        response = response.json()
        """
        {
            'Id': '48.01.901.155', 
            'FirstName': None, 
            'LastName': None, 
            'FullName': 'Trần Ngọc Thảo Nguyên', 
            'Token': 'eyJhbGciOiJI...', 
            'Role': 'SV', 
            'GraduateLevel': 'DHCQ', 
            'Expire': '2025-05-13T18:48:53.9026597+07:00', 
            'TrangThai': True
        }"""
        print(response)
        return True
    return False

#lay khoa
def getStudyProgramID(authen):
    url = "https://dkhpapi.hcmue.edu.vn/api/Authen/GetAllStudyProgramRegist"
    # Headers
    headers = {
        "origin": "https://dkhp.hcmue.edu.vn",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "Accept": "application/json, text/plain, */*",
        "Host": "dkhpapi.hcmue.edu.vn",
        "authorization": "Bearer " + authen,
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Connection": "keep-alive"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response = response.json()
        """[{
            'StudyProgramID': 'K487140202', 
            'StudyProgramName': 'Giáo dục Tiểu học'
        }]"""
        print(response)
        return True
    return False

#lay tham so de dang ky mon va kiem tra ket qua
def getIdDotandRandID(authen, StudyProgramID):
    url = f"https://dkhpapi.hcmue.edu.vn/api/Regist/GetRegistSemesterCreditQuota?StudyProgramID={StudyProgramID}"
    # Headers
    headers = {
        "origin": "https://dkhp.hcmue.edu.vn",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "Accept": "application/json, text/plain, */*",
        "Host": "dkhpapi.hcmue.edu.vn",
        "authorization": "Bearer " + authen,
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Connection": "keep-alive"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response = response.json()
        """{
            "ID": 0,
            "IdDot": 60,
            "MainTermMinCredits": 0,
            "MainTermMaxCredits": 100,
            "MaxTheoryCredits": 0,
            "MaxPraticeCredits": 0,
            "RegistNoneProgram": 0,
            "DeletePerMin": 0,
            "IsSinhVienNoPhi": 0,
            "IsInsert": true,
            "IsTranfer": true,
            "IsDelete": true,
            "DebtFee": 0,
            "IsCheckDebtFee": false,
            "RegistAble": true,
            "RegistAbleDescr": "",
            "IsRegistClassStudent": 0,
            "IsRegistPlan": true,
            "IsRegistSecond": false,
            "IsRegistImprove": false,
            "IsRegistCross": false,
            "IsRegistOutPlan": true,
            "IsRegistProgram": 1,
            "IsRegistOutProgram": true,
            "isChanDSSVDK": false,
            "YearStudy": "2024-2025",
            "TermID": "HK03",
            "BeginDate": "05/13/2025 07:45:00",
            "EndDate": "05/13/2025 17:00:00",
            "IsConflictSchedule": true,
            "IsTuChonTuDo": true,
            "LanguageID": "vi-VN",
            "IsStudentTest": 0,
            "RandID": 30848
        }"""
        print(response)
        return True
    print(response.status_code)
    return False

#xem mon da dang ky thanh cong
def getAllClassRegisted(authen, randID, idDot):
    url = "https://dkhpapi.hcmue.edu.vn/api/Regist/GetAllClassRegisted"
    payload = {"ReqParam1":f"{randID}","ReqParam2":f"{idDot}"}
    # Headers
    headers = {
        "origin": "https://dkhp.hcmue.edu.vn",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "content-type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "authorization": "Bearer " + authen,
        "Host": "dkhpapi.hcmue.edu.vn",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        response = response.json()
        """{
            "Rows": [
                {
                    "ScheduleStudyUnitID": "2431LITR191201",
                    "ScheduleStudyUnitAlias": "LITR191201",
                    "ParentScheduleStudyUnitID": null,
                    "StudyUnitID": "2431LITR1912",
                    "StudyUnitTypeID": 1,
                    "StudyUnitTypeName": "Lý thuyết",
                    "CurriculumID": "LITR1912",
                    "CurriculumName": "Cơ sở văn hóa Việt Nam",
                    "Credits": 2.00,
                    "ProfessorName": "Đặng Ngọc  Ngận",
                    "Schedules": "Thứ Hai, Tiết(3 - 6), C.617, ADV<br/> (30/06/2025 -> 29/07/2025)<br/> , Thứ Ba, Tiết(3 - 4), B.114, ADV<br/> (30/06/2025 -> 29/07/2025)<br/> , Thứ Ba, Tiết(3 - 6), B.114, ADV<br/> (30/06/2025 -> 29/07/2025)<br/> ",
                    "Status": 2,
                    "IsTranfer": true,
                    "IsDelete": true,
                    "BeginDate": "30/06/2025",
                    "EndDate": "29/07/2025",
                    "TrungLich": false
                }
            ],
            "Reval": ""
        }"""
        print(response)
        return True
    return False

#xem mon duoc phep dang ky
def getAllClassAllowRegist(authen, StudyProgramID):
    url = "https://dkhpapi.hcmue.edu.vn/api/Regist/GetAllClassAllowRegist"
    payload = {"ReqParam1":f"{StudyProgramID}","ReqParam2":"KH","ReqParam3":"2024-2025","ReqParam4":"HK03","ReqParam5":""}
    # Headers
    headers = {
        "origin": "https://dkhp.hcmue.edu.vn",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "content-type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "authorization": "Bearer " + authen,
        "Host": "dkhpapi.hcmue.edu.vn",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        response = response.json()
        """[
            {
                "CurriculumTypeGroupName": "Tự chọn",
                "classStudyUnits": [
                    {
                        "SelectionName": "Học phần chuyên môn chung lĩnh vực và riêng cho ngành cụ thể",
                        "Selections": [
                            {
                                "StudyUnitID": "2421PRIM1796",
                                "CurriculumID": "PRIM1796",
                                "CurriculumName": "Văn hoá Âm nhạc và Hợp xướng sinh viên 1",
                                "CurriculumType": "2",
                                "NumberOfScheduleStudyUnit": 1,
                                "Credits": 2,
                                "CurriculumTypeGroupName": "Tự chọn",
                                "IsInsert": true,
                                "SelectionID": "10180",
                                "SelectionName": "Học phần chuyên môn chung lĩnh vực và riêng cho ngành cụ thể"
                            }
                        ]
                    }
                ]
            }
        ]"""
        print(response)
        return True
    return False

#xem nhom mon
def getAllScheduleUnitAllowRegist(authen, StudyProgramID, maMon, maNhom = None):
    url = "https://dkhpapi.hcmue.edu.vn/api/Regist/GetAllScheduleUnitAllowRegist"
    payload = {"ReqParam1":f"{StudyProgramID}","ReqParam2":"KH","ReqParam3":f"2431{maMon}"}
    # Headers
    headers = {
        "origin": "https://dkhp.hcmue.edu.vn",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "content-type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "authorization": "Bearer " + authen,
        "Host": "dkhpapi.hcmue.edu.vn",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        responses = response.json()
        """[
            {
                "CurriculumID": "2431EDUC280301",
                "ScheduleStudyUnitAlias": "EDUC280301",
                "CurriculumName": "Khởi nghiệp và giáo dục khởi nghiệp",
                "StudyUnitID": "2431EDUC2803",
                "TypeName": "Lý thuyết",
                "Credits": 0.0,
                "StudentQuotas": "15-50",
                "StudyUnitTypeID": 1,
                "MaxStudentNumber": null,
                "NumberOfStudents": 12,
                "Schedules": " Thứ Hai, Tiết(3 - 6), B.115, ADV<br/> (30/06/2025 -> 29/07/2025)<br/> , Thứ Ba, Tiết(3 - 6), B.115, ADV<br/> (30/06/2025 -> 29/07/2025)<br/> ",
                "ProfessorName": " Nguyễn Hoàng  Thiện",
                "IsRegisted": false,
                "ListOfClassStudentID": "",
                "NumberOfChilds": 0,
                "FeeDebt": "",
                "ParentID": "",
                "UpdateDate": "05/13/2025 09:31:23",
                "NumberRegistOfEmpty": "38",
                "IsHocTrucTuyen": null
            }
        ]"""
        if maNhom is not None:
            for i in responses:
                if i["ScheduleStudyUnitAlias"] == maNhom:
                    return i
        return responses
    return False

#checkdangky
def checkRegistScheduleStudyUnit(authen, StudyProgramID, maNhom):
    url = "https://dkhpapi.hcmue.edu.vn/api/Regist/GetAllScheduleUnitAllowRegist"
    payload = {"ReqParam1":f"{StudyProgramID}","ReqParam2":"KH","ReqParam3":f"2431{maNhom[:8]}"}
    # Headers
    headers = {
        "origin": "https://dkhp.hcmue.edu.vn",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "content-type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "authorization": "Bearer " + authen,
        "Host": "dkhpapi.hcmue.edu.vn",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        responses = response.json()
        """[
            {
                "CurriculumID": "2431EDUC280301",
                "ScheduleStudyUnitAlias": "EDUC280301",
                "CurriculumName": "Khởi nghiệp và giáo dục khởi nghiệp",
                "StudyUnitID": "2431EDUC2803",
                "TypeName": "Lý thuyết",
                "Credits": 0.0,
                "StudentQuotas": "15-50",
                "StudyUnitTypeID": 1,
                "MaxStudentNumber": null,
                "NumberOfStudents": 12,
                "Schedules": " Thứ Hai, Tiết(3 - 6), B.115, ADV<br/> (30/06/2025 -> 29/07/2025)<br/> , Thứ Ba, Tiết(3 - 6), B.115, ADV<br/> (30/06/2025 -> 29/07/2025)<br/> ",
                "ProfessorName": " Nguyễn Hoàng  Thiện",
                "IsRegisted": false,
                "ListOfClassStudentID": "",
                "NumberOfChilds": 0,
                "FeeDebt": "",
                "ParentID": "",
                "UpdateDate": "05/13/2025 09:31:23",
                "NumberRegistOfEmpty": "38",
                "IsHocTrucTuyen": null
            }
        ]"""
        for i in responses:
            if i["ScheduleStudyUnitAlias"] == maNhom:
                if i["IsRegisted"] == True:
                    return True
    return False

#dang ky mon, chuyen nhom => Action = CHANGE
def registScheduleStudyUnit(authen,IdDot, StudyProgramID, payloads, Action = "REGIST"):
    url = f"https://dkhpapi.hcmue.edu.vn/api/Regist/RegistScheduleStudyUnit?TurnID={IdDot}&Action={Action}&StudyProgramID={StudyProgramID}&RegistType=KH"
    """payloads = [
        {
            "CurriculumID":f"2431{maNhom}",
            "ScheduleStudyUnitAlias":f"{maNhom}",
            "CurriculumName":"Phát triển chương trình Tiểu học",
            "StudyUnitID":f"2431{maMon}",
            "TypeName":"Lý thuyết",
            "Credits":0,
            "StudentQuotas":"15-50",
            "StudyUnitTypeID":1,
            "MaxStudentNumber":None,
            "NumberOfStudents":47,
            "Schedules":" Thứ",
            "ProfessorName":" Hồ ",
            "IsRegisted":False,
            "ListOfClassStudentID":"48.01.GDTH.A",
            "NumberOfChilds":0,
            "FeeDebt":"",
            "ParentID":"",
            "UpdateDate":"05/13/2025 09:31:2",
            "NumberRegistOfEmpty":"3",
            "IsHocTrucTuyen":None,
        }
    ]"""
    for payload in payloads:
        payload["isOpen"] = True
        payload["isOpenChilrentTask"] = False
        print(payload)
    # Headers
    headers = {
        "origin": "https://dkhp.hcmue.edu.vn",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "content-type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "authorization": "Bearer " + authen,
        "Host": "dkhpapi.hcmue.edu.vn",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }
    response = requests.post(url, headers=headers, json=payloads)

    if response.status_code == 200:
        response = response.text
        """Đăng ký thành công lớp học phần PHYL240201 """
        print(response.text)
        return True
    print(response.json())
    return False

#huy mon
def removeScheduleStudyUnit(authen,IdDot, StudyProgramID, payloads):
    url = f"https://dkhpapi.hcmue.edu.vn/api/Regist/RemoveScheduleStudyUnit?TurnID={IdDot}&StudyProgramID={StudyProgramID}"
    """payloads = {
    "ScheduleStudyUnitID":"2421PRIM170601",
    "ScheduleStudyUnitAlias":"PRIM170601",
    "ParentScheduleStudyUnitID":null,
    "StudyUnitID":"2421PRIM1706",
    "StudyUnitTypeID":1,
    "StudyUnitTypeName":"Lý thuyết",
    "CurriculumID":"PRIM1706",
    "CurriculumName":"Phát triển chương trình Tiểu học",
    "Credits":2,
    "ProfessorName":"Hồ Ngọc Khải",
    "Schedules":"Thứ Hai, Tiết(7 - 10), A.413, ADV<br/> (10/02/2025 -> 12/05/2025)<br/> , Thứ Hai, Tiết(7 - 10), Online, ADV<br/> (10/02/2025 -> 12/05/2025)<br/> , Thứ Hai, Tiết(7 - 8), A.413, ADV<br/> (10/02/2025 -> 12/05/2025)<br/> ",
    "Status":2,
    "IsTranfer":true,
    "IsDelete":true,
    "BeginDate":"10/02/2025",
    "EndDate":"12/05/2025",
    "TrungLich":false}"""
    # Headers
    headers = {
        "origin": "https://dkhp.hcmue.edu.vn",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "content-type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "authorization": "Bearer " + authen,
        "Host": "dkhpapi.hcmue.edu.vn",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }
    response = requests.post(url, headers=headers, json=payloads)

    if response.status_code == 200:
        response = response.text
        """Đăng ký thành công lớp học phần PHYL240201 """
        print(response.text)
        return True
    print(response.json())
    return False



authen = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJJZCI6IjQ4LjAxLjkwMS4xNTUiLCJOYW1lIjoiVHLhuqduIE5n4buNYyBUaOG6o28gTmd1ecOqbiIsIlJvbGUiOiJTViIsIlN0dWR5UHJvZ3JhbUlkcyI6Iks0ODcxNDAyMDIiLCJuYmYiOjE3NDcxMjkwOTEsImV4cCI6MTc0NzEzNjI5MSwiaWF0IjoxNzQ3MTI5MDkxLCJpc3MiOiJQU0NVSVNBcGkiLCJhdWQiOiJoY211ZSJ9.XANekvhQsRvmtG93eTZTuhOc14d8zZ7FYobqIog7mbo"
StudenID = "K487140202"
randID = "30848"
idDot = "60"
maMon = ["EDUC2803", "LITR1912"]
maNhom = ["EDUC280302", "LITR191201"]
payloads = []
for ma in maNhom:
    print(ma[:8])
    result = getAllScheduleUnitAllowRegist(authen, StudenID, ma[:8], ma)
    if result["ScheduleStudyUnitAlias"] == ma:  # Kiểm tra kết quả trả về hợp lệ
        payloads.append(result)
print(payloads)
for payload in payloads:
    print(payload)
registScheduleStudyUnit(authen, idDot, StudenID, payloads)
for ma in maNhom:
    if checkRegistScheduleStudyUnit(authen,StudenID, ma):
        print(ma + " thanh cong")
    else:
        print(ma + " that bai")