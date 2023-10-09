import pymysql
from tkinter import messagebox


class Database:
    def __init__(self):
        self.connection = None
        self.host = '120.53.45.165'
        self.port = 3306
        self.user = 'feng'
        self.password = '123456'
        self.database = 'guess_word_game'

    def get_data_random(self, table: str) -> str:
        """获取指定数据表的随意一行数据"""
        try:
            with self.connection.cursor() as cursor:
                query = f"SELECT * FROM {table} ORDER BY RAND() LIMIT 1"
                cursor.execute(query)
                random_row = cursor.fetchone()[0]
                return random_row
        except Exception as e:
            messagebox.showerror("获取数据错误", str(e))

    def insert_data(self, table: str, data: dict[str]) -> None:
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
            messagebox.showerror('数据库插入数据异常', str(e))

    def close_database(self) -> None:
        """关闭数据库"""
        if self.connection:
            self.connection.close()

    def connect_database(self) -> None:
        """连接数据库"""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except Exception as e:
            messagebox.showerror('数据库连接异常', str(e) + "\n请重启应用...")
