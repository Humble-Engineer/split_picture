import cv2
import os
import shutil

# pyinstaller -F main.py
# pyinstaller -F --hidden-import=cv2 --hidden-import=cv2.data --hidden-import=cv2.utils --hidden-import=cv2.highgui --hidden-import=cv2.imgproc main.py

def draw_cut_lines(image, rows, cols):
    height, width = image.shape[:2]
    row_height = height // rows
    col_width = width // cols
    
    # 绘制水平切割线
    for i in range(1, rows):
        cv2.line(image, (0, i * row_height), (width, i * row_height), (255, 0, 0), 2)
    
    # 绘制垂直切割线
    for j in range(1, cols):
        cv2.line(image, (j * col_width, 0), (j * col_width, height), (255, 0, 0), 2)
    
    return image

def split_image(image_path, rows, cols):
    # 读取图像
    image = cv2.imread(image_path)
    
    # 获取图像的高度和宽度
    height, width = image.shape[:2]
    
    # 计算每个小块的高度和宽度
    row_height = height // rows
    col_width = width // cols
    
    # 绘制切割线
    image_with_lines = draw_cut_lines(image.copy(), rows, cols)
    
    # 显示带有切割线的图像
    cv2.imshow('Image with cut lines', image_with_lines)
    
    # 等待用户输入
    key = cv2.waitKey(0) & 0xFF
    
    # 处理用户输入
    if key == 27:  # 按下 "esc" 键
        cv2.destroyAllWindows()
        print("程序已退出")
        return
    elif key == ord('c'):  # 按下 "c" 键
        cv2.destroyAllWindows()
        
        # 创建输出文件夹，如果存在则先删除
        output_folder = 'output'
        if os.path.exists(output_folder):
            shutil.rmtree(output_folder)
        os.makedirs(output_folder)
        
        # 分割图像
        for i in range(rows):
            for j in range(cols):
                start_row = i * row_height
                end_row = (i + 1) * row_height
                start_col = j * col_width
                end_col = (j + 1) * col_width
                sub_image = image[start_row:end_row, start_col:end_col]
                
                # 保存分割后的图像
                filename = f'({i+1},{j+1}).jpg'
                cv2.imwrite(os.path.join(output_folder, filename), sub_image)
    else:
        cv2.destroyAllWindows()
        print("无效的按键，程序已退出")

# 调用函数
split_image('real_img.png', 4, 6)  # 将图像切成m行n列