import cv2
import os

# pyinstaller --name=split_picture --onefile main.py

def draw_cut_lines_and_circles(image, rows, cols, circle_radius_ratio=0.40):
    height, width = image.shape[:2]
    row_height = height // rows
    col_width = width // cols
    
    # 绘制水平切割线
    for i in range(1, rows):
        cv2.line(image, (0, i * row_height), (width, i * row_height), (255, 0, 0), 2)
    
    # 绘制垂直切割线
    for j in range(1, cols):
        cv2.line(image, (j * col_width, 0), (j * col_width, height), (255, 0, 0), 2)
    
    # 绘制每个小方格中的圆
    for i in range(rows):
        for j in range(cols):
            center_x = j * col_width + col_width // 2
            center_y = i * row_height + row_height // 2
            radius = int(min(row_height, col_width) * circle_radius_ratio)
            cv2.circle(image, (center_x, center_y), radius, (0, 0, 255), 2)
    
    return image

def split_image(image_path, rows, cols):
    # 读取图像
    image = cv2.imread(image_path)
    
    # 获取图像的高度和宽度
    height, width = image.shape[:2]
    
    # 计算每个小块的高度和宽度
    row_height = height // rows
    col_width = width // cols
    circle_radius_ratio = 0.3
    
    # 绘制切割线和圆
    image_with_lines_and_circles = draw_cut_lines_and_circles(image.copy(), rows, cols, circle_radius_ratio)
    
    # 显示带有切割线和圆的图像
    cv2.imshow('Image with cut lines and circles', image_with_lines_and_circles)
    
    print("按下“c”键保存切割图像...")

    # 等待用户输入
    key = cv2.waitKey(0) & 0xFF
    
    # 处理用户输入
    if key == ord('c'):  # 按下 "c" 键

        cv2.destroyAllWindows()
        
        # 创建输出文件夹，如果存在则先删除
        output_folder = 'output'
        if os.path.exists(output_folder):
            pass
        else:
            os.makedirs(output_folder)
        
        # 分割图像
        for i in range(rows):
            for j in range(cols):
                center_x = j * col_width + col_width // 2
                center_y = i * row_height + row_height // 2
                radius = int(min(row_height, col_width) * circle_radius_ratio)
                
                # 计算圆的边界
                start_row = max(center_y - radius, 0)
                end_row = min(center_y + radius, height)
                start_col = max(center_x - radius, 0)
                end_col = min(center_x + radius, width)
                
                # 裁剪图像
                sub_image = image[start_row:end_row, start_col:end_col]

                # 计算子图的平均灰度值
                gray_sub_image = cv2.cvtColor(sub_image, cv2.COLOR_BGR2GRAY)
                average_gray_value = cv2.mean(gray_sub_image)[0]

                # 将平均灰度值转换为字符串
                text = f'{average_gray_value:.2f}'

                # 在子图的左上角绘制文本
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.5
                font_color = (0, 0, 255)
                thickness = 1
                line_type = cv2.LINE_AA

                # 文本位置
                text_position = (5, 20)

                # 绘制文本
                cv2.putText(sub_image, text, text_position, font, font_scale, font_color, thickness, line_type)

                # 保存分割后的图像
                filename = f'{i+1}-{j+1}.jpg'
                cv2.imwrite(os.path.join(output_folder, filename), sub_image)

        print("图像已保存...")

    else:
        cv2.destroyAllWindows()
        print("无效的按键，程序已退出")

# 调用函数
split_image('real_img.png', 4, 6)  # 将图像切成m行n列