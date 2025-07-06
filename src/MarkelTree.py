import ssdeep

class MerkelNode:
    def __init__(self, tag=None, text=None, attrs=None, children=None):
        self.tag = tag
        self.attrs = attrs or {}
        self.text = " ".join(text.strip().split())[:30] if text else ""
        self.children = children or []
        self.is_leaf = len(self.children) == 0

        self.fingerprint = self.__generate_fingerprint()
        self.hash = self.__compute_hash()

    def __generate_fingerprint(self):
        style = self.attrs.get("style", "")
        classes = self.attrs.get("class", "")
        if isinstance(classes, list):
            classes = " ".join(sorted(classes))
        elif isinstance(classes, str):
            classes = " ".join(sorted(classes.split()))

        return f"<{self.tag}|text={self.text}|style={style}|class={classes}>"

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
        return MerkelNode(tag='__text__', text=text)

    attrs = bs_node.attrs if hasattr(bs_node, "attrs") else {}

    children = []
    for child in bs_node.children:
        node = build_merkel_tree(child)
        if node:
            children.append(node)

    return MerkelNode(
        tag=bs_node.name,
        text=bs_node.get_text(strip=True),
        attrs=attrs,
        children=children
    )
