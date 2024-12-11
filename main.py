import ui
import db_manager

# Active the program ui.
window = ui.TestWindow()
window.run()

# Close connection to DB after program closed.
db_manager.connection.close()
