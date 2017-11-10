
import pymysql
from xlsxwriter.workbook import Workbook

def write_in_excel(user = 'root',
                    passwd = '12345',
                    host = 'localhost',
                    db = 'mybase',
                    table = 'users'):
    """
    function write mysql's table in excel file
    :param user:
    :param passwd:
    :param host:
    :param db:
    :param table:
    :return:
    """
    con = pymysql.connect(user=user, passwd=passwd, host=host, db=db)
    cursor = con.cursor()

    query = "SELECT * FROM %s;" % table
    cursor.execute(query)

    workbook = Workbook('outfile.xlsx')
    sheet = workbook.add_worksheet()
    for r, row in enumerate(cursor.fetchall()):
        for c, col in enumerate(row):
            sheet.write(r, c, col)

    workbook.close()
    return None