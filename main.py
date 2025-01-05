import cv2
import os
import datetime

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

def split_image(image_path, rows, cols, output_subfolder):
    # 读取图像
    image = cv2.imread(image_path)
    
    # 获取图像的高度和宽度
    height, width = image.shape[:2]
    
    # 计算每个小块的高度和宽度
    row_height = height // rows
    col_width = width // cols
    circle_radius_ratio = 0.15
    
    # 绘制切割线和圆
    image_with_lines_and_circles = draw_cut_lines_and_circles(image.copy(), rows, cols, circle_radius_ratio)
    
    # 显示带有切割线和圆的图像
    cv2.imshow('Image with cut lines and circles', image_with_lines_and_circles)
    
    print("按下“c”键保存,其它任意键退出...",end="\n")

    # 等待用户输入
    key = cv2.waitKey(0) & 0xFF
    
    # 处理用户输入
    if key == ord('c'):  # 按下 "c" 键

        cv2.destroyAllWindows()
        
        # 创建输出子文件夹
        output_folder = os.path.join('output', output_subfolder)
        if not os.path.exists(output_folder):
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
                font_scale = 0.3
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

        print("图像已保存到", output_folder)

    else:
        cv2.destroyAllWindows()
        print("程序已退出...")

def list_files(directory):
    valid_extensions = ['.jpg', '.png', '.jpeg', '.bmp', '.gif']  # 添加更多合法的图片格式
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and os.path.splitext(f)[1].lower() in valid_extensions]

if __name__ == '__main__':
    
    # 修改为从 samples 文件夹中列出图像文件
    samples_directory = 'samples'
    if not os.path.exists(samples_directory):
        print(f"{samples_directory} 文件夹不存在，请创建该文件夹并放入图片文件。")
        exit(1)
    
    files = list_files(samples_directory)
    if not files:
        print(f"{samples_directory} 文件夹下没有合法的图片文件。")
        exit(1)
    
    print(f"{samples_directory} 文件夹下的图片文件:")
    for idx, file in enumerate(files):
        print(f"{idx + 1}: {file}")
    
    # 用户选择文件
    file_choice = int(input("请输入要分割的文件编号: ")) - 1
    image_path = os.path.join(samples_directory, files[file_choice])
    
    # 用户输入行数和列数
    rows = int(input("请输入分割的行数: "))
    cols = int(input("请输入分割的列数: "))
    
    # 生成基于时间戳的子文件夹名称
    timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    output_subfolder = f'{timestamp}'
    
    split_image(image_path, rows, cols, output_subfolder)
