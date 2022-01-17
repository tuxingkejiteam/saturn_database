import json
from def_class import ImgLabel

json_path = 'Clb000b_unlabeled.json'
img_label = ImgLabel(json_path)
print(img_label)
print(len(img_label))
for item in img_label:
    print(item)

#target = img_label[1]

pass

