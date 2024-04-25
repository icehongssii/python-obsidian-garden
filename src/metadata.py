import yaml
from typing import Any, Dict, List, Union, Tuple

class MetadataError(Exception):
    """Custom error for metadata processing."""
    pass

class MetadataMappingKeyTypeError(MetadataError):
    """Error for non-string mapping keys."""
    def __str__(self):
        return "Mapping key is not a string"

class FrontMatterYamlError(MetadataError):
    """Error for invalid YAML in front matter section."""
    def __init__(self, original_exception):
        self.original_exception = original_exception

    def __str__(self):
        return f"Invalid YAML in frontmatter section: {self.original_exception}"

class Metadata:
    def __init__(self, inner: Dict[str, Any]):
        self.inner = inner

    @staticmethod
    def from_dict(value: Dict[str, Any]) :
        return Metadata(inner=value)

    def tags(self) -> List[str]:
        """
        Example of input : {'tag': 'hello, world', 'tags': ['python', 'code', 'kimchi']}
        """

        tags = []
        
        if 'tag' in self.inner and isinstance(self.inner['tag'], str):
            tags.extend([tag.strip() for tag in self.inner['tag'].split(',')])
        
        if 'tags' in self.inner and isinstance(self.inner['tags'], list):
            tags.extend([tag for tag in self.inner['tags'] if isinstance(tag, str)])

        return tags

def parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]: # -> (Metadata, str)
    """Parse YAML front matter from the given content string."""
    try:
        parts = content.split('---\n', 2)
        if len(parts) < 3:
            return Metadata.from_dict({}), content
        
        frontmatter, remaining_content = parts[1], parts[2]
        data = yaml.safe_load(frontmatter)
        if not isinstance(data, dict):
            raise MetadataMappingKeyTypeError()

        return Metadata.from_dict(data), remaining_content
    except yaml.YAMLError as e:
        raise FrontMatterYamlError(e)

# Example usage
if __name__ == '__main__':
    content = """
---
tag: hello, world
tags:
  - python
  - code
  - kimchi
---
This is the body of the text document.
"""
    metadata, remaining = parse_frontmatter(content)
    print("Tags:", metadata.tags())
    print("Remaining content:", remaining)
