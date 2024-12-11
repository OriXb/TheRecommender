from tkinter import *
from tkinter import font
from tkinter import messagebox
from PIL import Image, ImageTk
import db_manager
import data
import brain

# CONST
BLUE_COLOR = "#006ca6"
LIGHT_BLUE_COLOR = "#03d9ff"
DARKER_BLUE = "#2a79b5"
DARKEST_BLUE = "#00518f"


class TestWindow:

    def __init__(self):
        self.window = Tk()
        self.window.title("The Recommender")
        self.window.config(pady=20, padx=20)
        self.window.minsize(1500, 500)
        self.window.config(bg="lightblue")  # רקע בצבע תכלת

        # Images on screen
        self.images_on_screen = []

        # Setup values
        self.setup_brain = brain.Brain()
        self.langs_selected = set()
        self.main_lang = "en"
        self.genres_selected = {"tv": set(), "movie": set()}
        self.loved_content = set()

        # Potential loved content, saved here for setup
        self.contents_to_show = []

        # User info
        self.user_id = str()

        # Grid of 9 by 9
        for row in range(9):
            self.window.grid_rowconfigure(row, weight=1)
        for col in range(9):
            self.window.grid_columnconfigure(col, weight=1)

        TITLE_FONT = font.Font(family="Helvetica", size=28, weight="bold")
        LABEL_FONT = font.Font(family="Arial", size=14)

        # Labels
        self.title_label = Label(self.window, text="The Recommender", font=TITLE_FONT, bg="lightblue", fg=BLUE_COLOR)
        self.title_label.grid(row=0, column=0, columnspan=9, pady=20)  # כיתוב במרכז

        self.instruction_label = Label(self.window, text="Please enter your user or create new one", font=LABEL_FONT,
                                       bg="lightblue")
        self.instruction_label.grid(row=1, column=0, columnspan=9, pady=10)

        # login widgets
        self.create_login_widgets()

    def create_login_widgets(self):
        """
        Create widgets for the login screen.
        """

        user_label = Label(self.window, text="Username:", font=font.Font(family="Arial", size=14), bg="lightblue")
        user_label.grid(row=2, column=2, columnspan=2)
        self.username_entry = Entry(self.window, width=30)
        self.username_entry.grid(row=2, column=4, columnspan=3)

        password_label = Label(self.window, text="Password:", font=font.Font(family="Arial", size=14), bg="lightblue")
        password_label.grid(row=3, column=2, columnspan=2)
        self.password_entry = Entry(self.window, width=30, show="*")
        self.password_entry.grid(row=3, column=4, columnspan=3)

        login_button = Button(self.window, text="Login", font=font.Font(family="Arial", size=14), bg="white",
                              command=self.login)
        login_button.grid(row=4, column=3, columnspan=3, pady=20)

        create_user_button = Button(self.window, text="Create New User", font=font.Font(family="Arial", size=14),
                                    bg="white",
                                    command=self.show_create_user_widgets)
        create_user_button.grid(row=5, column=3, columnspan=3, pady=10)

    def show_create_user_widgets(self):
        """
        Create widgets for the create new user screen.
        """

        self.instruction_label.config(text="Create a New User")
        self.reset_screen_widgets()

        # Create user widgets
        user_label = Label(self.window, text="New Username:", font=font.Font(family="Arial", size=14), bg="lightblue")
        user_label.grid(row=2, column=2, columnspan=2)
        self.new_username_entry = Entry(self.window, width=30)
        self.new_username_entry.grid(row=2, column=4, columnspan=3)

        password_label = Label(self.window, text="New Password:", font=font.Font(family="Arial", size=14),
                               bg="lightblue")
        password_label.grid(row=3, column=2, columnspan=2)
        self.new_password_entry = Entry(self.window, width=30, show="*")
        self.new_password_entry.grid(row=3, column=4, columnspan=3)

        create_button = Button(self.window, text="Create User", font=font.Font(family="Arial", size=14), bg="white",
                               command=self.create_user)
        create_button.grid(row=4, column=3, columnspan=3, pady=20)

    def login(self):
        """
        Function active when user try to connect, check in database if user info known.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()
        if db_manager.is_user_valid(username, password):
            self.show_alert(f"Login succeeded", f"Hello {username}!")
            self.user_id = db_manager.get_user_id(username)
            self.show_main_screen()
        else:
            self.show_alert("Login failed", "Username or password are wrong. Try again.")

    def create_user(self):
        """
        Function to create a new user, and register him in database.
        """
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()

        if db_manager.is_username_taken(new_username):
            self.show_alert("Create user failed", "username already taken")
            return

        db_manager.add_new_user(new_username, new_password)
        self.show_alert("User created", f"Creating user with Username: {new_username}, Password: {new_password}")

        self.reset_to_login_widgets()

    def show_main_screen(self):
        """
        Show main screen widgets.
        """
        for widget in self.window.grid_slaves():
            if widget.grid_info()["row"] != 0:
                widget.grid_forget()

        self.title_label.config(text="Welcome to the Recommender System")

        welcome_label = Label(self.window, text="You have successfully logged in!",
                              font=font.Font(family="Arial", size=18, weight="bold"), bg="lightblue", fg=BLUE_COLOR)
        welcome_label.grid(row=1, column=0, columnspan=9, pady=20)

        # If user already finished setup.
        if db_manager.is_user_active(self.user_id):

            # Go to main menu
            main_menu_button = Button(self.window, text="Go to Main Menu [IN PROGRESS]", font=font.Font(family="Arial", size=28),
                                      bg=LIGHT_BLUE_COLOR, command=self.in_progress_features)
            main_menu_button.grid(row=2, column=3, columnspan=3, pady=10)

            # Reset setup
            main_menu_button = Button(self.window, text="Reset setup", font=font.Font(family="Arial", size=20),
                                      bg=DARKER_BLUE, command=self.setup_menu)
            main_menu_button.grid(row=3, column=3, columnspan=3, pady=10)

            # user settings
            main_menu_button = Button(self.window, text="Settings [IN PROGRESS]", font=font.Font(family="Arial", size=14),
                                      bg=DARKEST_BLUE, command=self.in_progress_features)
            main_menu_button.grid(row=4, column=3, columnspan=3, pady=10)

        # If user didn't already finish setup.
        else:

            # start setup
            main_menu_button = Button(self.window, text="Start Setup", font=font.Font(family="Arial", size=28),
                                      bg=LIGHT_BLUE_COLOR, command=self.setup_menu)
            main_menu_button.grid(row=2, column=3, columnspan=3, pady=10)

            # Manual changes
            main_menu_button = Button(self.window, text="Manual changes [IN PROGRESS]", font=font.Font(family="Arial", size=14),
                                      bg=DARKER_BLUE, command=self.in_progress_features)
            main_menu_button.grid(row=3, column=3, columnspan=3, pady=10)

            # user settings
            main_menu_button = Button(self.window, text="Settings [IN PROGRESS]", font=font.Font(family="Arial", size=12),
                                      bg=DARKEST_BLUE, command=self.in_progress_features)
            main_menu_button.grid(row=4, column=3, columnspan=3, pady=10)

    def in_progress_features(self):
        # For features that dont work yet, so they can be there for testing
        pass

    def setup_menu(self):
        """
        Set setup menu widgets.
        """
        self.reset_screen_widgets()
        self.title_label.config(text="The Recommender Setup")

        desc_label_one = Label(self.window,
                               text="Let us find you the content that best suits you!",
                               font=font.Font(family="Arial", size=18, weight="bold"), bg="lightblue", fg=BLUE_COLOR)
        desc_label_one.grid(column=0, row=1, columnspan=9)

        desc_label_two = Label(self.window,
                               text="Please select the following features you like best from the following options!\n"
                                    "3 short steps and you will immediately receive the movies and shows that will"
                                    " suit you best!"
                               , font=font.Font(family="Arial", size=18), bg="lightblue", fg=DARKER_BLUE)
        desc_label_two.grid(column=0, row=2, columnspan=9, rowspan=2)

        start_setup = Button(self.window, text="Start!", font=font.Font(family="Arial", size=40),
                             bg=DARKER_BLUE, command=self.setup_menu_langs_one)
        start_setup.grid(row=5, column=0, columnspan=9, pady=10)

    def setup_menu_langs_one(self):
        """
        Setup first step-user select known langs.
        """
        self.reset_screen_widgets()
        desc_label_one = Label(self.window,
                               text="Please select the languages you want!",
                               font=font.Font(family="Arial", size=18, weight="bold"), bg="lightblue", fg=BLUE_COLOR)
        desc_label_one.grid(column=0, row=1, columnspan=9)

        desc_label_two = Label(self.window,
                               text="Don't worry! This can be changed later!",
                               font=font.Font(family="Arial", size=12), bg="lightblue", fg=DARKER_BLUE)
        desc_label_two.grid(column=0, row=2, columnspan=9, pady=20)

        langs = data.get_available_langs()

        lang_one_checked = IntVar()
        popular_lang_one = Checkbutton(text=langs[0], variable=lang_one_checked)
        popular_lang_one.grid(column=3, row=3)

        lang_two_checked = IntVar()
        popular_lang_two = Checkbutton(text=langs[1], variable=lang_two_checked)
        popular_lang_two.grid(column=4, row=3)

        lang_three_checked = IntVar()
        popular_lang_three = Checkbutton(text=langs[2], variable=lang_three_checked)
        popular_lang_three.grid(column=5, row=3)

        # Var to store user selections.
        selected_language = StringVar(self.window)
        selected_language.set("Other languages?")  # ערך ברירת המחדל

        langs_to_select = langs[3:]

        # Dropdown to other langs.
        dropdown = OptionMenu(self.window, selected_language, *langs_to_select)
        dropdown.config(width=40)
        dropdown.grid(row=4, column=0, columnspan=9, pady=20)

        # langs that were added by user will be show here.
        langs_added = Label(self.window,
                            text="",
                            font=font.Font(family="Arial", size=12),
                            bg="lightblue", fg=BLUE_COLOR)
        langs_added.grid(column=0, row=5, columnspan=9)

        self.langs_selected = set()

        def reset_langs_selection():
            self.langs_selected.clear()
            langs_added.config(text="")

        def add_language_toview():
            if lang_one_checked.get() == 1:
                self.langs_selected.add(langs[0])
                langs_added.config(text=f"Added: {', '.join(self.langs_selected)}")

            if lang_two_checked.get() == 1:
                self.langs_selected.add(langs[1])
                langs_added.config(text=f"Added: {', '.join(self.langs_selected)}")

            if lang_three_checked.get() == 1:
                self.langs_selected.add(langs[2])
                langs_added.config(text=f"Added: {', '.join(self.langs_selected)}")

            if selected_language.get() != "Other languages?":
                self.langs_selected.add(selected_language.get())
                langs_added.config(text=f"Added: {', '.join(self.langs_selected)}")

            # Add reset selection button
            if len(self.langs_selected) != 0:
                reset_langs = Button(self.window, text="Reset selection", font=font.Font(family="Arial", size=10),
                                     bg=LIGHT_BLUE_COLOR, command=reset_langs_selection)
                reset_langs.grid(row=9, column=0, columnspan=9, pady=10)

        # Add lang button
        add_lang = Button(self.window, text="Add language", font=font.Font(family="Arial", size=30),
                          bg=LIGHT_BLUE_COLOR, command=add_language_toview)
        add_lang.grid(row=6, column=0, columnspan=9, pady=10)

        # checker if user selected yet main lang
        is_selected_main_lang = False

        def try_to_next():
            if len(self.langs_selected) == 0:
                langs_added.config(text="Please add at least 1 language.")
            elif not is_selected_main_lang:
                ask_for_main_lang()

        def move_on_next_setup():
            if selected_main_lang.get() != "Select your main language":
                self.main_lang = selected_main_lang.get()
                self.setup_menu_genres_two()
            else:
                desc_label_one.config(text="Please select to keep going.")

        selected_main_lang = StringVar(self.window)
        selected_main_lang.set("Select your main language")  # ערך ברירת המחדל

        def ask_for_main_lang():

            for widget in self.window.grid_slaves():
                if widget.grid_info()["row"] in range(3, 9):
                    widget.grid_forget()  # hide fields to ask for main lang

            desc_label_one.config(text="")
            desc_label_one.config(text="Which one your main language?")

            main_lang_dropdown = OptionMenu(self.window, selected_main_lang, *self.langs_selected)
            main_lang_dropdown.config(width=40)
            main_lang_dropdown.grid(row=4, column=0, columnspan=9, pady=20)

            next_stage = Button(self.window, text="Next", font=font.Font(family="Arial", size=40),
                                bg=DARKER_BLUE, command=move_on_next_setup)
            next_stage.grid(row=8, column=0, columnspan=9, pady=10)

        keep_going = Button(self.window, text="Next", font=font.Font(family="Arial", size=40),
                            bg=DARKER_BLUE, command=try_to_next)
        keep_going.grid(row=8, column=0, columnspan=9, pady=10)

    def setup_menu_genres_two(self):
        """
        Setup step two-user select loved genres.
        """
        self.reset_screen_widgets()
        desc_label_one = Label(self.window,
                               text="Please select the genres you like!",
                               font=font.Font(family="Arial", size=18, weight="bold"), bg="lightblue", fg=BLUE_COLOR)
        desc_label_one.grid(column=0, row=1, columnspan=9)

        desc_label_two = Label(self.window,
                               text="Please select your loved genres!",
                               font=font.Font(family="Arial", size=12), bg="lightblue", fg=DARKER_BLUE)
        desc_label_two.grid(column=0, row=2, columnspan=9, pady=20)

        # dict of all the genres
        main_lang_code = data.get_lang_code(self.main_lang)
        genres_dict = data.get_geners("tv", main_lang_code) | (data.get_geners("movie", main_lang_code))
        genres_count = len(genres_dict)

        # vars to store if genre checked or not
        check_vars = {key: IntVar() for key, value in genres_dict.items()}

        # create a check button for genre
        count = 0
        start_row_num = 4
        start_column_num = 0

        for genre in genres_dict:
            cb = Checkbutton(text=f"{genres_dict[genre]}", variable=check_vars[genre])
            cb.grid(row=start_row_num, column=start_column_num)

            # change the pos of the button
            if start_column_num + 1 > 8:
                start_row_num += 1
                start_column_num = 0
            else:
                start_column_num += 1

        def try_to_next():

            # clear to prevent errors
            self.genres_selected = {"tv": set(), "movie": set()}
            # to check min selection
            checker = 0

            for key in check_vars:
                if check_vars[key].get() == 1:
                    checker += 1
                    if data.get_genre_type(key) == "both":
                        self.genres_selected["tv"].add(key)
                        self.genres_selected["movie"].add(key)
                    else:
                        self.genres_selected[data.get_genre_type(key)].add(key)
            if checker < 3:
                desc_label_two.config(text="Please select at least 3 loved genres!")
            else:
                self.setup_menu_content_three()

        keep_going = Button(self.window, text="Next", font=font.Font(family="Arial", size=40),
                            bg=DARKER_BLUE, command=try_to_next)
        keep_going.grid(row=9, column=0, columnspan=9, pady=10)

    def setup_menu_content_three(self):
        """
        User select loved content from generated content that he may like based on previous selections.
        and the program after selection analyze the selected content in the Brain and add that info the user data
        in the database.
        """
        self.reset_screen_widgets()
        desc_label_one = Label(self.window,
                               text="We've prepared movies and series that you might enjoy!",
                               font=font.Font(family="Arial", size=18, weight="bold"), bg="lightblue", fg=BLUE_COLOR)
        desc_label_one.grid(column=0, row=1, columnspan=9)

        desc_label_two = Label(self.window,
                               text="Please mark which you liked or found interesting "
                                    "so we can improve our recommendations!",
                               font=font.Font(family="Arial", size=12), bg="lightblue", fg=DARKER_BLUE)
        desc_label_two.grid(column=0, row=2, columnspan=9, pady=20)

        # get content to view
        self.contents_to_show = self.setup_brain.get_setup_recommended_content(
            self.langs_selected, self.main_lang, self.genres_selected)

        if len(self.contents_to_show) != 10:
            raise ValueError("The contents_to_show not = 10.")

        def show_content_options():

            # Clean the before widgets
            for widget in self.window.grid_slaves():
                if widget.grid_info()["row"] in [3, 4, 5, 6, 7, 8]:
                    widget.grid_forget()

            index = 0
            rows = [3, 6]

            check_vars = {x.info["title"]: IntVar() for x in self.contents_to_show}
            for row in rows:
                for column in range(2, 7):  # pass throw 5 columns
                    content_to_view = self.contents_to_show[index]

                    img = Image.open(data.get_poster(content_to_view))  # הכנס את הנתיב לתמונה שלך כאן
                    img = img.resize((100, 150))  # שינוי גודל התמונה לפי הצורך
                    tk_ximg = ImageTk.PhotoImage(img)

                    content_title = Label(self.window, text=content_to_view.info["title"])
                    content_title.grid(column=column, row=row, pady=10)

                    image_label = Label(self.window, image=tk_ximg)
                    image_label.grid(column=column, row=row + 1)

                    check_button = Checkbutton(variable=check_vars[content_to_view.info["title"]])
                    check_button.grid(column=column, row=row + 2)

                    # for the picture to stay on screen need to be saved somewhere so GC not delete
                    self.images_on_screen.append([tk_ximg])

                    index += 1

            return check_vars

        # Active the func that show the recommended content on screen
        # check_vars (vars of the Check Buttons 0 or 1)
        self.check_vars = show_content_options()

        def refresh_content():
            """
            refresh content without saving selection
            """
            # get new content
            self.contents_to_show = self.setup_brain.get_setup_recommended_content(
                self.langs_selected, self.main_lang, self.genres_selected)

            # show on screen
            self.check_vars = show_content_options()

        def save_refresh_content():
            """
            refresh content with saving selection
            """
            for key in self.check_vars:
                if self.check_vars[key].get() == 1:
                    for content in self.contents_to_show:
                        if content.info["title"] == key:
                            self.loved_content.add(content)

            # FOR TESTING IF NEEDED
            #for x in self.loved_content:
            #    print(x.info["title"])

            # refresh with early commend
            refresh_content()

        save_refersh_button = Button(self.window, text="Save and refresh", font=font.Font(family="Arial", size=20),
                                     bg=LIGHT_BLUE_COLOR, command=save_refresh_content)
        save_refersh_button.grid(row=9, column=0, columnspan=9, pady=10)

        refersh_button = Button(self.window, text="Refresh", font=font.Font(family="Arial", size=10),
                                bg=BLUE_COLOR, command=refresh_content)
        refersh_button.grid(row=10, column=0, columnspan=9, pady=10)

        def try_to_next():

            if len(self.loved_content) < 10:
                desc_label_two.config(text="Please select at least 10 movies/shows you like!")
            else:
                self.end_setup()

        keep_going = Button(self.window, text="Next", font=font.Font(family="Arial", size=40),
                            bg=DARKER_BLUE, command=try_to_next)
        keep_going.grid(row=11, column=0, columnspan=9, pady=30)

    def end_setup(self):
        """
        Finished setup screen.
        """
        self.reset_screen_widgets()
        desc_label_one = Label(self.window,
                               text="You finished the setup!",
                               font=font.Font(family="Arial", size=18, weight="bold"), bg="lightblue", fg=BLUE_COLOR)
        desc_label_one.grid(column=0, row=1, columnspan=9)

        desc_label_two = Label(self.window,
                               text="You can now return to main menu and get recommendation "
                                    "based on your style!",
                               font=font.Font(family="Arial", size=12), bg="lightblue", fg=DARKER_BLUE)
        desc_label_two.grid(column=0, row=2, columnspan=9, pady=20)

        desc_label_three = Label(self.window,
                               text="The system will learn from your future selection!"
                                    " but if you think you made a mistake, just click again on the start setup button!",
                               font=font.Font(family="Arial", size=12), bg="lightblue", fg=DARKER_BLUE)
        desc_label_three.grid(column=0, row=3, columnspan=9, pady=20)

        def try_to_next():

            # Give the brain the results of the selected content of the user,
            # and the brain make conclusions of that.
            self.setup_brain.set_loved_content(list(self.loved_content))
            self.setup_brain.print_all()

            self.show_main_screen()

        keep_going = Button(self.window, text="Return to main menu", font=font.Font(family="Arial", size=40),
                            bg=DARKER_BLUE, command=try_to_next)
        keep_going.grid(row=11, column=0, columnspan=9, pady=30)

    def reset_to_login_widgets(self):

        for widget in self.window.grid_slaves():
            if widget.grid_info()["row"] in [2, 3, 4]:
                widget.grid_forget()

        self.instruction_label.config(text="Please enter your user or create new one")  # החזרת ההוראות
        self.create_login_widgets()

    def show_alert(self, msg_title: str, msg: str):
        messagebox.showinfo(msg_title, msg)

    def reset_screen_widgets(self):
        for widget in self.window.grid_slaves():
            if widget.grid_info()["row"] not in [0]:
                widget.grid_forget()

    def run(self):
        self.window.mainloop()
