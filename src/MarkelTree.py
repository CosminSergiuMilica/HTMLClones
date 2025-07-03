import ssdeep

class MerkelNode:
    def __init__(self, tag=None, text=None, attrs=None, children=None):
        self.tag = tag # debug
        self.fingerprint = self.__generate_fingerprint(text.strip() if text else "", attrs or {})
        self.children = children or []
        self.is_leaf = len(self.children)==0
        self.hash = self.__compute_hash()

    def __generate_fingerprint(self, text, attributes):
        attr_repr = ""
        if "class" in attributes:
            attr_repr += f" class='{attributes['class']}'"
        if "id" in attributes:
            attr_repr += f" id='{attributes['id']}'"

        text = " ".join(text.split())
        return f"<{self.tag}{attr_repr}>{text}"

    def __compute_hash(self):
        if self.is_leaf:
            return ssdeep.hash(self.fingerprint)
        else:
            combined = ''.join(child.hash for child in self.children)
            return ssdeep.hash(combined)

    def print_tree(self, level=0):
        indent = "  " * level
        prefix = "Leaf" if self.is_leaf else "Node"
        print(f"{indent}{prefix}<{self.tag}> ({self.hash})")
        for child in self.children:
            child.print_tree(level + 1)

def build_merkel_tree(bs_node):
    if bs_node.name is None:
        text = bs_node.string or ''
        text = text.strip()
        if not text:
            return None
        return MerkelNode(tag='__text__', text=text, attrs={})

    children = []
    for child in bs_node.children:
        node = build_merkel_tree(child)
        if node:
            children.append(node)

    return MerkelNode(
        tag=bs_node.name,
        text='',
        attrs=bs_node.attrs,
        children=children
    )
