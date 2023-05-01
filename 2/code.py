# import some lib
import pandas as pd
import numpy as np
import os


print('Nhap duong dan den Data folder: ')
print("C:\\Users\\buivu\\Downloads\\data\\")

lk_sgd = pd.read_excel('data/sogd.xlsx')
lk_cap = pd.read_excel('data/capbac.xlsx')
lk_lh = pd.read_excel('data/loaihinh.xlsx')
lk_lt = pd.read_excel('data/loaitruong.xlsx')
lk_pgd = pd.read_excel('data/phonggd.xlsx')


gdtx = pd.read_excel('data/data_gdtx.xlsx')
mn = pd.read_excel('data/data_mn.xlsx')
th = pd.read_excel('data/data_th.xlsx')
thcs = pd.read_excel('data/data_thcs.xlsx')
thpt = pd.read_excel('data/data_thpt.xlsx')

# create dictionary
dcap = {}
dlh = {}
dlt = {}
dpgd = {}
dsgd= {}



# null data
def xx(leng):
    ans = ''
    for i in range(leng):
        ans += 'X'
    return ans


# insert all the table
def inslk(a, f, table, leng, d):
    for index, row in a.iterrows():
        ma = str(row['ma' + table])
        ten = str(row['ten' + table])
        if (ten == 'nan'):
            ten = 'NULL'
            f.write('INSERT INTO {} VALUES ("{}", NULL);\n'.format(table, ma))
        else:
            f.write('INSERT INTO {} VALUES ("{}", "{}");\n'.format(table, ma, ten))
        d[ten] = ma

f = open('data/sogd.sql', 'w', encoding='utf-8')
f.write('USE truonghoc;\n')
f.write("INSERT INTO sogd (stt, sogd) VALUES ('1', 'Sở Giáo Dục Và Đào Tạo TPHCM');")
f.close()

# insert lookup table
def lookup():
    f = open('data/lookup.sql', 'w', encoding='utf-8')
    f.write('USE truonghoc;\n')
    inslk(lk_cap, f, 'capbac', 2, dcap)
    inslk(lk_lt, f, 'loaitruong', 6, dlt)
    inslk(lk_lh, f, 'loaihinh', 5, dlh)
    inslk(lk_pgd, f, 'phonggd', 3, dpgd)
    f.close()


# insert to main table
def ins(arr, name, cap):
    with open('data/' + name + '.sql', 'w', encoding='utf-8') as f:
        f.write('USE truonghoc;\n')
        for index, row in arr.iterrows():
            ma = str(row['matruong'])

            ten = str(row['tentruong'])

            dc = str(row['diachi'])
            if (dc == 'nan'):
                dc = 'Không có'

            pgd = str(row['phonggd'])
            if (pgd == 'nan'):
                pgd = 'NULL'
            pgd = dpgd[pgd]

            lh = str(row['loaihinh'])
            if (lh == 'nan'):
                lh = 'NULL'
            lh = dlh[lh]

            lt = str(row['loaitruong'])
            if (lt == 'nan'):
                lt = 'NULL'
            lt = dlt[lt]

            f.write(
                'INSERT INTO thongtintruong VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}");\n'.format(ma, ten, dc, pgd, lh, lt, cap))
        f.close()


lookup()
ins(gdtx, 'gdtx', 'TX')
ins(mn, 'mn', 'MN')
ins(th, 'th', 'TH')
ins(thcs, 'thcs', 'CS')
ins(thpt, 'thpt', 'PT')