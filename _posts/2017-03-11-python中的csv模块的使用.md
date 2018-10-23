---
layout: default
title: python中csv模块的使用
author: 穆亚磊
tags:：
   - python模块
---
#### csv简介
CSV (Comma Separated Values)，即逗号分隔值（也称字符分隔值，因为分隔符可以不是逗号），是一种常用的文本
格式，用以存储表格数据，包括数字或者字符。很多程序在处理数据时都会碰到csv这种格式的文件，它的使用是比
较广泛的（Kaggle上一些题目提供的数据就是csv格式），csv虽然使用广泛，但却没有通用的标准，所以在处理csv
格式时常常会碰到麻烦，幸好Python内置了csv模块。下面简单介绍csv模块中最常用的一些函数。

更多内容请参考：[https://docs.python.org/2/library/csv.html#module-csv](https://docs.python.org/2/library/csv.html#module-csv)


#### csv模块中的函数
1.reader(csvfile, dialect='excel', **fmtparams)

参数说明：

csvfile，必须是支持迭代(Iterator)的对象，可以是文件(file)对象或者列表(list)对象，如果是文件对
象，打开时需要加"b"标志参数。

dialect，编码风格，默认为excel的风格，也就是用逗号（,）分隔，dialect方式也支持自定义，通过调用register_dialect方法来注册，下文会提到。

fmtparam，格式化参数，用来覆盖之前dialect对象指定的编码风格。
```
import csv  
with open('test.csv','rb') as myFile:  
    lines=csv.reader(myFile)  
    for line in lines:  
        print line 
```

'test.csv'是文件名，‘rb’中的r表示“读”模式，因为是文件对象，所以加‘b’。open()返回了一个文件对象
myFile，reader(myFile)只传入了第一个参数，另外两个参数采用缺省值，即以excel风格读入。reader()返回一个
reader对象lines,lines是一个list，当调用它的方法lines.next()时，会返回一个string。上面程序的效果是将csv
文件中的文本按行打印，每一行的元素都是以逗号分隔符','分隔得来。

在我的test.csv文件中，存储的数据如图：

![2017-03-11-python中的csv模块的使用图片1.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-11-python%E4%B8%AD%E7%9A%84csv%E6%A8%A1%E5%9D%97%E7%9A%84%E4%BD%BF%E7%94%A8%E5%9B%BE%E7%89%871.png)

程序输出：
```
['1','2'] 
['3','a'] 
['4','b']
```

补充：reader对象还提供一些方法：line_num、dialect、next()

2.writer(csvfile, dialect='excel', **fmtparams)

参数的意义同上，这里不赘述，直接上例程：
```
with open('t.csv','wb') as myFile:      
    myWriter=csv.writer(myFile)  
    myWriter.writerow([7,'g'])  
    myWriter.writerow([8,'h'])  
    myList=[[1,2,3],[4,5,6]]  
    myWriter.writerows(myList)  
```
'w'表示写模式。

首先open()函数打开当前路径下的名字为't.csv'的文件，如果不存在这个文件，则创建它，返回myFile文件对象。

csv.writer(myFile)返回writer对象myWriter。

writerow()方法是一行一行写入，writerows方法是一次写入多行。

注意：如果文件't.csv'事先存在，调用writer函数会先清空原文件中的文本，再执行writerow/writerows方法。

补充：除了writerow、writerows，writer对象还提供了其他一些方法：writeheader、dialect

3.register_dialect(name, [dialect, ]**fmtparams)

这个函数是用来自定义dialect的。

参数说明：

name,你所自定义的dialect的名字，比如默认的是'excel'，你可以定义成'mydialect'

[dialect, ]**fmtparams，dialect格式参数，有delimiter（分隔符，默认的就是逗号）、quotechar、
quoting等等，可以参考Dialects and Formatting Parameters

`csv.register_dialect('mydialect',delimiter='|',quoting=csv.QUOTE_ALL)`  

上面一行程序自定义了一个命名为mydialect的dialect，参数只设置了delimiter和quoting这两个，其他的仍然采用
默认值，其中以'|'为分隔符。接下来我们就可以像使用'excel'一样来使用'mydialect'了。我们来看看效果：

在我test.csv中存储如下数据：

![2017-03-11-python中的csv模块的使用图片2.png](https://github.com/muyalei/muyalei.github.io/blob/gh-pages/img/2017-03-11-python%E4%B8%AD%E7%9A%84csv%E6%A8%A1%E5%9D%97%E7%9A%84%E4%BD%BF%E7%94%A8%E5%9B%BE%E7%89%872.png)

以'mydialect'风格打印：
```
with open('test.csv','rb') as myFile:  
    lines=csv.reader(myFile,'mydialect')  
    print lines.line_num  
    for line in lines:  
        print line  
```
输出：
```
['1,2','3'] 
['4,5','6']
```

可以看到，现在是以'|'为分隔符，1和2合成了一个字符串（因为1和2之间的分隔符是逗号，而mydialect风格的分隔
符是'|'），3单独一个字符串。

对于writer()函数，同样可以传入mydialect作为参数，这里不赘述。
4.unregister_dialect(name)
这个函数用于注销自定义的dialect

此外，csv模块还提供get_dialect(name)、list_dialects()、field_size_limit([new_limit])等函数，这些都比较
简单，可以自己试试。比如list_dialects()函数会列出当前csv模块里所有的dialect：
```
print csv.list_dialects()  
输出：
['excel-tab','excel','mydialect']
```
'mydialect'是自定义的，'excel-tab', 'excel'都是自带的dialect，其中'excel-tab'跟'excel'差不多，
只不过它以tab为分隔符。

csv模块还定义了

一些类：DictReader、DictWriter、Dialect等，DictReader和DictWriter类似于reader和writer。

一些常量：QUOTE_ALL、QUOTE_MINIMAL、.QUOTE_NONNUMERIC等，这些常量可以作为Dialects and Formatting Parameters的值。


### 使用实例
```
#-*- coding:utf-8 -*-
import os,re
import time
import xlrd
import mysql.connector


#连接mysql
conn = mysql.connector.connect(user='root',password='toor',database='qytxl_batwd',host='localhost')
cursor = conn.cursor()



#处理无表头的sheet文件
#无表头,不需要再横切,也不需要纵切
def no_heading(excel,sheet):

    db_cols = []
    value_index = []

    #判断每一列的表头值
    for col_num in range(sheet.ncols):  #遍历所有列
        col_values = []   #记录该列前200个单元格每个非空单元格值对应的数据库中字段值，单元格值不符合特征字典中任何一个值时，直接跳过该单元格值
        for col_value in map(str,sheet.col_values(col_num)[0:200]):  #只检查该列的前200个值
            if col_value:
                col_value = str(col_value).strip().replace('\n','')
                col_value = col_value.replace('\u3000','')
                col_value = col_value.replace(' ','')
                col_value = col_value.replace('\t','')
                col_value = col_value.replace('\n','')
                #判断是否为部门
                if col_value in bumen or re.search(r'.部$',col_value):
                    col_values.append('col_0')
                    continue
                #判断是否为职务
                for item in zhiwu:
                    if item in col_value:
                        col_values.append('col_3')
                        continue
                #判断是否为姓名
                for item in names:
                    if item in col_value and len(col_value)==3 or item in col_value and len(col_value)==2:
                        col_values.append('col_1')
                        continue
                #判断是否为手机号
                if len(col_value)==11 or len(col_value)==13:
                    if col_value[0]=='1' and col_value[1] in ['3','4','5','6','7','8']:
                        col_values.append('col_5')
                        continue
                #判断是否为座机
                if len(col_value)==8 or len(col_value)==10 or len(col_value) ==12:
                    L_tel_num = []    #用于检查是否col_value中的每个字符都是数字或 -
                    for x in col_value:
                        if x in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] or x=='-':
                            L_tel_num.append(1)
                    if len(L_tel_num)==len(col_value):
                        col_values.append('col_6')
                        continue
                #判断是否为E-mail
                if re.search(r'^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])',col_value):
                    col_values.append('col_4')
                    continue

        #根据表头出现的次数确定该列表头
        #5个以上的单元格值在特征字典中找到符合条件的值，才认为该列是有效数据列，否则，直接跳过该列
        if len(col_values)>5:
            count_times = []
            for item in col_values:
                count_times.append(col_values.count(item))  #将每个key出现的次数计入count_times中
            m = max(count_times)   #现在count_times中每个key的位置被取代为该key在count_times中出现的次数,拿到最大值
            if m>=3:  #出现次数最多的表头标签至少出现5次,才认为是有效的
                MaxValue_index = count_times.index(m)   #拿到出现次数最多的key在count_times中的位置
                key = col_values[MaxValue_index]   #拿到出现次数最多的数据库中字段key_value，即表头值
            else:
                key = None
            if key:
                if key not in db_cols:
                    db_cols.append(key)
                    value_index.append(col_num)
            else:
                print('该列数据无效！')
        else:
            print('该列数据无效！')

    if len(set(db_cols))<2:   #如果有效数据少于2列，则该sheet直接抛弃
        f_worthless.write(excel+'\t'+sheet.name+'\n')   #将无价值的sheet名及excel名写入 '无效的excel.txt'
        return None
    else:
        #按行写入mysql
        for row_num in range(sheet.nrows):
            values = [sheet.row_values(row_num)[i] for i in value_index]
            sqli = ('insert into qytxl_no_heading(' + ','.join(db_cols) + ',' + 'col_company' + ',' + 'col_remarks' + ',' + 'col_source' + ',' + 'col_from' + ')' + ' ' + 'values(' + '"' + '","'.join(map(str,values)).replace('\\', '') + '"' + ',' + '"' + company_name + '"' + ',' + '"' + ','.join(map(str, remarks)).replace('"', '').replace('\\', '') + '"' + ',' + '"' + ','.join(map(str,sheet.row_values(row_num))).replace('"', '').replace('\\','') + '"' + ',' + '"' + excel + '"' + ")").encode('utf-8').decode('utf-8')
            print(sqli)
            try:
                cursor.execute(sqli)
            except Exception as e:
                print('该行数据插入mysql失败,错误信息:%s' % str(e.args))
                f_inserError.write(','.join(map(str,sheet.row_values(row_num)))+'\n')
        conn.commit()



#得到当前sheet的表头行行号,并将其写入hl_num_L
def get_hl_num_L(excel,sheet):
    hl_num_L = []
    for row_num in range(sheet.nrows):  #遍历所有行,查找表头行
        hv_L = []  #存放识别到的表头行有效表头值,目的是排除 例如某一行有两个单元格的值是'传真',会把该行认为是一个表头行 的情况。
        for col_num in range(sheet.ncols):
            cell_value = str(sheet.cell_value(row_num, col_num))
            cell_value = cell_value.replace(' ', '')
            cell_value = cell_value.replace('\t', '')
            cell_value = cell_value.replace('\n', '')
            if cell_value in heading_list:
                hv_L.append(cell_value)
        if len(set(hv_L))>=2:
            hl_num_L.append(row_num)
    return hl_num_L



#提取客服电话、传真、地址等的备注信息
def get_remarks(sheet):
    global remarks
    remarks = []
    for row_num in range(sheet.nrows):   #不能在这里用range(10)，对于总行数小于10行的sheet，会报错
        if row_num<10:    #只检查前10行
            for col_num in range(sheet.ncols):
                cell_value = str(sheet.cell_value(row_num,col_num))
                if re.search(r':',cell_value) or re.search(r'：',cell_value):
                    remarks.append(cell_value)


#提取公司名称
def get_company_name(excel,sheet):
    global company_name

    #检查当前sheet的前10行，如果找到符合正则表达式的单元格值，判定该单元格值为公司名，否则以excel名称为公司名
    for row_num in range(sheet.nrows):
        if row_num<10:   #只检查前10行
            for col_num in range(sheet.ncols):
                cell_value = str(sheet.cell_value(row_num,col_num))
                if re.search(r'.通讯录',cell_value) or re.search(r'.通讯簿',cell_value):
                    company_name = cell_value
                else:
                    company_name = excel



#主程序
def main(item):

    #读取待处理的excel文件名及对应的sheet名
    item = item.split('\t')
    excel_name = item[0]
    sheet_name = item[1]
    print('正在打开文件%s的表%s' % (excel_name,sheet_name))

    workbook = xlrd.open_workbook(os.getcwd()+r'\excel'+'\\'+excel_name)
    sheet = workbook.sheet_by_name(sheet_name)
    get_company_name(excel_name,sheet)
    get_remarks(sheet)
    no_heading(excel_name,sheet)



#程序入口
if __name__=='__main__':
    global heading_list
    global f_worthless,f_inserError,f_no_heading
    global bumen,names,zhiwu,remarks

    f_worthless = open(os.getcwd()+r'\无效的excel.txt','a+',encoding='utf-8',errors='ignore')
    f_inserError = open(os.getcwd()+r'\insertError.txt','a+',encoding='utf-8',errors='ignore')  #插入excel报错的数据行

    #获取包含所有表头值的列表
    with open(os.getcwd()+r'\headers.txt','r',encoding='utf-8',errors='ignore') as f:
        headers = f.read()
        f.close()
    heading_list = headers.replace(',','\n').split('\n')

    #读取无表头excel的特征字典
    with open(os.getcwd()+r'\no_headers'+r'\部门.txt','r',encoding='utf-8',errors='ignore') as f:
        bumen = f.read().split(',')
        f.close()
    with open(os.getcwd()+r'\no_headers'+r'\中文名.txt','r',encoding='utf-8',errors='ignore') as f:
        names = f.read().split(',')
        f.close()
    with open(os.getcwd()+r'\no_headers'+r'\职务.txt','r',encoding='utf-8',errors='ignore') as f:
        zhiwu = f.read().split(',')
        f.close()

    #main('2.xls\t2013年组织机构')  #@测试代码

    #遍历待处理多表头sheet
    with open(r'C:\Users\龚才春\Desktop\BAT+万达\综合','r',encoding='utf-8',errors='ignore') as f:
        sheets = f.read().split('\n')
        f.close()

    for item in sheets:
        if item:
            main(item)
    """
    #断点恢复
    for item in sheets[sheets.index('（大部分是我们公司的会员）聚成名录.xls\t公司会员名单（聚成）'):]:
        if item:
            main(item)
    """

    f_worthless.close()
    f_inserError.close()

```
