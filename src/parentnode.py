from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("No tag found")
        if self.children == None or self.children == []:
            raise ValueError("No children found")
        childstring = ""
        for child in self.children:
            childstring += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{childstring}</{self.tag}>"