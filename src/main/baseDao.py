# from transwarp import db
# coding:utf-8
import pymysql as mysql
from spider import LianHangHaoSpider

# import sys
# reload(sys)
# sys.setdefaultencoding("UTF-8")
config = {
    'host': '172.16.0.10',
    'port': 3300,
    'user': 'root',
    'passwd': 'gozapdev',
    'db': 'longdai_p2p_admin',
    'charset': 'utf-8',
    'cursorclass': mysql.cursors.DictCursor,
}


def connect():
    # return mysql.connect(**config)
    return mysql.connect(host="172.16.0.10", port=3300, user="root", passwd="gozapdev", db="longdai_p2p_admin",
                         charset="utf8")
    # db.create_engine(user='root', password='gozapdev', database='longdai_p2p_admin', host='172.16.0.10', port=3300)
    # connect(db='base', user='root', passwd='pwd', host='localhost', port=XXXX)


def insertDB(sql, paramArr):
    db = connect()
    cursor = db.cursor()
    try:
        # do sql
        # sql = 'insert into `lianhanghao_spider` (`proName`,`cityName`,`bankName`,`bankNo`,`bankChildName`,`bankTel`,`bankAddress`) ' \
        #       'values (北京市 ,北京市,中国工商银行,102100099996,中国工商银行总行清算中心,010-68217526,北京市海淀区翠微路15号)'
        sql = sql.encode('utf-8')
        # cursor.execute(sql % spider['proName,spider['cityName,spider['bankName,spider['bankNo,spider['bankChildName,spider['bankTel,spider['bankAddress)
        cursor.execute(sql, (paramArr))
        db.commit()
    except mysql.err.OperationalError:
        print "mysql connect out error"
        print "data : " + paramArr


    except mysql.err.IntegrityError:
        print "bankNo unique error pass "
        pass

    finally:
        db.close()


def batch_insertDB(sql, paramesArr):
    db = connect()
    cursor = db.cursor()
    rs = 0
    try:
        sql = sql.encode('utf-8')
        rs = cursor.executemany(sql, paramesArr)
        db.commit()
    except mysql.err.OperationalError:
        print "batch_insertDB mysql connect out error"
        print "batch_insertDB data : " + paramesArr

    except mysql.err.IntegrityError:
        print "batch_insertDB bankNo unique error pass "
        pass
        index = 0
        for param in paramesArr:
            # insertDB(sql, param)
            try:
                cursor.execute(sql, param)
                db.commit()
            except mysql.err.IntegrityError:
                print "batch_insertDB - single -  bankNo unique error pass "
            index += 1
        if index == 0:
            rs = -1
        else:
            rs = index

    finally:
        db.close()

    return rs


def selectUser(id):
    db = connect()
    cursor = db.cursor()
    try:
        sql = 'select * from t_person where userId = ' + str(id)
        cursor.execute(sql)
        results = cursor.fetchall()
        # commit sql
        db.commit()
    except:
        # error
        db.rollback()
    finally:
        db.close()
        for row in results:
            print row[3]


def selectLeastSpider():
    db = connect()
    cursor = db.cursor()
    demo = LianHangHaoSpider()
    try:
        sql = 'select * from lianhanghao_spider  order by id desc limit 1'
        cursor.execute(sql)
        results = cursor.fetchall()
        print results
        row = results[0]
        demo.id = row[0]
        demo.proName = row[1]
        demo.cityName = row[2]
        demo.bankName = row[3]
        demo.bankNo = row[4]
        demo.bankChildName = row[5]
        demo.bankTel = row[6]
        demo.bankAddress = row[7]
        demo.pageNo = row[8]
        # commit sql
        db.commit()
    except EOFError:
        # error
        db.rollback()
    finally:
        db.close()
    return demo
