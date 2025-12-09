# 导入PyPDF2库，用于读取和处理PDF文件
import PyPDF2
# 导入sys模块，用于访问命令行参数和标准错误输出
import sys

def extract_text_from_pdf(pdf_path):
    """
    从PDF文件中提取文本内容
    
    参数:
        pdf_path: PDF文件的路径
    
    返回:
        提取的文本字符串，如果出错则返回None
    """
    # 初始化一个空字符串，用于存储所有提取的文本内容
    text = ""
    # 使用try-except块捕获可能的异常（如文件不存在、文件损坏等）
    try:
        # 以二进制只读模式打开PDF文件，'rb'表示read binary（二进制读取）
        with open(pdf_path, 'rb') as file:
            # 创建PdfReader对象，用于读取PDF文件内容
            pdf_reader = PyPDF2.PdfReader(file)
            # 获取PDF文件的总页数，通过访问pages属性的长度
            num_pages = len(pdf_reader.pages)
            
            # 打印正在处理的PDF文件路径，提示用户处理开始
            print(f"正在处理PDF文件: {pdf_path}")
            # 打印PDF文件的总页数，让用户了解处理规模
            print(f"总页数: {num_pages}")
            
            # 遍历PDF的每一页，range(num_pages)生成0到num_pages-1的序列
            for page_num in range(num_pages):
                # 获取当前页的页面对象，通过索引访问pages列表
                page = pdf_reader.pages[page_num]
                # 从当前页面提取所有文本内容，返回字符串
                page_text = page.extract_text()
                # 在文本中添加页面分隔标记，格式为"--- Page X ---"，page_num+1是因为索引从0开始
                text += f"\n--- Page {page_num + 1} ---\n"
                # 将当前页面的文本内容追加到总文本字符串中
                text += page_text
                
                # 显示进度：每处理10页就打印一次进度信息
                if (page_num + 1) % 10 == 0:
                    # 打印当前已处理的页数和总页数，使用f-string格式化字符串
                    print(f"已处理 {page_num + 1}/{num_pages} 页...")
                
    # 捕获所有类型的异常
    except Exception as e:
        # 将错误信息输出到标准错误流（stderr），而不是标准输出（stdout）
        print(f"错误: {e}", file=sys.stderr)
        # 返回None表示提取失败
        return None
    
    # 如果提取成功，返回包含所有页面文本的字符串
    return text

# 判断当前脚本是否作为主程序运行（而不是被其他模块导入）
if __name__ == "__main__":
    # 设置默认的PDF文件名，如果用户没有提供命令行参数则使用此文件名
    pdf_path = "elife-59187-v2.pdf"
    
    # 检查命令行参数：sys.argv是命令行参数列表，len(sys.argv) > 1表示除了脚本名外还有其他参数
    if len(sys.argv) > 1:
        # 如果提供了命令行参数，使用第一个参数（索引1，因为索引0是脚本名）作为PDF文件路径
        pdf_path = sys.argv[1]
    
    # 调用extract_text_from_pdf函数，传入PDF文件路径，开始提取文本
    extracted_text = extract_text_from_pdf(pdf_path)
    
    # 检查提取是否成功（extracted_text不为None且不为空字符串）
    if extracted_text:
        # 生成输出文件名：将原PDF文件名中的'.pdf'替换为'_extracted.txt'
        # 例如：'elife-59187-v2.pdf' -> 'elife-59187-v2_extracted.txt'
        output_path = pdf_path.replace('.pdf', '_extracted.txt')
        
        # 以写入模式打开输出文件，使用UTF-8编码确保中文等字符正确保存
        with open(output_path, 'w', encoding='utf-8') as f:
            # 将提取的文本内容写入文件
            f.write(extracted_text)
        
        # 打印空行，使输出更清晰
        print(f"\n提取完成！")
        # 打印输出文件的保存路径，告知用户文件位置
        print(f"文本已保存到: {output_path}")
        # 打印提取文本的总字符数，让用户了解提取的数据量
        print(f"总字符数: {len(extracted_text)}")
    else:
        # 如果提取失败，将错误信息输出到标准错误流
        print("提取失败", file=sys.stderr)
        # 以非零退出码退出程序，表示程序执行失败
        sys.exit(1)

