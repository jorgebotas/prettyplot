import os
import json
import glob
import re

def parse_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    cells = []
    subsections = []
    
    # Extract file-level docstring
    docstring_match = re.match(r'"""(.*?)"""', content, re.DOTALL)
    if docstring_match:
        docstring = docstring_match.group(1).strip()
        # Convert RST-style headers to Markdown headers
        lines = docstring.split('\n')
        markdown_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]
            if i + 1 < len(lines) and set(lines[i+1].strip()) <= set('=-'):
                # It's a header
                level = 1 if '=' in lines[i+1] else 2
                markdown_lines.append(f"{'#' * level} {line}")
                i += 2
            else:
                markdown_lines.append(line)
                i += 1
        
        cells.append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [l + "\n" for l in markdown_lines]
        })
        
        # Remove the docstring from content for further processing
        content = content[docstring_match.end():].strip()

    # Split by # %%
    parts = re.split(r'# %%', content)
    
    # The first part is usually imports and setup
    if parts[0].strip():
        cells.append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [l + "\n" for l in parts[0].strip().split('\n')]
        })

    for part in parts[1:]:
        part = part.strip()
        if not part:
            continue
            
        # Check if the part starts with a comment block (markdown)
        lines = part.split('\n')
        markdown_content = []
        code_content = []
        
        in_markdown = True
        for line in lines:
            if in_markdown and line.strip().startswith('#'):
                # Check for RST headers in comments
                clean_line = line.strip().lstrip('#').strip()
                markdown_content.append(clean_line)
            else:
                in_markdown = False
                code_content.append(line)

        # Process markdown content to handle RST headers
        final_markdown = []
        i = 0
        while i < len(markdown_content):
            line = markdown_content[i]
            if i + 1 < len(markdown_content) and markdown_content[i+1].strip() and set(markdown_content[i+1].strip()) <= set('=-~'):
                 # It's a header
                header_char = markdown_content[i+1].strip()[0]
                if header_char == '=':
                    level = 2
                elif header_char == '-':
                    level = 3
                else: # '~'
                    level = 3
                
                final_markdown.append(f"{'#' * level} {line}")
                subsections.append(line)
                i += 2
            else:
                final_markdown.append(line)
                i += 1

        if final_markdown:
             cells.append({
                "cell_type": "markdown",
                "metadata": {},
                "source": [l + "\n" for l in final_markdown]
            })
            
        if code_content:
             cells.append({
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [l + "\n" for l in code_content if l.strip()]
            })
            
    return cells, subsections

def generate_notebook():
    notebook = {
        "cells": [],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.5"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    # TOC
    toc_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": ["# Table of Contents\n"]
    }
    
    files = sorted(glob.glob('examples/plots/plot_*.py'))
    all_cells = []
    
    section_counter = 1

    for filepath in files:
        filename = os.path.basename(filepath)
        print(f"Processing {filename}...")
        
        # Get title for TOC
        with open(filepath, 'r') as f:
            first_line = f.readline().strip() # Skip """
            second_line = f.readline().strip()
            title = second_line if second_line else filename
        
        numbered_title = f"{section_counter}. {title}"
        link_name = numbered_title.lower().replace(' ', '-').replace('_', '-').replace('.', '')
        toc_cell["source"].append(f"- [{numbered_title}](#{link_name})\n")
        
        file_cells, subsections = parse_file(filepath)
        
        # Update the title in the first cell to include numbering
        if file_cells and file_cells[0]["cell_type"] == "markdown":
            source = file_cells[0]["source"]
            if source and source[0].startswith("# "):
                source[0] = f"# {numbered_title}\n"
        
        # Add subsections to TOC
        for sub in subsections:
            sub_link = sub.lower().replace(' ', '-').replace('_', '-')
            toc_cell["source"].append(f"    - [{sub}](#{sub_link})\n")
            
        all_cells.extend(file_cells)
        section_counter += 1

    notebook["cells"].append(toc_cell)
    notebook["cells"].extend(all_cells)

    with open('examples/examples.ipynb', 'w') as f:
        json.dump(notebook, f, indent=2)
    
    print(f"Generated examples/examples.ipynb with {len(notebook['cells'])} cells.")

if __name__ == "__main__":
    generate_notebook()
