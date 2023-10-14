import pymysql
from tkinter import messagebox


class DelError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Database:
    def __init__(self):
        self.connection = None
        self.host = '120.53.45.165'
        self.port = 3306
        self.user = 'feng'
        self.password = '123456'
        self.database = 'guess_word_game'

    def create_table(self, table_name: str, columns: list) -> None:
        """创建数据表"""
        try:
            with self.connection.cursor() as cursor:
                sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"
                cursor.execute(sql)
                self.connection.commit()
        except pymysql.Error as e:
            messagebox.showerror("创建数据表错误", str(e))

    def del_data(self, table: str, unique_key: str, column_name: str) -> None:
        """删除数据"""
        with self.connection.cursor() as cursor:
            # 先查询是否存在该数据
            query = f"SELECT * FROM {table} WHERE {column_name} = '{unique_key}'"
            cursor.execute(query)
            if cursor.fetchone() is not None:
                # 删除主键对应数据
                sql = f"DELETE FROM {table} WHERE {column_name} = '{unique_key}'"
                cursor.execute(sql)
                self.connection.commit()
            else:
                raise DelError("删除数据错误")

    def get_data_all(self, table: str) -> tuple:
        """获取表的全部数据"""
        try:
            with self.connection.cursor() as cursor:
                query = f"SELECT * FROM {table}"
                cursor.execute(query)
                word_tuple = cursor.fetchall()
            return word_tuple
        except pymysql.Error as e:
            messagebox.showerror("数据库获取数据错误", str(e))

    def get_data(self, table: str, unique_key: str, column_name: str) -> tuple:
        """获取数据"""
        try:
            with self.connection.cursor() as cursor:
                # 查询主键对应数据
                query = f"SELECT * FROM {table} WHERE {column_name} = '{unique_key}'"
                cursor.execute(query)
                row = cursor.fetchone()
            return row
        except Exception as e:
            messagebox.showerror("获取数据异常", str(e))

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
        """向表中插入数据"""
        with self.connection.cursor() as cursor:
            # 构建 SQL 插入语句
            columns = ', '.join(data.keys())
            values = ', '.join(['%s' for _ in data])
            sql = f"INSERT INTO {table} ({columns}) VALUES ({values})"

            # 执行插入操作
            cursor.execute(sql, tuple(data.values()))
            self.connection.commit()

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
