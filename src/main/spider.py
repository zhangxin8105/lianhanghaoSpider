#coding:utf-8
# import baseDao as dao

class LianHangHaoSpider:
    id = ''
    proName = ''
    cityName = ''
    bankName = ''
    bankNo = ''
    bankChildName = ''
    bankTel = ''
    bankAddress = ''
    pageNo = ''
    def __init__(self,proName,cityName,bankName,pageNo):
        self.proName = proName
        self.cityName = cityName
        self.bankName =bankName
        self.pageNo =pageNo

    def __init__(self):
        pass

    def tostring(self):
        return self.proName +',' +self.cityName+','+self.bankName +','+self.bankNo +',' + self.bankChildName +',' +self.bankTel +',' +self.bankAddress + ',' + str(self.pageNo)
    def toStringArr(self):
        strArr = []
        strArr.append(self.proName)
        strArr.append(self.cityName)
        strArr.append(self.bankName)
        strArr.append(self.bankNo)
        strArr.append(self.bankChildName)
        strArr.append(self.bankTel)
        strArr.append(self.bankAddress)
        strArr.append(self.pageNo)
        return strArr


# spider = LianHangHaoSpider()
# spider.proName = 'test'
# spider.cityName = 'test'
# spider.bankName = 'test'
# spider.bankChildName = 'test'
# spider.proName = 'test'

