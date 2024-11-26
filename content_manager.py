

class Content:

    def __init__(self, content_type: str, content_origin: str, info_dict: dict, team_dict: dict):

        self.content_type = content_type # MOVIE OR TV
        self.content_origin = content_origin # origin of the content, if it from RATED, POPULAR, ONAIR..

        self.team = team_dict
        self.info = info_dict

        if content_type == "tv":
            self.info["title"] = self.info["name"]
            del self.info["name"]
