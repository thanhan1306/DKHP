import json


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

ds_nhom_to = open_array("ds_nhom_to2_4_25.json")
for nhom in ds_nhom_to:
    print(nhom)