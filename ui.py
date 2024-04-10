from PyQt5.QtWidgets import QMainWindow, QFileSystemModel
from PyQt5.QtCore import Qt, QSortFilterProxyModel
from mainwindow import Ui_MainWindow
from pass_store import Pass
import os

class PyPassUI(Ui_MainWindow):
    def __init__(self, win):
        self.setupUi(win) # inherited from Ui_MainWindow class
        self.init_pass_store_treeView()
        self.setup_toolbar_actions()


    def setup_toolbar_actions(self):
        self.connect_button_to_show_password()
        self.connect_button_to_copy_password()
        self.connect_button_to_copy_otp()


    def get_path_from_selected_item(self):
        selection_model = self.treeView.selectionModel()
        selected_indexes = selection_model.selectedIndexes()

        if not selected_indexes: return

        sourceIndex = self.search_filter_proxy_model.mapToSource(selected_indexes[0])
        fp = self.pass_dir_model.filePath(sourceIndex)

        if fp[-4:] != '.gpg': return
        
        path = fp.replace(self.passRootPath + '/', '', 1)
        path = path.replace('.gpg', '', 1)

        return path


    def copy_otp(self):
        self.textBrowser.clear()
        path = self.get_path_from_selected_item()
        if path:
            password = Pass()
            password.copy_otp_from_path(path)
        self.textBrowser.append('Copied OTP for password: ' + path)


    def copy_password(self):
        self.textBrowser.clear()
        path = self.get_path_from_selected_item()
        if path:
            password = Pass()
            password.copy_password_from_path(path)
        self.textBrowser.append('Copied password: ' + path)


    def show_password(self):
        self.textBrowser.clear()
        path = self.get_path_from_selected_item()
        if path:
            password = Pass()
            self.textBrowser.append(path + ':\n--------\n\n' + password.show_password_from_path(path))


    def connect_button_to_copy_otp(self):
        self.actionCopy_OTP.triggered.connect(self.copy_otp)


    def connect_button_to_copy_password(self):
        self.actionCopy_Password.triggered.connect(self.copy_password)


    def connect_button_to_show_password(self):
        self.actionShow_Password.triggered.connect(self.show_password)


    def init_pass_store_treeView(self):
        # Set up filesystem model and filter model to display in tree view
        self.setup_pass_dir_tree_view()

        # Remove size, modified date, etc. as it's not needed. We just want name
        self.pass_tree_remove_cols()

        # Clicking reset button reverts back to the original unfiltered model
        self.pushButton.clicked.connect(self.setup_pass_dir_tree_view)


    def on_button_click_reset_dir_view(self):
        self.lineEdit.setText('')
        self.setup_pass_dir_tree_view()


    def setup_pass_dir_tree_view(self):
        try:
            self.passRootPath = os.getenv('PASSWORD_STORE_DIR')
            print('PASSWORD_STORE_DIR = ' + self.passRootPath)
        except:
            self.passRootPath = '/home/usef/.local/share/pass'
            print('Error finding $PASSWORD_STORE_DIR')
            print('Defaulting to: ' + self.passRootPath)

        # Base filesystem model based on the pass root path
        self.pass_dir_model = QFileSystemModel()
        self.pass_dir_model.setRootPath(self.passRootPath)

        # Create the filter proxy model (wrapper for base model with filtering)
        self.search_filter_proxy_model = QSortFilterProxyModel()
        self.search_filter_proxy_model.setSourceModel(self.pass_dir_model)
        self.search_filter_proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.search_filter_proxy_model.setRecursiveFilteringEnabled(True)

        # Model of the tree View should be set to the filter proxy, not the base
        # That way the tree View will always show the filtering output not just
        # the base
        self.treeView.setModel(self.search_filter_proxy_model)

        # Set the index of the view to the pass root path as opposed to '/'
        rootIndex = self.pass_dir_model.index(self.passRootPath)
        self.treeView.setRootIndex(self.search_filter_proxy_model.mapFromSource(rootIndex))

        # Connect the textChanged signal from the lineEdit to the filtering of
        # the filter proxy model. Accordingly it will update the proxy output
        # which will be displayed in the tree View
        self.lineEdit.textChanged.connect(self.update_pass_filter)

        self.selectionModel = self.treeView.selectionModel()
#         self.selectionModel.selectionChanged.connect(self.on_selection_get_password)


    def pass_tree_remove_cols(self):
        self.treeView.hideColumn(1)
        self.treeView.hideColumn(2)
        self.treeView.hideColumn(3)


    def update_pass_filter(self, text):
        search_criteria = text
        self.search_filter_proxy_model.setFilterRegExp(search_criteria)
