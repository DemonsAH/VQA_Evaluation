class Figure:

    def __init__(self, dir, caption):
        self.fig_dir = dir
        self.caption = caption
        self.contexts = []
        self.is_table = False
        self.name = ""

    def add_context(self, context):
        self.contexts += context

    def set_is_table(self):
        self.is_table = True

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def get_contexts(self):
        return self.contexts

    def get_dir(self):
        return self.fig_dir

    def get_caption(self):
        return self.caption
