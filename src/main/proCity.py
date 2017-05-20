# coding:utf-8
import requests
import sys

bankNoSet = {}
reload(sys)
sys.setdefaultencoding('utf-8')
import __init__
from bs4 import BeautifulSoup
# import beautifulsoup

import baseDao as sqlDao

onFlag = 0
from spider import LianHangHaoSpider

cityList = []

onFlag = 0


def onBankNoSet(bankNo):
    rs = False
    for key, value in bankNoSet.iteritems():
        key = str(key)
        if key != '' and key == str(bankNo):
            rs = True

    return rs


def readCityList():
    if cityList.__len__() == 0:
        readCityR = open('./cityList', 'r')
        for rs in readCityR.readlines():
            cityList.append(rs)
        readCityR.close()


def queryProIdByName(proName):
    proName = str(proName).replace('\n', '').strip()
    # proJson = json.loads(str(__init__.proMap))
    for key, value in __init__.proMap.iteritems():

        value = str(value).replace('\n', '').strip()
        if value == proName:
            return key


def queryCityIdByName(cityName):
    for city in cityList:
        cityInfo = str(city).split('-')
        if str(cityName).strip() == str(cityInfo[3]).strip():
            return cityInfo[2]


def queryCityName(cityId):
    for city in cityList:
        cityInfo = city.split('-')
        if int(cityId) == int(cityInfo[2]):
            return cityInfo[3]


def queryBankId(bankName):
    bankName = str(bankName).replace('\n', '').strip()
    for key, value in __init__.bankMap.iteritems():
        value = str(value).replace('\n', '').strip()
        if value == bankName:
            return key


def queryCityByProId(bankId):
    global onFlag
    readCityList()
    leastSpider = sqlDao.selectLeastSpider()
    if (leastSpider != None):
        dbProName = leastSpider.proName
        dbProId = queryProIdByName(dbProName)
        dbCityId = queryCityIdByName(leastSpider.cityName)
        dbBankId = queryBankId(leastSpider.bankName)
        dbPageNo = leastSpider.pageNo
        dbPageNo = int(dbPageNo)
    # 指定某个银行时,不需要此判断
    # if(int(bankId) < int(dbBankId)):
    #     return

    if (int(bankId) > int(dbBankId)):
        onFlag = 1
    for t in cityList:
        cityInfo = t.split('-')
        proId = str(cityInfo[0])
        cityId = str(cityInfo[2])
        # 临时断点
        if int(bankId) == 3:
            queryOnlineData(bankId, proId, cityId, 1)
        else:
            break

        if (int(bankId) > int(dbBankId)):
            queryOnlineData(bankId, proId, cityId, 1)
        elif onFlag == 1 and int(bankId) == int(dbBankId) and int(proId) > int(dbProId) and int(cityId) > int(dbCityId):
            queryOnlineData(bankId, proId, cityId, 1)
        elif int(bankId) == int(dbBankId) and int(proId) == int(dbProId) and int(cityId) == int(
                dbCityId) and onFlag == 0:
            onFlag = 1
            queryOnlineData(bankId, proId, cityId, dbPageNo + 1)
        else:
            pass
            # print"bankId " + str(bankId) + " proId - cityId : " + proId + " --- " + cityId
            # print str(onFlag)
            # if int(bankId) == int(dbBankId) and int(proId) == int(dbProId) and int(cityId) == int(dbCityId) and (
            #                 onFlag == 0 or onFlag == '0'):
            #     queryOnlineData(bankId, proId, cityId, 1)
            #     onFlag = 1
            # if int(bankId) >= int(dbBankId) and int(proId) > int(dbProId) and int(cityId) > int(dbCityId):
            #     queryOnlineData(bankId, proId, cityId, 3)


def queryOnlineData(bankId, proId, cityId, pageNo):
    if int(proId) < 20 or int(cityId) < 251:
        return
    tempUrlPre = "http://www.lianhanghao.com/index.php/Index/index/bank/" + str(bankId) + "/province/" + str(
        proId) + "/city/" + str(cityId) + "/p/1.html"
    print str("tempUrlPre :  ") + str(tempUrlPre)
    tempRespPre = requests.get(tempUrlPre)
    respTextPre = tempRespPre.text
    soupPre = BeautifulSoup(respTextPre)
    aTags = soupPre.find_all('a', {'class': 'num'})
    totoalPage = 0
    len = aTags.__len__()
    if len > 0:
        a = aTags[len - 1]
        totoalPage = int(a.text)
    else:
        # only one
        totoalPage = 1

    bankId = str(bankId)
    proId = str(proId)
    cityId = str(cityId)
    print "totoalPage : " + str(totoalPage)
    for i in range(totoalPage):
        index = pageNo + i
        if index > int(i + 1):
            index = (i + 1)
        # print t['name'] + str(index) + " : " + bankId + " : " + __init__.bankList[bankId]
        index = str(index)
        dataUrl = "http://www.lianhanghao.com/index.php/Index/index/bank/" + bankId + "/province/" + proId + "/city/" + cityId + "/p/" + index + ".html"
        print str("dataUrl :  ") + str(dataUrl)
        tempResp = requests.get(dataUrl)
        respText = tempResp.text
        if cityId == 357 or cityId == '357':
            print "357 cityName: " + queryCityName(cityId)
        genData(respText, __init__.bankMap[bankId], __init__.proMap[proId], queryCityName(cityId), index, pageNo)


