
import os
from pathlib import Path
from typing import Dict, List, Optional, TypeVar, Generic
import networkx as nx
from note import Note

T = TypeVar('T')

class ItemPath:
    def __init__(self, components: List[str]):
        self.components = components

    @staticmethod
    def from_path(path: Path):
        return ItemPath([part for part in path.parts])

    @staticmethod
    def from_path_without_ext(path: Path):
        parts = list(path.parent.parts)
        parts.append(path.stem)
        return ItemPath(parts)

    def to_dict(self) -> dict:
        # Otherwise, ItemPath can't be serialized to be rendered
        return {'components': self.components}

    def __hash__(self):
        return hash(tuple(self.components))

    def __eq__(self, other):
        return isinstance(other, ItemPath) and self.components == other.components

    def __str__(self):
        return "/".join(self.components)

class EmbeddedFile:
    def __init__(self, path: Path, file_type: str):
        self.path = path
        self.file_type = file_type

    def __str__(self):
        return f"{self.file_type} file at {self.path}"

class Vault:
    def __init__(self, root: Path):
        self.root = root
        self.notes: Dict[ItemPath, Note] = {}
        self.files: Dict[ItemPath, EmbeddedFile] = {}
        self._walk()
        self.graph = nx.DiGraph()

    def add_note(self, note: Note, item_path: ItemPath):
        self.notes[item_path] = note
        # TODO @icehongssii 240425
        # self.graph.add_node(item_path)

    def add_file(self, file: EmbeddedFile, item_path: ItemPath):
        self.files[item_path] = file

    def link_notes(self, from_path: ItemPath, to_path: ItemPath):
        if from_path in self.notes and to_path in self.notes:
            self.graph.add_edge(from_path, to_path)

    def get_note(self, item_path: ItemPath) -> Optional[Note]:
        return self.notes.get(item_path)

    def _walk(self):

        for root, dirs, files in os.walk(self.root):
            for file in files:

                full_path = Path(root) / file
                relative_path = full_path.relative_to(self.root)
                item_path = ItemPath.from_path_without_ext(relative_path)

                if file.endswith('.md'):
                    
                    note = Note.from_file(full_path)  # Implementation needed
                    
                    self.add_note(note, item_path)
                elif any(file.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif']):
                    self.add_file(EmbeddedFile(full_path, 'Image'), item_path)


# Usage example
if __name__ == '__main__':
    vault_path= '/Users/icehongssii/ws/tech-blog/tech-blog/2. posts/blogs/'
    vault = Vault(Path(vault_path))
    print(vault.notes)
    print(vault.files)
