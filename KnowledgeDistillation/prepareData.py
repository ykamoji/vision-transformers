import os
import shutil

val_labels = {}
for mapping in open('/Users/ykamoji/Documents/ImageDatabase/imageNet/tiny-imagenet-200/val/val_annotations.txt','r').readlines():
    maps = mapping.replace('\n','').split('\t')
    val_labels[maps[0]] = maps[1]

parent_dir = "/Users/ykamoji/Documents/ImageDatabase/imageNet/tiny-imagenet-200/val/"

i=0
for file_name, class_name in val_labels.items():
    path = parent_dir+class_name
    if not os.path.exists(path):
        os.mkdir(path)
    if not os.path.exists(path+"/images/"):
        os.mkdir(path+"/images/")
    shutil.copyfile(parent_dir+"/images/"+file_name, path+"/images/"+file_name)
