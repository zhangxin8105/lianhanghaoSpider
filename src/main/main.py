# coding:utf-8
import proCity
import __init__

# import time

bankIdList = __init__.init_data()

print __init__.bankIdList
print __init__.bankMap
print __init__.proIdList

for bankId in bankIdList:
    
    bankName = __init__.bankMap[str(bankId)]
    print str(bankId) + " - " + bankName
    proCity.queryCityByProId(bankId)
# proName = __init__.proList[proId]

# proCity.queryCityByProId(id)

# print time.time()


# print time.time()
