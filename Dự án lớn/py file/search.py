from PyQt6 import QtWidgets, uic
from connectdb import DatabaseConnect

class SearchWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("Search.ui", self)

        self.Connect_DB = DatabaseConnect()

        self.product_name_LW = self.ui.listWidget
        self.input_product_name_LE = self.ui.lineEdit
        self.current_stock_label = self.ui.label_2
        self.reorder_label = self.ui.label_4
        self.location_number_label = self.ui.label_6

        self.all_product_btn = self.ui.pushButton
        self.current_stock_btn = self.ui.pushButton_2
        self.reorder_btn = self.ui.pushButton_3
        self.no_stock_btn = self.ui.pushButton_4
        self.detail_btn = self.ui.pushButton_5

        self.init_search_dialog()

        self.input_product_name_LE.textChanged.connect(self.update_product_name_list)
        self.product_name_LW.currentTextChanged.connect(self.search_product_info)
        self.detail_btn.clicked.connect(self.get_more_detail)
        self.all_product_btn.clicked.connect(self.get_all_products)
        self.current_stock_btn.clicked.connect(self.get_in_stock_product)
        self.reorder_btn.clicked.connect(self.get_reorder_product)
        self.no_stock_btn.clicked.connect(self.get_no_stock_product)

    def init_search_dialog(self):
        search_result = self.Connect_DB.get_product_names("")
        product_name_list = [item[0] for item in search_result]
        self.product_name_LW.addItems(product_name_list)
      
        self.current_stock_label.setText("-")
        self.reorder_label.setText("-")
        self.location_number_label.setText("-")

    def get_more_detail(self):
        product_name_obj = self.ui.listWidget.currentItem()
        if product_name_obj:
            product_name = product_name_obj.text()
            data = self.Connect_DB.get_data(product_name=product_name)
            self.close()
            return data
        else:
            QtWidgets.QMessageBox.warning(self, "Warning", "Xin hãy chọn một mặt hàng.")
            return None
        
    def get_in_stock_product(self):
        data = self.Connect_DB.get_data(search_flag="IN_STOCK")
        self.close()
        return data  
    
    def get_reorder_product(self):
        data = self.Connect_DB.get_data(search_flag="RE_ORDER")
        self.close()
        return data  
    
    def get_no_stock_product(self):
        data = self.Connect_DB.get_data(search_flag="NO_STOCK")
        self.close()
        return data  
    
    def get_all_products(self):
        data = self.Connect_DB.get_data(search_flag="ALL")
        self.close()
        return data  
    
    def search_product_info(self, product_name):
        if product_name:
            search_result = self.Connect_DB.get_single_product_info(product_name=product_name)
            if search_result:
                self.current_stock_label.setText(str(search_result[0]))
                if search_result[0] > search_result[1]:
                    self.reorder_label.setText("No")
                else:
                    self.reorder_label.setText("Yes")
                self.location_number_label.setText(str(search_result[2]))
            else:
                self.current_stock_label.setText("-")
                self.reorder_label.setText("-")
                self.location_number_label.setText("-")
        else:
            self.current_stock_label.setText("-")
            self.reorder_label.setText("-")
            self.location_number_label.setText("-")

    def update_product_name_list(self, text):
        self.product_name_LW.clear()
        search_result = self.Connect_DB.get_product_names(text)
        product_name_list = [item[0] for item in search_result]
        self.product_name_LW.addItems(product_name_list)

