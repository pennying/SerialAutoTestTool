import os
import sys

import pytest
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import *

from ui.Table import MyTable
from utils.ctrlSerial import CtrlSerial
from result.get_result import Result

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 控件
        self.serial_asin = None
        self.btl_asin = None
        self.port_name = "COM1"
        self.baud_rate = "9600"

        # 窗体标题
        self.setWindowTitle("内窥镜串口自动化测试工具")

        # 窗体尺寸
        self.resize(1300, 830)

        # 窗体位置
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)

        # 创建布局
        layout = QVBoxLayout()

        # 1.创建表单
        layout.addLayout(self.init_header())

        # 2.创建表格
        layout.addLayout(self.init_table())

        # # 3.创建文本
        # layout.addLayout(self.init_log_tittle())
        #
        # # 日志打印
        # layout.addLayout(self.init_log_print())

        # 设置排列顺序
        self.setLayout(layout)

    def init_header(self):
        # 1.创建顶部菜单布局
        header_layout = QHBoxLayout()

        product_ver = QLabel("产品型号：", self)
        header_layout.addWidget(product_ver)

        # 输入框
        txt_asin = QLineEdit()
        txt_asin.setPlaceholderText("请输入产品型号")
        header_layout.addWidget(txt_asin)

        serial_ver = QLabel("串口：", self)
        header_layout.addWidget(serial_ver)

        # 输入框
        serial_asin = QLineEdit()
        serial_asin.setPlaceholderText("COM1")
        self.serial_asin = serial_asin
        header_layout.addWidget(serial_asin)

        btl_ver = QLabel("波特率：", self)
        header_layout.addWidget(btl_ver)

        # 输入框
        btl_asin = QLineEdit()
        btl_asin.setPlaceholderText("9600")
        self.btl_asin = btl_asin
        header_layout.addWidget(btl_asin)

        # stop_ver = QLabel("停止位：", self)
        # header_layout.addWidget(stop_ver)
        #
        # # 输入框
        # stop_asin = QLineEdit()
        # stop_asin.setPlaceholderText("1")
        # header_layout.addWidget(stop_asin)
        #
        # data_ver = QLabel("数据位：", self)
        # header_layout.addWidget(data_ver)
        #
        # # 输入框
        # data_asin = QLineEdit()
        # data_asin.setPlaceholderText("8")
        # header_layout.addWidget(data_asin)
        #
        # check_ver = QLabel("校验位：", self)
        # header_layout.addWidget(check_ver)
        #
        # # 输入框
        # check_asin = QLineEdit()
        # check_asin.setPlaceholderText("None")
        # header_layout.addWidget(check_asin)

        # 确认按钮
        serial_start = QPushButton("打开串口")
        serial_start.clicked.connect(self.event_start_serial)
        header_layout.addWidget(serial_start)

        # 确认按钮
        serial_stop = QPushButton("关闭串口")
        serial_stop.clicked.connect(self.event_stop_serial)
        header_layout.addWidget(serial_stop)

        # 弹簧
        header_layout.addStretch()
        header_layout.addStretch()

        # 创建按钮
        btn_start = QPushButton("开始测试")
        btn_start.clicked.connect(self.event_start_test)
        header_layout.addWidget(btn_start)

        btn_stop = QPushButton("停止测试")
        header_layout.addWidget(btn_stop)

        return header_layout

    def init_table(self):

        table_layout = QHBoxLayout()

        self.table_widget = myTable = MyTable()
        # # 创建表格
        # self.table_widget = table_widget = QTableWidget(25, 5)
        # table_header = [
        #     {"field": "test", "text": "测试内容", "width": 200},
        #     {"field": "send", "text": "发送命令", "width": 300},
        #     {"field": "receive", "text": "接收命令", "width": 300},
        #     {"field": "result", "text": "测试结果", "width": 150},
        #     {"field": "tip", "text": "备注", "width": 300}
        # ]
        #
        # for idx, info in enumerate(table_header):
        #     item = QTableWidgetItem()
        #     item.setText(info["text"])
        #     table_widget.setHorizontalHeaderItem(idx, item)
        #     table_widget.setColumnWidth(idx, info["width"])

        # # 初始化表格数据
        # import json
        # file_path = os.path.join(BASE_DIR, "db", "db.json")
        # with open(file_path, mode="r", encoding="utf-8") as f:
        #     data = f.read()
        # self.data_list = json.loads(data)
        # print(self.data_list)

        # current_row_count = table_widget.rowCount()
        # for row_list in self.data_list:
        #     table_widget.insertRow(current_row_count)
        #
        #     for i, ele in enumerate(row_list):
        #         cell = QTableWidgetItem(str(ele))
        #         table_widget.setItem(current_row_count, i, cell)
        #
        #     current_row_count += 1

        table_layout.addWidget(self.table_widget)
        return table_layout

    # def init_log_tittle(self):
    #     # 3.创建文本
    #     log_tittle_layout = QHBoxLayout()
    #     log_tittle = QLabel("日志", self)
    #     log_tittle_layout.addWidget(log_tittle)
    #
    #     return log_tittle_layout
    #
    # def init_log_print(self):
    #     log_layout = QHBoxLayout()
    #     # 输入框
    #     txt_asin = QLineEdit()
    #     log_layout.addWidget(txt_asin)
    #
    #     return log_layout

    def event_start_serial(self):
        self.port_name = self.serial_asin.text()
        self.baud_rate = self.btl_asin.text()
        if not self.port_name or not self.baud_rate:
            QMessageBox.warning(self, "错误", "请检查串口信息")
            return
        ctrl_serial = CtrlSerial(self.port_name, self.baud_rate)
        ctrl_serial.open_serial()

    def event_stop_serial(self):
        ctrl_serial = CtrlSerial(self.port_name, self.baud_rate)
        ctrl_serial.close_serial()

    def event_start_test(self):

        # 执行测试并获取结果
        # 不能在主线程执行，需创建一个线程执行测试，将结果再更新到窗体应用（信号）
        # from utils.threads import NewTaskThread
        # NewTaskThreadObj = NewTaskThread()
        # # NewTaskThreadThd = QThread()
        # # NewTaskThreadObj.moveToThread(NewTaskThreadThd)
        # NewTaskThreadObj.success.connect(self.init_task_success_callback)
        # NewTaskThreadObj.start()
        # pass

        ctrl_serial = CtrlSerial(self.port_name, self.baud_rate)

        current_row_count = 0
        print("current_row_count = " + str(current_row_count))

        # 获取数据
        import json
        file_path = os.path.join(BASE_DIR, "db", "db.json")
        with open(file_path, mode="r", encoding="utf-8") as f:
            data = f.read()
        data_list = json.loads(data)
        print(data_list)

        for row_list in data_list:
            # self.table_widget.insertRow(current_row_count)
            print("row_list = " + str(row_list))

            for j, ele in enumerate(row_list):

                cell = QTableWidgetItem(str(ele))
                self.table_widget.setItem(current_row_count, j, cell)
                self.table_widget.viewport().update()

                if j == 1:
                    send_c = bytes.fromhex(ele)
                    # print("send_c = " + str(self.send_c))

            # 执行测试用例
            if ctrl_serial.send_and_receive_command(id=1, cmd=row_list[0], send_c=send_c, expect=row_list[2]):
                result = "Pass"
            else:
                result = "Fail"

            print("result = " + result)
            result = result

            # 加到表格
            result = QTableWidgetItem(result)
            self.table_widget.setItem(current_row_count, 3, result)
            self.table_widget.viewport().update()

            current_row_count += 1

        # pytest.main(["./case/.", "-vk", "test_01_send_command",
        #              "--json-report", f"--json-report-file=./result/report.json"])
        #
        # # 拿到测试结果
        # result_list = Result.get_result_list()
        # print(result_list)
        #
        # # 加到表格
        # current_row_count = self.table_widget.rowCount()
        # for i, ele in enumerate(result_list):
        #     cell = QTableWidgetItem(str(ele))
        #     self.table_widget.setItem(i, 3, cell)

    def init_task_success_callback(self, index, tittle, result):
        # 更新窗体显示的数据
        print(index, tittle, result)
        pass


if __name__ == "__main__":
    # 创建QApplication对象
    app = QApplication(sys.argv)
    window = MainWindow()

    # 显示窗口
    window.show()

    # 进入事件循环
    sys.exit(app.exec_())


