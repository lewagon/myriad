
class Module:

    def __init__(self, slug, name, icon, path):

        self.slug = slug
        self.name = name
        self.icon = icon
        self.path = path

        self.leafs = []

    def __repr__(self):

        return (
            "#<Module "
            f"path={self.path} "
            f"slug={self.slug} "
            f"name={self.name} "
            f"icon={self.icon} "
            f"@={id(self)}>")

    def attach(self, leaf):

        self.leafs.append(leaf)
