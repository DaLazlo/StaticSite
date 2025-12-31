
from textnode import TextType, TextNode
from markdown import markdown_to_html_node, extract_title

import os, shutil, re

def copy_static(source, destination):
    if not os.path.exists(source):
        raise Exception("source not found")
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    for file in os.listdir(source):
        if os.path.isfile(os.path.join(source, file)):
            shutil.copy(os.path.join(source, file), destination)
        else:
            copy_static(os.path.join(source, file), os.path.join(destination, file))

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    file = open(from_path)
    markdown = file.read()
    file.close()
    file = open(template_path)
    template = file.read()
    file.close()
    node = markdown_to_html_node(markdown)
    my_html = node.to_html()
    my_title = extract_title(markdown)
    template = re.sub(r"\{\{ Title }}", my_title, template)
    template = re.sub(r"\{\{ Content }}", my_html, template)
    file = open(dest_path, "w")
    file.write(template)
    file.close()
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for file in os.listdir(dir_path_content):
        if os.path.isfile(os.path.join(dir_path_content, file)):
            generate_page(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, re.sub(r"(\.md)$", ".html", file)))
        else:
            os.mkdir(os.path.join(dest_dir_path, file))
            generate_pages_recursive(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file))

def main():
    copy_static("/home/lazlo/StaticSite/static", "/home/lazlo/StaticSite/public/")
    #generate_page("/home/lazlo/StaticSite/content/index.md", "/home/lazlo/StaticSite/template.html", "/home/lazlo/StaticSite/public/index.html")
    generate_pages_recursive("/home/lazlo/StaticSite/content/", "/home/lazlo/StaticSite/template.html", "/home/lazlo/StaticSite/public/")

if __name__=="__main__":
    main()