from PyQt6 import QtWidgets, uic
from connectdb import DatabaseConnect

class NewProductWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("New_Product.ui", self)
        self.new_product_save_btn = self.ui.pushButton
        self.new_product_cancel_btn = self.ui.pushButton_2
        
        self.product_name = self.ui.lineEdit
        self.cost = self.ui.doubleSpinBox
        self.price = self.ui.doubleSpinBox_2
        self.location = self.ui.comboBox
        self.reorder_level = self.ui.spinBox
        self.stock = self.ui.spinBox_2

        self.Connect_DB = DatabaseConnect()

        self.new_product_save_btn.clicked.connect(self.add_new_product)
        self.new_product_cancel_btn.clicked.connect(self.clear_data)

    def new_product_data(self):
        product_name = self.product_name.text().strip()
        cost = self.cost.value()
        price = self.price.value()
        location = self.location.currentText()
        reorder_level = self.reorder_level.value()
        stock = self.stock.value()

        data_list = [product_name, location]
        bool_data_list = list(map(lambda item: bool(item), data_list))

        if False in bool_data_list:
            return None
        else:
            data_dict = {
                "product_name": product_name,
                "cost": cost,
                "price": price,
                "location": location,
                "reorder_level": reorder_level,
                "stock": stock,
            }

            return data_dict
    
    def add_new_product(self):
        product_data = self.new_product_data()
        
        if product_data:
            add_result = self.Connect_DB.add_new_product(**product_data)
            if isinstance(add_result, Exception):
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to add product: {add_result}")
            else:
                QtWidgets.QMessageBox.information(self, "Success", "Thêm mới thành công")
                self.clear_data()
        else:
            QtWidgets.QMessageBox.warning(self, "Warning", "Thiếu thông tin")
        
    def clear_data(self):
        self.product_name.clear()
        self.cost.setValue(0)
        self.price.setValue(0)
        self.location.clear()
        self.reorder_level.setValue(0)
        self.stock.setValue(0)
