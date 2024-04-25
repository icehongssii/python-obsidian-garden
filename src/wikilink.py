class Wikilink:
    def __init__(self, target: str, label: str = None, embedded: bool = False):
        self.target = target
        self.label = label
        self.embedded = embedded

    @classmethod
    def new(cls, target: str, label: str = None):
        return cls(target, label, embedded=False)

    @classmethod
    def embedded(cls, target: str):
        return cls(target, embedded=True)

    def __str__(self):
        if self.embedded:
            return f"![[{self.target}]]"
        elif self.label:
            return f"[[{self.target}|{self.label}]]"
        else:
            return f"[[{self.target}]]"

class WikilinkParser:
    def __init__(self):
        self.reset()

    def reset(self):
        self.state = "Start"
        self.current_value = None
        self.embedded = False

    def feed(self, text):
        if self.state == "Start":
            if text == "![":
                self.state = "FirstOpen"
                self.embedded = True
            elif text == "[":
                self.state = "FirstOpen"
        elif self.state == "FirstOpen":
            if text == "[":
                self.state = "SecondOpen"
        elif self.state == "SecondOpen":
            self.current_value = self.parse_wikilink_text(text)
            self.state = "Text"
        elif self.state == "Text" and text == "]":
            self.state = "FirstClose"
        elif self.state == "FirstClose" and text == "]":
            self.state = "Start"
            result = str(self.current_value)
            self.current_value = None
            self.embedded = False
            return result
        return None

    def parse_wikilink_text(self, text):
        parts = text.split('|', 1)
        target = parts[0]
        label = parts[1] if len(parts) > 1 else None
        if self.embedded:
            return Wikilink.embedded(target)
        return Wikilink.new(target, label)

# Example usage
if __name__ == '__main__':
    parser = WikilinkParser()
    print(parser.feed("[") )
    print(parser.feed("[")  )
    print(parser.feed("Page One"))
    print(parser.feed("]"))
    print(parser.feed("]"))
    print(parser.feed("!["))
    print(parser.feed("[") )
    print(parser.feed("image.png"))
    print(parser.feed("]"))
    print(parser.feed("]"))