def genData(respDataStr, bankName, proName, cityName, pageNo, times):
    bankName = str(bankName).replace('\n', '').strip()
    proName = str(proName).replace('\n', '').strip()
    cityName = str(cityName).replace('\n', '').strip()
    soup = BeautifulSoup(respDataStr)
    # print str(soup.contents)
    table = soup.find("table", {"class": "table"})
    if table != None:
        for tag in table.tbody:
            if tag != None and str(tag).replace('\n', '').strip() != '':
                tagStr = str(tag)
                tableSoup = BeautifulSoup(tagStr)
                index = 0
                bankNo = ''
                bankChildName = ''
                bankTel = ''
                bankAddress = ''
                demoSpider = LianHangHaoSpider()
                demoSpider.proName = proName
                demoSpider.cityName = cityName
                demoSpider.bankName = bankName
                demoSpider.bankNo = ''
                demoSpider.pageNo = pageNo
                for td in tableSoup.tr:
                    tdStr = str(td)
                    if tdStr != None and tdStr != '' and tdStr.replace('\n', '').strip() != '':
                        demoSpider.bankName = bankName
                        demoSpider.proName = proName
                        demoSpider.cityName = cityName
                        tdSoup = BeautifulSoup(str(td))
                        tdmessage = tdSoup.text
                        if tdmessage != None and tdmessage.strip() != '':
                            if (index == 0):
                                tdmessage = str(tdmessage).encode('utf-8')
                                print "bankNo == : " + tdmessage
                                demoSpider.bankNo = tdmessage

                            if (index == 1):
                                print "bankChildName == :" + tdmessage
                                demoSpider.bankChildName = tdmessage
                            if (index == 2):
                                print "tel == :" + tdmessage
                                demoSpider.bankTel = tdmessage
                            if (index == 3):
                                print "address == :" + tdmessage
                                demoSpider.bankAddress = tdmessage
                            index = index + 1
                # sql = "insert into `lianhanghao_spider` (`proName`,`cityName`,`bankName`,`bankNo`,`bankChildName`,`bankTel`,`bankAddress`) values ("+proName+","+cityName +","+ bankName +","+bankNo+","+bankChildName+","+bankTel +","+bankAddress +""+proName+","+cityName +","+ bankName +","+bankNo+","+bankChildName+","+bankTel +","+bankAddress +")"
                # sql = "insert into `lianhanghao_spider` (`proName`,`cityName`,`bankName`,`bankNo`,`bankChildName`,`bankTel`,`bankAddress`) values ('%s','%s','%s','%s','%s','%s','%s')"
                # demoSpider.inserDB()

                if demoSpider.bankNo != '' and demoSpider.bankNo != None and onBankNoSet(demoSpider.bankNo) == False:
                    __init__.dataList.append(demoSpider)

                    print "data List length1 : " + str(len(__init__.dataList))
                    if (len(__init__.dataList) >= 10):
                        index = 0
                        # 做批量插入
                        paramesArr = []
                        for data in __init__.dataList:
                            param = data.toStringArr()
                            paramesArr.append(param)
                            index += 1

                        sql = """insert into lianhanghao_spider (`proName`,`cityName`,`bankName`,`bankNo`,`bankChildName`,`bankTel`,`bankAddress`,`pageNo`) values (%s,%s,%s,%s,%s,%s,%s,%s)"""
                        rs = sqlDao.batch_insertDB(sql, paramesArr)
                        if (rs == index):
                            print "data list insert success and list now is  empty"
                            __init__.dataList = []
                        elif (rs == -1):
                            # 违反 bankNo唯一性
                            __init__.dataList = []
                        elif rs != -1:
                            # 有重复的bankNo
                            print "data list insert success  but bankNo not only "
                            __init__.dataList = []
                        else:
                            __init__.dataList = []
                            # def readCity():
                            #     readCityR = open('./cityList', 'r')
                            #
                            #     for rs in readCityR.readlines():
                            #         print rs
            else:
                pass

                # readCity()
