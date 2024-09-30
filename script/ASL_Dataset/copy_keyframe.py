import os
import numpy as np 
import json
import argparse
import shutil


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='copy file to target directory')
    parser.add_argument('-j','--json_file', type=str)
    parser.add_argument('-o','--output_folder', type=str)
    args = parser.parse_args()
    json_file = args.json_file
    output_folder = args.output_folder
    os.makedirs(output_folder, exist_ok=True)

    with open(json_file, 'r') as file:
        keyframes = json.load(file) 
    # 遍历数据并复制文件
    for key, value in keyframes.items():
        if key == "camera":
            None
        else:
            image_path = value['image_path']
       # 提取文件名
            file_name = os.path.basename(image_path)
            # 构建目标文件路径
            target_path = os.path.join(output_folder, file_name)
       # 复制文件
            shutil.copy(image_path, target_path)
            print(f"复制文件: {image_path} 到 {target_path}")