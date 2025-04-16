#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import re
import shutil
import zipfile
import xml.etree.ElementTree as ET

def main():
    """
    python epub_mod.py <target folder>
    """
    if len(sys.argv) != 2:
        print("python epub_mod.py <target folder>")
        temp_dir = os.getcwd()
    else:
        temp_dir = sys.argv[1]

    files = os.listdir(temp_dir)
    epub_files = [i for i in files if i.endswith('.epub') == True]

    for file in epub_files:
        folder = unzip_files(file, temp_dir)
        # folder = os.path.basename(file).split('.')[0]
        container_name = os.path.join(temp_dir, folder, "META-INF/container.xml")
        print(container_name)
        tree = ET.parse(container_name)
        root = tree.getroot()
        rootfile = root[0][0]
        content_file = rootfile.attrib['full-path']
        content_path = os.path.join(temp_dir, folder, content_file)
        middle_folder = os.path.dirname(content_file)



#man = root.find('{http://www.idpf.org/2007/opf}manifest') 
#title = root.find('./atom:title', {'atom': 'http://www.w3.org/2005/Atom'})  
#t第2引数に名前空間のマッピングを指定
#root[1].findall("{http://www.idpf.org/2007/opf}item[@media-type='image/jpeg']")
        content_tree = ET.parse(content_path)
        content_root = content_tree.getroot()
        root_tag = content_root.tag
        m = re.search(r'\{.+\}', root_tag)
        if m is not None:
            file_list = []
            # print(m.group())
            namespace = m.group()
            #man = root.find('{http://www.idpf.org/2007/opf}manifest') 
            man = content_root.find(namespace + 'manifest')
            #man.findall("{http://www.idpf.org/2007/opf}item[@media-type='image/jpeg']")
            query = namespace + "item[@media-type='image/jpeg']"
            items = man.findall(query)
            for item in items:
                href = item.get('href')
                # print(href)
                file_list.append(href)


            zip_file_name = os.path.join(temp_dir, folder + '.zip')
            with zipfile.ZipFile(zip_file_name, 'w',
                    compression=zipfile.ZIP_DEFLATED,
                    compresslevel=9) as zf:
                for pic in file_list:
                    in_file = os.path.join(temp_dir, folder, middle_folder, pic)
                    # print(in_file)
                    zf.write(in_file, os.path.basename(pic))
        work_folder = os.path.join(temp_dir, folder)
        shutil.rmtree(work_folder)

def unzip_files(target, temp_dir) :
    target_folder = os.path.basename(target).split('.')[0]
    target_path = os.path.join(temp_dir, target)
    with zipfile.ZipFile(target_path, 'r') as zf:
        for file in zf.namelist():
            file_path = ''
            # print(file)
            with zf.open(file) as f:
                contents = f.read()
                file_path = os.path.join(temp_dir, target_folder, file)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                # print(file_path)
                if file_path.endswith('/') is False:
                    with open(file_path, 'wb') as w:
                        w.write(contents)
    return target_folder




if __name__ == "__main__":
    main()
