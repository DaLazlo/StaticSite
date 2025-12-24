
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("not implemented")

    def props_to_html(self):
        mystring = ""
        if self.props == None:
            return mystring
        for key in self.props.keys():
            mystring += f' {key}="{self.props[key]}"'
        return mystring

    def __repr__(self):
        return f"{self.tag} : {self.value} : {self.children} :{self.props_to_html()}"
