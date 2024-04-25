import os
import shutil
from pathlib import Path

import fire

from noteToHtmlConverter import Site
from vault import Vault
# from wikilink import Wikilink

class ObsidianGardenCLI:
    def __init__(self, vault_path:str="/Users/icehongssii/ws/tech-blog/tech-blog/2. posts", 
                        output_directory:str="/Users/icehongssii/ws/fake-obisidian-garden/dist", 
                        # base_url:str="xxx.icehongssii.xyz", 
                        base_url:str="/",
                        template:str="/Users/icehongssii/ws/fake-obisidian-garden/templates/default",
                        config:str="/Users/icehongssii/ws/fake-obisidian-garden/context.yaml"):
        self.vault = vault_path
        self.output_directory = output_directory
        self.base_url = base_url
        self.template = template
        self.config = config


    def init(self):
        """
        python main.py init
        Initialize the vault directory with necessary config and template files. 
        """

        config_dir = Path(self.vault) / ".garden"
        if config_dir.exists():
            print(f"{config_dir} already exists.")
            return

        try:
            self._initialize_config(config_dir)
            self._initialize_default_template(config_dir)
            print("Obsidian Garden initialized. 🌱🌺\nRun `obsidian-garden build` to generate a static site from your notes.")
        except IOError as e:
            print(f"Initialization failed: {e}")

    def build(self, tag=None):
        """ 
        python main.py build
        Build the static site based on the notes and configuration. 
        """
        from pathlib import Path
        

        vault_builder = Vault(Path(self.vault))
        
        if tag:
            vault_builder.filter_tags(tag)

        site = Site(self.vault, self.template, self.output_directory, self.base_url, self.config)
        
        print("🌱Generating pages...")
        for path in vault_builder.notes.keys():
            
            site.render_note(path)
        self._sync_static_dir(self.template, self.output_directory)
        print(f"\n🌺Output directory: {self.output_directory}")

    def _initialize_config(self, config_dir):
        default_config = """
---
title: Site name
katex: true
topnav:
  links:
    - text: Link 1
      href: https://example.com/link-1
    - text: Link 2
      href: https://example.com/link-2
"""
        os.makedirs(config_dir, exist_ok=True)
        config_filepath = config_dir / "site.yaml"
        with open(config_filepath, 'w') as file:
            file.write(default_config)

    def _initialize_default_template(self, config_dir):
        default_template_dir = config_dir / "templates/default"
        os.makedirs(default_template_dir, exist_ok=True)
        # Implement copying template files similar to Rust's embedding

    def _sync_static_dir(self, template, output_directory):
        source_static_dir = Path(template) / "_static"
        target_static_dir = Path(output_directory) / "_static"
        shutil.copytree(source_static_dir, target_static_dir, dirs_exist_ok=True)

def main():
    fire.Fire(ObsidianGardenCLI)

if __name__ == '__main__':
    main()
