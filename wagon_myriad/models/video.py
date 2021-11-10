
class Video:

    def __init__(self, language, video_id):

        self.language = language
        self.video_id = video_id

    def __repr__(self):

        return (
            "#<Video "
            f"language={self.language} "
            f"video_id={self.video_id} "
            f"@={id(self)}>")
