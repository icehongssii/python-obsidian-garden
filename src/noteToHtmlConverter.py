from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path
import yaml
import os
from note import Note
from vault import Vault, ItemPath

class SiteError(Exception):
    """Base class for site-related errors."""
    pass

class TemplateError(SiteError):
    """Error raised when a template processing issue occurs."""
    pass

class NoteNotFoundError(SiteError):
    """Error raised when a note cannot be found."""
    pass

class Site:
    def __init__(self, vault_path, template_dir, output_directory, base_url, context_filepath):
        self.vault = Vault(Path(vault_path))
        self.env = Environment(loader=FileSystemLoader(template_dir), autoescape=select_autoescape())
        self.output_directory = Path(output_directory)
        

        self.base_url = base_url
        self.menu = self.build_menu()
        self.context = self.load_context(context_filepath)

    def load_context(self, filepath):
        try:
            with open(filepath, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Failed to open {filepath}")
            return {}

    def render_note_string(self, item_path):

        # TODO @icehongssii IDK What I am
        if type(item_path) == str:
            item_path = ItemPath.from_path_without_ext(Path(item_path))
        item_path = ItemPath.from_path_without_ext(Path(str(item_path)))
                
        note = self.vault.notes.get(item_path)
        
        if not note:
            raise NoteNotFoundError(f"Note not found for path: {item_path}")
        page_template = self.env.get_template('page.html')
        
        html = page_template.render(
            base_url=self.base_url,
            note=note,
            path=item_path.to_dict(),
            note_html=note.render_html(),
            menu=self.menu,
            site=self.context,
            graph={}
        )
        return html

    def render_note(self, item_path):
        html = self.render_note_string(item_path)
        output_path = self.output_directory / f"{item_path}.html"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as   file:
            file.write(html)

    def build_menu(self):

        # Assuming self.vault.notes is a dictionary like {path: note}
    
        paths = self.vault.notes.keys()
        
        menu = {}
        for path in paths:
            components = str(path).split('/')
            menu_node = menu
            for component in components[:-1]:
                menu_node = menu_node.setdefault(component, {})
            menu_node[components[-1]] = {'link': path}


        return menu

# Example usage
if __name__ == '__main__':
    vault_path = '/Users/icehongssii/ws/tech-blog/tech-blog/2. posts/blogs'
    template_path = '/Users/icehongssii/ws/fake-obisidian-garden/templates/default'
    output_path = '/Users/icehongssii/ws/fake-obisidian-garden/dist'
    domain = 'https://xxx.icehongssii.xyz'
    config_path = '/Users/icehongssii/ws/fake-obisidian-garden/context.yaml'

    
    site = Site(vault_path, template_path, output_path, domain, config_path)
    html = site.render_note_string("Docker 이미지 크기 최적화.md")
    print(html)
    
    