#coding=utf8

import pymssql
import ConfigParser


class SF_Station:
    def __init__(self):
        try:
            conf = ConfigParser.ConfigParser()
            conf.read('setting.ini')
            host = conf.get('DBInfo', 'host')
            database = conf.get('DBInfo', 'database')
        except Exception as e:
            raise e
        self.host = host
        self.database = database
        self.usrname = 'sdt'
        self.password = 'SDT#7'

    def queryInfo(self, SN):
        '''
        query station info by SN
        '''
        data = "SN=" + SN + ";$;Station=QueryData;$;MonitorAgentVer=VL20151102.01;$;"
        conn = pymssql.connect(
            host=self.host,
            user=self.usrname,
            password=self.password,
            database=self.database,
            login_timeout=5)
        sqlcommand = '''DECLARE @ReturnValue varchar(7400)
                        EXEC %s '%s','%s','%s','%s',@ReturnValue output
                        SELECT @ReturnValue ''' % ('MonitorPortal', 'NB4',
                                                   'SWDL', 'QueryData', data)
        cur = conn.cursor()
        cur.execute(sqlcommand)
        returnResult = cur.fetchall()[0]
        cdata = cur.nextset()
        conn.commit()
        cur.close()

        print returnResult
        return str(returnResult)

    def uploadInfo(self, station, SN, errorcode, fpy_code):
        '''
        give station, SN, errorcode, fpy_code to upload SF info
        '''
        data = "MASTER:SN=%s;*;MASTER:MB_NUM=;*;MASTER:STATION=%s;*;MASTER:ERRORCODE=%s;*;MASTER:FPYCODE=%s;*;MASTER:MonitorAgentVer=VW20151102.01;*;" % (
            SN, station, errorcode, fpy_code)
        print data
        conn = pymssql.connect(
            host=self.host,
            user=self.usrname,
            password=self.password,
            database=self.database,
            login_timeout=5)
        sqlcommand = '''DECLARE @ReturnValue varchar(7400)
                        EXEC %s '%s','%s','%s','%s',@ReturnValue output
                        SELECT @ReturnValue ''' % ('MonitorPortal', 'NB4',
                                                   station, 'QDW', data)
        cur = conn.cursor()
        cur.execute(sqlcommand)
        returnResult = cur.fetchall()[0]
        cdata = cur.nextset()
        conn.commit()
        cur.close()

        print returnResult
        return str(returnResult)


if __name__ == '__main__':
    t = SF_Station()
    import time
    start = time.time()
    try:
        # t.queryInfo('7921G005MW')
        t.uploadInfo('MIC2', '7924G007E2', 'Pass', 'Pass')
    except Exception as e:
        print e
    end = time.time()
    print end - start
