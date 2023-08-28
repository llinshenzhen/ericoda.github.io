import os
import shutil
import logging

def process_sidebar_files(root_path, log_file):
    # 配置日志记录器
    logging.basicConfig(filename=log_file, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    
    logging.info("脚本开始运行")
    
    # 遍历根目录下的所有子文件夹
    for dirpath, dirnames, filenames in os.walk(root_path):
        # 过滤根目录
        if dirpath == root_path:
            continue
        
        sidebar_path = os.path.join(dirpath, "_sidebar.md")
        
        if not os.path.exists(sidebar_path):
            # 如果_sidebar.md文件不存在，则创建它
            with open(sidebar_path, "w") as sidebar_file:
                folder_name = os.path.basename(dirpath)
                # 修复：将生成的目录链接名称保持严格一致
                sidebar_file.write(f"[{folder_name}目录](#{folder_name})\n\n")
                logging.info(f"创建了 {sidebar_path}")
        else:
            # 备份_sidebar.md文件
            shutil.copy2(sidebar_path, f"{sidebar_path}.bak")
            logging.info(f"备份了 {sidebar_path}")
            
        with open(sidebar_path, "w") as sidebar_file:
            logging.info(f"打开 {sidebar_path} 进行写入")
            folder_name = os.path.basename(dirpath)
            # 修复：将生成的目录链接名称保持严格一致
            sidebar_file.write(f"[{folder_name}目录](#{folder_name})\n\n")
            
            # 添加“返回上一级”链接
            parent_dir = os.path.dirname(sidebar_path)
            relative_path_from_parent = os.path.relpath(parent_dir, dirpath)
            parent_link_text = f"- [返回上一级]({relative_path_from_parent}/)"
            sidebar_file.write(parent_link_text + "\n\n")
            
            for filename in filenames:
                if not filename.lower().startswith("_") and filename.lower().endswith(".md") and filename.lower() != "readme.md":
                    file_name_without_extension = os.path.splitext(filename)[0]
                    relative_path = os.path.relpath(os.path.join(dirpath, filename), root_path)
                    link_text = f"- [{file_name_without_extension}]({relative_path})"
                    sidebar_file.write(link_text + "\n")
                    logging.info(f"在 {sidebar_path} 中添加链接：{file_name_without_extension}")
            
    logging.info("脚本运行结束")

if __name__ == "__main__":
    current_directory = os.getcwd()
    log_file = os.path.join(current_directory, "script_log.txt")
    
    process_sidebar_files(current_directory, log_file)
    print("脚本已完成操作，详情请查看日志文件。")
