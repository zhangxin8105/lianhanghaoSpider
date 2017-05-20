# -*- coding: utf-8 -*-
import sys
import requests
reload(sys)
sys.setdefaultencoding("UTF-8")

proIdList = []
bankMap = {}
proMap = {}
bankIdList = []

bankes = None
proes = None
dataList = []

def init_data():
    print "初始化城市列表和银行数据开始: ...."
    try:
        bankes = open('./bankList', 'r')
        tempBankIdList = []
        for line in bankes:
            lines = line.split("-")
            bankId = lines[0]
            bankName = lines[1]
            bankMap[bankId] = bankName
            tempBankIdList.append(int(bankId))
        print tempBankIdList
        bankIdList = sorted(tempBankIdList)

        proes = open('./proList', 'r')
        tempProIdList = []
        for proObj in proes:
            proSplit = proObj.split("-")
            proId = proSplit[0]
            proName = proSplit[1]
            proMap[proId] = proName
            # tempProIdList.append(int(proId))
            # proIdList = (sorted(tempProIdList)[:])
            proIdList.append(int(proId))
    except EOFError:
        print "error " + EOFError.message
    finally:
        if bankes != None:
            bankes.close()

        if proes != None:
            proes.close()

    # print bankIdList

    # print proIdList
    print "初始化城市列表和银行数据结束: ...."
    print "初始化城市列表和银行数据结束:....."

    return bankIdList


def queryCityes():
    print proIdList
    read_city = open('./cityList', 'r')
    tempLines = read_city.readlines()

    tempLines.__len__()
    if tempLines != None and tempLines.__len__() > 34:
        print "tempLines length  " + str(tempLines.__len__())
        pass
        return
    tempStr = ''
    for proId in proIdList:
        proIdStr = str(proId)
        print "ajax查询省相关信息 " + proIdStr
        url = 'http://www.lianhanghao.com/index.php/Index/Ajax?id=' + proIdStr
        resp = requests.get(url)
        respObj = resp.json()

        if respObj != None and respObj != False:
            for t in respObj:
                temp_str = str(proId) + '-' + proMap[str(proId)].encode("utf-8") + '-' + t['id'].encode("utf-8") + '-' + \
                           t['name'].encode("utf-8")
                temp_str = temp_str.replace('\n', '').strip()
                tempStr = tempStr + temp_str + '\n'

    wirteCity = open("./cityList", 'w')
    wirteCity.write(tempStr)
    wirteCity.flush()
    if wirteCity != None:
        wirteCity.close()

# init_data()
#
# queryCityes()
#
# for i in range(19):
#     print i
