import random

from content_manager import Content
import data


class Brain:

    def __init__(self):
        self.loved_genres_selected = {"tv": set(), "movie": set()}  # {}

        self.loved_genres_generator = {"tv": set(), "movie": set()}  # {}
        self.loved_original_lang = set()
        self.loved_content_origin = set()
        self.loved_actors = set()
        self.loved_directors = set()

        # var for setup
        self.already_viewed = {"content": set(),
                               "pages": {
                                   "get_popular_tvshows": 1,
                                   "get_popular_movies": 1,
                                   "get_content_by_genre": 1,
                                   "get_rated_content": 1,
                                   "get_tvshows_onair": 1
                               }}

    def set_loved_genres(self, loved_genres: set):
        self.loved_genres_selected = loved_genres

    def set_loved_content(self, loved_content: list):

        content_count = len(loved_content)

        # dict that track the number a genre apper in loved movies & shows
        potential_loved_genres = {}

        # number of the avg popularity of the popularity rating in the selected movies & shows
        # that can indicate whether the user prefer more or less popular content
        sum_popularity = 0
        final_avg_popularity = 0

        # the lang that apper in most selected shows/movies
        potential_loved_langs = {"en": 0}

        # the origin of the content that is most selected
        potential_loved_content_origin = {"rated": 0, "popular": 0, "onair": 0}

        # the actors of the content that is most selected
        potential_loved_actors = {"NAME": 0}

        # the director of the content that is most selected
        potential_loved_directors = {"NAME": 0}

        for content in loved_content:

            content_info = content.info
            content_actors = content.team["cast"]

            # GENRES
            for genre in content_info["genre_ids"]:
                if genre in potential_loved_genres:
                    potential_loved_genres[genre] = potential_loved_genres[genre] + 1
                else:
                    potential_loved_genres[genre] = 1

            # sum_popularity = sum_popularity + movie["popularity"]

            # LANGS
            if content_info["original_language"] in potential_loved_langs:
                potential_loved_langs[content_info["original_language"]] = \
                    potential_loved_langs[content_info["original_language"]] + 1
            else:
                potential_loved_langs[content_info["original_language"]] = 1

            # content_origin
            if content.content_origin in potential_loved_content_origin:
                potential_loved_content_origin[content.content_origin] = \
                    potential_loved_content_origin[content.content_origin] + 1
            else:
                potential_loved_content_origin[content.content_origin] = 1

            # ACTORS
            if len(content_actors) > 3:
                for actor_number in range(0, 3):  # Will take the top 3 actors of the content
                    if content_actors[actor_number]["name"] in potential_loved_actors:
                        potential_loved_actors[content_actors[actor_number]["name"]] = \
                            potential_loved_actors[content_actors[actor_number]["name"]] + 1
                    else:
                        potential_loved_actors[content_actors[actor_number]["name"]] = 1
            elif len(content_actors) > 0:
                if content_actors[0]["name"] in potential_loved_actors:
                    potential_loved_actors[content_actors[0]["name"]] = \
                        potential_loved_actors[content_actors[0]["name"]] + 1
                else:
                    potential_loved_actors[content_actors[0]["name"]] = 1

            # DIRECTOR
            for team_member in content.team["crew"]:
                if team_member["job"] == "Director":
                    if team_member["name"] in potential_loved_directors:
                        potential_loved_directors[team_member["name"]] = \
                            potential_loved_directors[team_member["name"]] + 1
                    else:
                        potential_loved_directors[team_member["name"]] = 0
                    break

        for genre in potential_loved_genres:
            if potential_loved_genres[genre] > (content_count / 3):
                genre_type = data.get_genre_type(genre)
                if genre_type == "both":
                    self.loved_genres_generator["tv"].add(genre)
                    self.loved_genres_generator["movie"].add(genre)
                else:
                    self.loved_genres_generator[genre_type].add(genre)

        for lang in potential_loved_langs:
            if potential_loved_langs[lang] > (content_count / 3):
                self.loved_original_lang.add(lang)

        for content_origin in potential_loved_content_origin:
            if potential_loved_content_origin[content_origin] > (content_count / 2):
                self.loved_content_origin.add(content_origin)

        for actor in potential_loved_actors:
            if content_count > 10:
                if potential_loved_actors[actor] > (
                        content_count / 5):  # if count bigger than 10 go by if more than 20%
                    self.loved_actors.add(actor)
            elif potential_loved_actors[actor] > 2:
                self.loved_actors.add(actor)

        for director in potential_loved_directors:
            if content_count > 10:
                if potential_loved_directors[director] > (content_count / 5):  # bigger than 10 go by if more than 20%
                    self.loved_directors.add(director)
            elif potential_loved_directors[director] > 2:
                self.loved_directors.add(director)

        # self.loved_avg_popularity = (sum_popularity / movies_count)

    def set_selected_genres(self, genres: set):
        self.loved_genres_selected = genres

    def get_loved_origins(self):
        return self.loved_content_origin

    def get_loved_langs(self):
        return self.loved_original_lang

    def get_loved_directors(self):
        return self.loved_directors

    def get_loved_actors(self):
        return self.loved_actors

    def get_loved_genres(self):
        return self.loved_genres_generator.union(self.loved_genres_selected)

    def print_all(self):
        print(self.loved_content_origin)
        print(self.loved_original_lang)
        print(self.loved_directors)
        print(self.loved_actors)
        print(self.loved_genres_generator)

    def get_setup_recommended_content(
            self, langs_selected: set, main_lang: str, genres_selected: dict):
        """
        Get 10 contents (2 rows of 5) to show in the setup for user to select.
        """

        def get_popular_tvshows(amount: int):

            to_be_returned = []

            # if already view those pages, keep going
            from_page = self.already_viewed["pages"]["get_popular_tvshows"]
            to_page = from_page
            # Pick random lang from selected langs
            lang = random.choice(list(langs_selected))
            data_list = data.get_popular_tvshows(from_page=from_page, to_page=to_page,
                                                 language_code=data.get_lang_code(lang))
            index = 0

            for x in range(0, amount):
                if len(data_list) <= index:
                    index = 0
                    # If not enough content, get more
                    self.already_viewed["pages"]["get_popular_tvshows"] += 1
                    from_page = from_page + 1
                    to_page = to_page + 1
                    data_list = data.get_popular_tvshows(from_page=from_page, to_page=to_page,
                                                         language_code=data.get_lang_code(lang))

                while data_list[index].info["title"] in self.already_viewed["content"]:
                    index = index + 1
                    if len(data_list) <= index:
                        index = 0
                        # If not enough content, get more
                        self.already_viewed["pages"]["get_popular_tvshows"] += 1
                        from_page = from_page + 1
                        to_page = to_page + 1
                        data_list = data.get_popular_tvshows(from_page=from_page, to_page=to_page,
                                                             language_code=data.get_lang_code(lang))

                to_be_returned.append(data_list[index])
                index = index + 1

            for viewd in to_be_returned:
                self.already_viewed["content"].add(viewd.info["title"])
            return to_be_returned

        def get_popular_movies(amount: int):

            to_be_returned = []

            # if already view those pages, keep going
            from_page = self.already_viewed["pages"]["get_popular_movies"]
            to_page = from_page
            # Pick random lang from selected langs
            lang = random.choice(list(langs_selected))
            data_list = data.get_popular_movies(from_page=from_page, to_page=to_page,
                                                language_code=data.get_lang_code(lang))
            index = 0

            for x in range(0, amount):
                if len(data_list) <= index:
                    index = 0
                    # If not enough content, get more
                    self.already_viewed["pages"]["get_popular_movies"] += 1
                    from_page = from_page + 1
                    to_page = to_page + 1
                    data_list = data.get_popular_movies(from_page=from_page, to_page=to_page,
                                                        language_code=data.get_lang_code(lang))

                while data_list[index].info["title"] in self.already_viewed["content"]:
                    index = index + 1
                    if len(data_list) <= index:
                        index = 0
                        # If not enough content, get more
                        self.already_viewed["pages"]["get_popular_movies"] += 1
                        from_page = from_page + 1
                        to_page = to_page + 1
                        data_list = data.get_popular_movies(from_page=from_page, to_page=to_page,
                                                            language_code=data.get_lang_code(lang))

                to_be_returned.append(data_list[index])
                index = index + 1

            for viewd in to_be_returned:
                self.already_viewed["content"].add(viewd.info["title"])
            return to_be_returned

        def get_content_by_genre(amount: int):

            # select random type - tv or movie, for each time
            # try to get movie/tvshow that suits all genres, if no- get of random selected genre.

            to_be_returned = []

            data_list = self.helper_try_all_genres(amount, langs_selected, genres_selected)
            if data_list:
                return data_list

            # if already view those pages, keep going
            from_page = self.already_viewed["pages"]["get_content_by_genre"]
            to_page = from_page
            # Pick random lang & type & genre from what user selected
            lang = random.choice(list(langs_selected))
            type = random.choice(["tv", "movie"])
            random_genre = set()
            random_genre.add(random.choice(genres_selected[type]))

            data_list = data.get_content_by_genre(content_type=type, genres=random_genre, from_page=from_page,
                                                  to_page=to_page, language_code=data.get_lang_code(lang))
            index = 0

            for x in range(0, amount):
                if len(data_list) <= index:
                    index = 0
                    # If not enough content, get more
                    from_page = from_page + 1
                    to_page = to_page + 1
                    data_list = data.get_content_by_genre(content_type=type, genres=random_genre, from_page=from_page,
                                                          to_page=to_page, language_code=data.get_lang_code(lang))

                while data_list[index].info["title"] in self.already_viewed["content"]:
                    index = index + 1
                    if len(data_list) <= index:
                        index = 0
                        # If not enough content, get more
                        from_page = from_page + 1
                        to_page = to_page + 1
                        data_list = data.get_content_by_genre(content_type=type, genres=random_genre,
                                                              from_page=from_page,
                                                              to_page=to_page, language_code=data.get_lang_code(lang))
                        print(len(data_list))
                    print(str(len(data_list)) + " " + str(index))

                to_be_returned.append(data_list[index])
                index = index + 1

            self.already_viewed["content"].update(to_be_returned)
            return to_be_returned

        def get_rated_content(amount: int):
            to_be_returned = []

            # if already view those pages, keep going
            from_page = self.already_viewed["pages"]["get_rated_content"]
            to_page = from_page
            # Pick random lang from selected langs
            lang = random.choice(list(langs_selected))
            type = random.choice(["tv", "movie"])

            data_list = data.get_rated_content(type, from_page=from_page, to_page=to_page,
                                               language_code=data.get_lang_code(lang))
            print(f"Z + {type} + {lang} + {from_page} + {to_page}")
            print(data_list)
            index = 0

            for x in range(0, amount):
                if len(data_list) <= index:
                    index = 0
                    # If not enough content, get more
                    self.already_viewed["pages"]["get_rated_content"] += 1
                    from_page = from_page + 1
                    to_page = to_page + 1
                    data_list = data.get_rated_content(type, from_page=from_page, to_page=to_page,
                                                       language_code=data.get_lang_code(lang))

                while data_list[index].info["title"] in self.already_viewed["content"]:
                    print("X")
                    index = index + 1
                    if len(data_list) <= index:
                        print("Y")
                        index = 0
                        # If not enough content, get more
                        self.already_viewed["pages"]["get_rated_content"] += 1
                        from_page = from_page + 1
                        to_page = to_page + 1
                        data_list = data.get_rated_content(type, from_page=from_page, to_page=to_page,
                                                           language_code=data.get_lang_code(lang))
                        print(data_list)

                to_be_returned.append(data_list[index])
                index = index + 1

            self.already_viewed["content"].update(to_be_returned)
            return to_be_returned

        def get_tvshows_onair(amount: int):
            to_be_returned = []

            # if already view those pages, keep going
            from_page = self.already_viewed["pages"]["get_tvshows_onair"]
            to_page = from_page
            # Pick random lang from selected langs
            lang = random.choice(list(langs_selected))

            data_list = data.get_tvshows_onair(from_page=from_page, to_page=to_page,
                                               language_code=data.get_lang_code(lang))
            index = 0

            for x in range(0, amount):
                if len(data_list) <= index:
                    index = 0
                    # If not enough content, get more
                    self.already_viewed["pages"]["get_tvshows_onair"] += 1
                    from_page = from_page + 1
                    to_page = to_page + 1
                    data_list = data.get_tvshows_onair(from_page=from_page, to_page=to_page,
                                                       language_code=data.get_lang_code(lang))

                while data_list[index].info["title"] in self.already_viewed["content"]:
                    index = index + 1
                    if len(data_list) <= index:
                        index = 0
                        # If not enough content, get more
                        self.already_viewed["pages"]["get_tvshows_onair"] += 1
                        from_page = from_page + 1
                        to_page = to_page + 1
                        data_list = data.get_tvshows_onair(from_page=from_page, to_page=to_page,
                                                           language_code=data.get_lang_code(lang))

                to_be_returned.append(data_list[index])
                index = index + 1

            self.already_viewed["content"].update(to_be_returned)
            return to_be_returned

        return_list = []

        return_list.extend(get_popular_tvshows(5) + get_popular_movies(5))

        # TESTING IF NEEDED
        #for x in self.already_viewed["content"]:
        #    print(x)
        #print(self.already_viewed["pages"]["get_popular_tvshows"])

        return return_list

    def helper_try_all_genres(self, amount, langs_selected, genres_selected):
        """
        Helper func for get_content_by_genre
        this func try to get a content that match all genres selected.
        if there is no such, the main func will get from only 1 selected loved genre.
        """
        to_be_returned = []

        from_page = 1
        to_page = 1
        # Pick random lang & type & genre from what user selected
        lang = random.choice(list(langs_selected))
        type = random.choice(["tv", "movie"])
        genres = genres_selected[type]

        data_list = data.get_content_by_genre(content_type=type, genres=genres, from_page=from_page,
                                              to_page=to_page, language_code=data.get_lang_code(lang))
        index = 0

        for x in range(0, amount):
            if len(data_list) <= index:
                index = 0
                # If not enough content, get more
                from_page = from_page + 1
                to_page = to_page + 1
                data_list = data.get_content_by_genre(content_type=type, genres=genres, from_page=from_page,
                                                      to_page=to_page, language_code=data.get_lang_code(lang))

            while data_list[index].info["title"] in self.already_viewed["content"]:
                index = index + 1
                if len(data_list) <= index:
                    index = 0
                    # If not enough content, get more
                    from_page = from_page + 1
                    to_page = to_page + 1
                    data_list = data.get_content_by_genre(content_type=type, genres=genres,
                                                          from_page=from_page,
                                                          to_page=to_page, language_code=data.get_lang_code(lang))
                    print(len(data_list))
                print(str(len(data_list)) + " " + str(index))

            to_be_returned.append(data_list[index])
            index = index + 1

        return to_be_returned
