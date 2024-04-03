from PyQt5.QtWidgets import QMainWindow, QFileSystemModel
from mainwindow import Ui_MainWindow

class PyPassUI(Ui_MainWindow):
    def __init__(self, win):
        self.setupUi(win)
        self.init_pass_store_treeView()


    def init_pass_store_treeView(self):
        self.setup_pass_dir_tree_view()
        self.pass_tree_remove_cols()


    def pass_tree_remove_cols(self):
        self.treeView.hideColumn(1)
        self.treeView.hideColumn(2)
        self.treeView.hideColumn(3)


    def setup_pass_dir_tree_view(self):
        # Abstract to dynamically get user's pass store dir
        passRootPath = '/home/usef/.local/share/pass/'

        self.pass_dir_model = QFileSystemModel()
        self.pass_dir_model.setRootPath(passRootPath)

        self.treeView.setModel(self.pass_dir_model)
        self.treeView.setRootIndex(self.pass_dir_model.index(passRootPath))
