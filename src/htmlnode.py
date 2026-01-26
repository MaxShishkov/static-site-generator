from __future__ import annotations

class HTMLNode():
    def __init__(
        self,
        tag:str | None = None,
        value:str | None = None,
        children:list[HTMLNode] | None = None,
        props:dict[str,str] | None = None
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise(NotImplementedError)
    
    def props_to_html(self):
        html_str = ""
        if self.props is not None:
            for k, v in self.props.items():
                html_str += f" {k}=\"{v}\""
        return html_str
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    
class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props:dict[str,str] | None = None):
        super().__init__(tag, value, None, props)
        
    @property
    def children(self):
        return None
    
    @children.setter
    def children(self, value):
        if value != None:
            raise AttributeError("LeafNode cannot have children")
    
    def to_html(self):
        if self.tag != "img" and not self.value:
            raise(ValueError("All leaf nodes must have a value"))
        if self.tag is None or self.tag == "":
            return f"{self.value}"
        
        props_str = self.props_to_html()
        if self.tag == "img":
            html_str = f"<{self.tag}{props_str} />"
        else:
            html_str = f"<{self.tag}{props_str}>{self.value}</{self.tag}>"
            
        return html_str
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
    
class ParentNode(HTMLNode):
    def __init__(self, tag:str, children:list[HTMLNode], props:dict[str,str] | None = None):
        super().__init__(tag, None, children, props)
        
    @property
    def value(self):
        return None
    
    @value.setter
    def value(self, value):
        if value != None:
            raise AttributeError("ParentNode cannot have value")
        
    def to_html(self):
        if self.tag is None or self.tag == "":
            raise(ValueError("All Parent nodes must have a tag"))
        
        if not self.children:
            raise(ValueError("All Parent nodes must have children"))
        
        props_str = self.props_to_html()
        html_str = f"<{self.tag}{props_str}>"
        for child in self.children:
            child_html = child.to_html()
            html_str += child_html
        html_str += f"</{self.tag}>"
        
        return html_str
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"