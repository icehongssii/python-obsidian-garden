
import yaml
import markdown2
from pathlib import Path
from typing import List, Union, Any, Dict, Tuple
from wikilink import WikilinkParser
from metadata import parse_frontmatter

class NoteError(Exception):
    """Base class for errors in Note processing."""
    pass

class NoFileNameError(NoteError):
    """Raised when a filename is not provided."""
    def __str__(self):
        return "No file name"

class MetadataValueError(NoteError):
    """Raised for errors in metadata value processing."""
    def __init__(self, original_exception):
        self.original_exception = original_exception

    def __str__(self):
        return f"Metadata value error: {self.original_exception}"

class Note:
    def __init__(self, title: str, content: str, tags: List[str], links: List[str], metadata: Dict[str, Any]):
        self.title = title
        self.content = content
        self.tags = tags
        self.links = links
        self.metadata = metadata
        

    @staticmethod
    def parse(title: str, content: str):
        parser = WikilinkParser()

        metadata_dict, content = parse_frontmatter(content)

        if not metadata_dict: return 
        tags = metadata_dict.tags()
        # TODO @icehongssii 링크
        #links = extract_links(parser,content)
        links = []
        return Note(title, content, tags, links, metadata_dict)

    @staticmethod
    def from_file(path: Union[str, Path]):
        path = Path(path)
        if not path.is_file():
            raise NoFileNameError()
        title = path.stem
        content = path.read_text()
        return Note.parse(title, content)

    def render_html(self) -> str:
        #markdown(markdown_content,
        return markdown2.markdown(self.content,  extras=["metadata"])#, "highlightjs-lang", "spoiler", "tables", 'fenced-code-blocks', "admonitions"])

def extract_links(parser,content: str) -> List[str]:
    # TODO @icehongssii 링크
    #parser = WikilinkParser()
    links = []
    for c in content:
        res = parser.feed(c)
        
        if res: links.append(res)

    return links

# Example usage
if __name__ == '__main__':
    try:
        
        t = "/Users/icehongssii/ws/tech-blog/tech-blog/0. inbox/프로그래머스-한 번만 등장한 문자.md"
        note = Note.from_file(t)
        print("Title:", note.title)
        print(note.links)
        print("HTML Content:", note.render_html())

    except NoteError as e:
        print(str(e))

