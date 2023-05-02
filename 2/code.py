# ta thêm các thư viện cần sử dụng
import pandas as pd
import numpy as np
import os

# ta nhập đường dẫn vào như là input, tuy nhiên em đã print ra để dễ tương tác
print('Nhap duong dan den Data folder: ')
print("C:\\Users\\buivu\\Downloads\\data\\")

# ta đọc các thông tin từ file excel ở đây
thongtinsogd = pd.read_excel('data/sogd.xlsx')
thongtincapbac = pd.read_excel('data/capbac.xlsx')
thongtinloaihinh = pd.read_excel('data/loaihinh.xlsx')
thongtinloaitruong = pd.read_excel('data/loaitruong.xlsx')
thongtinphonggd = pd.read_excel('data/phonggd.xlsx')

gdtx = pd.read_excel('data/gdtx.xlsx')
mamnon = pd.read_excel('data/mamnon.xlsx')
tieuhoc = pd.read_excel('data/tieuhoc.xlsx')
thcs = pd.read_excel('data/thcs.xlsx')
thpt = pd.read_excel('data/thpt.xlsx')

# chúng ta sử dụng từ điển để dễ thao tác, thay vì sử dụng chuỗi hay mảng ( em đã thử hai dạng này trước đó, tuy nhiên đều dẫn đến các bug khó chữa )
dcapbac = {}
dloaihinh = {}
dloaitruong = {}
dphonggd = {}



# ở đây để xử lí các ô dữ liệu trống
def xx(leng):
    ans = ''
    for i in range(leng):
        ans += 'X'
    return ans

# ta tạo hàm để tạo file thêm thông tin
def insert(a, f, table, leng, d):
    for index, row in a.iterrows():
        ma = str(row['ma' + table])
        ten = str(row['ten' + table])
        if (ten == 'nan'):
            ten = 'NULL'
            f.write('INSERT INTO {} VALUES ("{}", NULL);\n'.format(table, ma))
        else:
            f.write('INSERT INTO {} VALUES ("{}", "{}");\n'.format(table, ma, ten))
        d[ten] = ma

# ta thêm thông tin vào table sogd trước
f = open('data/sogd.sql', 'w', encoding='utf-8')
f.write('USE truonghoc;\n')
f.write("INSERT INTO sogd (stt, sogd) VALUES ('1', 'Sở Giáo Dục Và Đào Tạo TPHCM');")
f.close()

# ta thêm thông tin vào table chứa các thông tin cấp bậc, loại hình/trường, phòng giáo dục
def thongtincapbacloaihinhtruongphong():
    f = open('data/thongtincapbacloaihinhtruongphong.sql', 'w', encoding='utf-8')
    f.write('USE truonghoc;\n')
    insert(thongtincapbac, f, 'capbac', 2, dcapbac)
    insert(thongtinloaitruong, f, 'loaitruong', 6, dloaitruong)
    insert(thongtinloaihinh, f, 'loaihinh', 5, dloaihinh)
    insert(thongtinphonggd, f, 'phonggd', 3, dphonggd)
    f.close()


#thêm thông tin vào table chứa thông tin của tất cả các trường
def ins(arr, name, cap):
    with open('data/' + name + '.sql', 'w', encoding='utf-8') as f:
        f.write('USE truonghoc;\n')
        for index, row in arr.iterrows():
            matruong = str(row['matruong'])

            tentruong = str(row['tentruong'])

            diachi = str(row['diachi'])
            if (diachi == 'nan'):
                diachi = 'Không có'

            phonggd = str(row['phonggd'])
            if (phonggd == 'nan'):
                phonggd = 'NULL'
            phonggd = dphonggd[phonggd]

            loaihinh = str(row['loaihinh'])
            if (loaihinh == 'nan'):
                loaihinh = 'NULL'
            loaihinh = dloaihinh[loaihinh]

            loaitruong = str(row['loaitruong'])
            if (loaitruong == 'nan'):
                loaitruong = 'NULL'
            loaitruong = dloaitruong[loaitruong]

            f.write(
                'INSERT INTO thongtintruong VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}");\n'.format(matruong, tentruong, diachi, phonggd, loaihinh, loaitruong, cap))
        f.close()

#ta tiếp tục thêm thông tin
thongtincapbacloaihinhtruongphong()
ins(gdtx, 'gdtx', 'TX')
ins(mamnon, 'mamnon', 'MN')
ins(tieuhoc, 'tieuhoc', 'TH')
ins(thcs, 'thcs', 'CS')
ins(thpt, 'thpt', 'PT')
