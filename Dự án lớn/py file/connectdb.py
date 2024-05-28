import mysql.connector
from mysql.connector import Error

class DatabaseConnect:
    def __init__(self):
        self.user='root'
        self.password= '123456'
        self.host= 'localhost'
        self.database= 'ql'
        self.table_name= 'duck'
        self.connection = None
        self.cursor = None

        self.init_database()
    
    def init_database(self):
        self.connector()
        try:
            sql = f"SHOW TABLES LIKE '{self.table_name}'"
            self.cursor.execute(sql)
            result = self.cursor.fetchone()

            if result:
                return
            else:
                sql = f"""
                    CREATE TABLE `{self.table_name}` (
                    `product_name` VARCHAR(255) NOT NULL,
                    `cost` DECIMAL(10, 2),
                    `price` DECIMAL(10, 2),
                    `location` INT,
                    `reorder_level` INT,
                    `stock` INT DEFAULT 0,
                    PRIMARY KEY (`product_name`)
                    );
                    """
                self.cursor.execute(sql)
                self.connection.commit()

        except Error as e:
            self.connection.rollback()
            return e
        
        finally:
            self.cursor.close()
            self.connection.close()

    def connector(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
        except Error as e:
            print(f"Error: {e}")
            return e

    def common_update_execute(self, sql):
        self.connector()
        try:
            self.cursor.execute(sql)
            self.connection.commit()

        except Error as e:
            self.connection.rollback()
            return e
        
        finally:
            self.cursor.close()
            self.connection.close()

    def common_search_one_execute(self, sql):
        self.connector()
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            return result
        
        except Error as e:
            print(f"Error: {e}")
            return None
        
        finally:
            self.cursor.close()
            self.connection.close()

    def common_search_all_execute(self, sql):
        self.connector()
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        
        except Error as e:
            print(f"Error: {e}")
            return None
        
        finally:
            self.cursor.close()
            self.connection.close()

    def get_all_location(self):
        sql = f"SELECT DISTINCT location FROM {self.table_name};"
        result = self.common_search_all_execute(sql=sql)
        return result
    
    def add_new_product(self, **kwargs):
        column_name = tuple(kwargs.keys())
        values = tuple(kwargs.values())

        sql = f"INSERT INTO {self.table_name} {column_name} VALUES {values};"
        result = self.common_update_execute(sql=sql)
        return result
    
    def update_product(self, **kwargs):
        values = tuple(kwargs.values())

        sql = f""" UPDATE {self.table_name} SET
                    cost={kwargs['cost']},
                    price={kwargs['price']},
                    location={kwargs['location']},
                    reorder_level={kwargs['reorder_level']},
                    stock={kwargs['stock']}
                   WHERE product_name='{values[0]}';
            """
        
        result = self.common_update_execute(sql=sql)
        return result
    
    def get_data(self, search_flag="", product_name=""):
        if search_flag == "ALL":
            sql = f"SELECT product_name, cost, price, stock, location, reorder_level FROM {self.table_name}"
        elif search_flag == "IN_STOCK":
            sql = (f"SELECT product_name, cost, price, stock, location, reorder_level FROM {self.table_name} "
                   f"WHERE stock > 0")
        elif search_flag == "NO_STOCK":
            sql = (f"SELECT product_name, cost, price, stock, location, reorder_level FROM {self.table_name} "
                   f"WHERE stock <= 0")
        elif search_flag == "RE_ORDER":
            sql = (f"SELECT product_name, cost, price, stock, location, reorder_level FROM {self.table_name} "
                   f"WHERE stock <= reorder_level")
        else:
            sql = (f"SELECT product_name, cost, price, stock, location, reorder_level FROM {self.table_name} "
                   f"WHERE product_name = '{product_name}'")
            
        result = self.common_search_all_execute(sql=sql)
        return result
    
    def delete_product(self, product_name):
        sql = f"DELETE FROM {self.table_name} WHERE product_name='{product_name}'"
        result = self.common_update_execute(sql=sql)
        return result
    
    def get_product_names(self, product_name):
        sql = (f"SELECT product_name FROM {self.table_name} "
               f"WHERE product_name LIKE '%{product_name}%'")
        search_result = self.common_search_all_execute(sql=sql)
        return search_result

    def get_single_product_info(self, product_name):
        sql = (f"SELECT stock, reorder_level, location FROM {self.table_name} "
               f"WHERE product_name = '{product_name}'")
        search_result = self.common_search_one_execute(sql=sql)
        return search_result

    def get_current_stock(self, product_name):
        sql = f"SELECT SUM(stock) FROM {self.table_name}"
        search_result = self.common_search_one_execute(sql=sql)
        return search_result

    def get_stock_value(self):
        sql = f"SELECT SUM(price * stock) FROM {self.table_name}"
        search_result = self.common_search_one_execute(sql=sql)
        return search_result     

    def get_stock_cost(self):
        sql = f"SELECT SUM(cost * stock) FROM {self.table_name}"
        search_result = self.common_search_one_execute(sql=sql)
        return search_result

    def get_reorder_product(self):
        sql = f"SELECT COUNT(*) FROM {self.table_name} WHERE reorder_level >= stock"
        search_result = self.common_search_one_execute(sql=sql)
        return search_result

    def get_no_stock_product(self):
        sql = f"SELECT COUNT(*) FROM {self.table_name} WHERE stock <= 0"
        search_result = self.common_search_one_execute(sql=sql)
        return search_result
    
    def update_stock(self, **kwargs):
        sql = f""" UPDATE {self.table_name} SET
                    stock = {kwargs['stock']}
                   WHERE product_name='{kwargs['product_name']}';
                """
        result = self.common_update_execute(sql)
        return result
