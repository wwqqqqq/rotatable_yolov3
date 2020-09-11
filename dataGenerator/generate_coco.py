import os
from PIL import Image
import json

DataDir = '../data/'
ImgDir = DataDir + 'image'
LabelDir = DataDir + 'labels'


def getRawLabels(dir):
    labelMap = {}
    files = os.listdir(dir)
    unique_id = 0
    for filename in files:
        try:
            key = filename.split('.')[0]
        except:
            print("Invalid filename:", filename)
        labelList = []
        path = dir+'/'+filename
        with open(path, 'r') as f:
            content = f.readlines()
            for line in content:
                label = {}
                nums = line.strip().split()
                if len(nums) != 13:
                    continue
                segmentation = []
                for i in range(8):
                    segmentation.append(int(nums[i]))
                area = float(nums[8])
                bbox = []
                for i in range(4):
                    bbox.append(int(nums[9+i]))
                label['id'] = unique_id
                label['segmentation'] = segmentation
                label['area'] = area
                label['bbox'] = bbox
                labelList.append(label)
                unique_id += 1
        labelMap[key] = labelList

    return labelMap


def getImageInfos(dir):
    imageList = []
    files = os.listdir(dir)
    unique_id = 0
    for filename in files:
        infoMap = {}
        path = dir+'/'+filename
        width, height = Image.open(path).size
        infoMap['id'] = unique_id
        infoMap['width'] = width
        infoMap['height'] = height
        infoMap['file_name'] = filename
        unique_id += 1
        imageList.append(infoMap)
    return imageList


def getDatasetInCocoFormat(imgDir, labelDir):
    imageList = getImageInfos(imgDir)
    labelMap = getRawLabels(labelDir)
    defaultCategoryId = 0
    datasetMap = {}
    # initialization
    datasetMap['info'] = {}
    datasetMap['license'] = []
    datasetMap['images'] = imageList
    datasetMap['annotations'] = []
    datasetMap['categories'] = []

    # add categories
    category = {
        'supercategory': 'bag',
        'id': defaultCategoryId,
        'name': 'sauce_bag'
    }
    datasetMap['categories'].append(category)

    # add image info and annotation
    for img in imageList:
        key = img['file_name'].split('.')[0]
        labels = labelMap[key]
        for label in labels:
            annotation = label
            annotation['category_id'] = defaultCategoryId
            annotation['image_id'] = img['id']
            annotation['iscrowd'] = 0
            datasetMap['annotations'].append(annotation)
    return datasetMap


def convert_to_json(dictionary, output_file):
    r = json.dumps(dictionary)
    with open(output_file, 'w') as f:
        f.write(r)
    return r


datasetMap = getDatasetInCocoFormat(ImgDir, LabelDir)
convert_to_json(datasetMap, 'coco.json')
