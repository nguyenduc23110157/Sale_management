from PyQt6 import QtWidgets, uic
from connectdb import DatabaseConnect

class UpdateStockWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('Update_Stock.ui', self)

        self.submit_btn = self.ui.pushButton
        self.select_btn = self.ui.pushButton_2
        
        self.input_product_name = self.ui.lineEdit
        self.show_product_name = self.ui.lineEdit_2
        self.product_name_list = self.ui.listWidget
        self.new_stock = self.ui.spinBox

        self.in_radio_btn = self.ui.radioButton
        self.out_radio_btn = self.ui.radioButton_2

        self.Connect_DB = DatabaseConnect()

        self.init_search_dialog()

        self.input_product_name.textChanged.connect(self.update_product_name_list)
        self.select_btn.clicked.connect(self.select_product)
        self.submit_btn.clicked.connect(self.submit)

    def init_search_dialog(self):
        search_result = self.Connect_DB.get_product_names("")
        product_name_list = [item[0] for item in search_result]
        self.product_name_list.addItems(product_name_list)

    def update_product_name_list(self, text):
        self.product_name_list.clear()
        search_result = self.Connect_DB.get_product_names(text)
        product_name_list = [item[0] for item in search_result]
        self.product_name_list.addItems(product_name_list)

    def select_product(self):
        product_name = self.product_name_list.currentItem().text()
        self.show_product_name.setText(product_name)

    def submit(self):
        product_name = self.show_product_name.text()
        if product_name:
            original_stock = self.Connect_DB.get_single_product_info(product_name=product_name)[0]
            update_stock = self.new_stock.value()

            if self.in_radio_btn.isChecked():
                stock = original_stock + update_stock
            else:
                stock = original_stock - update_stock

            update_result = self.Connect_DB.update_stock(product_name=product_name, stock=stock)
            QtWidgets.QMessageBox.information(self, "Success", "Cập nhật thành công!" if update_result > 0 else "Cập nhật thất bại")
            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, "Warning", "Chọn một sản phẩm")

