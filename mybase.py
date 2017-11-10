
import pymysql

class Mysql(object):
    """
    mysql queries
    """
    def __init__(self):
        self.connection = None

    def __del__(self):
        try:
            self.connection.close()
        except Exception:
            pass

    def configuration(self, host='localhost',
                    user='root',
                    password='12345',
                    db='mybase',
                    charset='utf8mb4',
                    cursorclass=pymysql.cursors.DictCursor):
        """
        configuration denied
        :param host:
        :param user:
        :param password:
        :param db:
        :param charset:
        :param cursorclass:
        :return:
        """
        # Connect to the database
        self.connection = pymysql.connect(host=host, user=user, password=password, db=db, charset=charset,
                                          cursorclass=cursorclass)
        return None


    def query(self, sql):
        """
        All queries except select
        :param connection:
        :param sql:
        :return:
        """
        try:
            with self.connection.cursor() as cursor:
                # Create a new record
                cursor.execute(sql)

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            self.connection.commit()
        finally:
            self.connection.close()
        return None

    def query_select(self, sql):
        """
        Receiving response from database
        :param connection:
        :param sql:
        :return:
        """
        try:
            with self.connection.cursor() as cursor:
                # Read a single record
                cursor.execute(sql)
                results = cursor.fetchall()
        finally:
            self.connection.close()
        return results
