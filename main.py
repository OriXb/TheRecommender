import ui
import db_manager

window = ui.TestWindow()
window.run()

db_manager.connection.close()
