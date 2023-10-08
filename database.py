import pymysql


class Database:
    def __init__(self):
        self.connection = None

    def insert_data(self, table: str, data: dict):
        """插入数据"""
        try:
            with self.connection.cursor() as cursor:
                # 构建 SQL 插入语句
                columns = ', '.join(data.keys())
                values = ', '.join(['%s' for _ in data])
                sql = f"INSERT INTO {table} ({columns}) VALUES ({values})"

                # 执行插入操作
                cursor.execute(sql, tuple(data.values()))
                self.connection.commit()
        except pymysql.Error as e:
            print(f"Error: {e}")

    def close_database(self):
        """关闭数据库"""
        if self.connection:
            self.connection.close()

    def connect_database(self):
        """连接数据库"""
        try:
            self.connection = pymysql.connect(
                host='120.53.45.165',
                port=3306,
                user='feng',
                password='123456',
                database='guess_word_game'
            )
        except Exception as e:
            print("异常:", e)
