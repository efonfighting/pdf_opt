# -*- coding:utf-8*-
import os
from PIL import Image

def imgConvert(srcPath, desPath):
    '''
    图片格式转换，后缀表示对应图片格式
    :param srcPath : 原图片绝对路径
    :param desPath : 目的图片绝对路径
    :return bool: 成功与否
    '''
    try:
        desDir = os.path.split(desPath)[0] # 如果保存路径不存在，则创建目录
        if(os.path.exists(desDir) == False): 
            os.makedirs(desDir)

        img = Image.open(srcPath).save(desPath) # #尝试打开图片，如果不是可以打开的类型，则忽略
        print('convert {} success.'.format(srcPath))
        return True
        
    except Exception as e:
        print(e)
        print('convert {} failed.'.format(srcPath))
        return False


if __name__ == "__main__":  #这里可以判断，当前文件是否是直接被python调用执行
    imgConvert('C:/Users/efonf/2.png', 'C:/Users/efonf/Desktop/capture/sss/ccc/2.jpg')