import subprocess
import os
import re
import pandas as pd
from tqdm import tqdm

data =[]
base_directory = 'Путь до клонированного репозитория'
repo_folders = [folder for folder in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, folder))]
df_s = ['328s', '51xw']
for repo_folder in tqdm(repo_folders, desc="Processing Repositories"):
    for i in tqdm(df_s.iterrows):
        repo_path = os.path.join(base_directory, repo_folder)
        os.chdir(repo_path)  # Переходим в директорию репозитория
        log_o = subprocess.check_output(['git', 'log', '--name-status', '-n', '1', i], universal_newlines=True).splitlines()
        for j, line in enumerate(log_o):
            if line.startswith('commit   '):
                commit = line.split('commit   ')[1]
                folder_name, file_name, author, date, commit_data = "", "", "", "", ""
            elif line.startswith('Author:  '):
                author = line.split('Author:  ')[1]
            elif line.startswith('Date:    '):
                date = line.split('Date:    ')[1]
            elif line.startswith('M\t') or line.startswith('A\t') or line.startswith('R\t') or line.startswith('D\t'):
                file_status, file_path = line.split('\t')
                folder_name = os.path.dirname(file_path)
                file_name = os.path.basename(file_path)
        if folder_name and file_name:
            commit_info = subprocess.check_output(['git', 'show', '--unified=0', i], universal_newlines=True)
            lines = commit_info.split('\n')
            plus_lines = []
            for k in range(len(lines)):
                line = lines[k]
                if re.search(r'@@', line):
                    next_line = lines[k+1]
                    plus_lines = re.findall('^\s*-', next_line)
                    if plus_lines == ['-']:
                        data.append({'Folder name': folder_name, 'File name': file_name, 'Commit Hash': commit, 'Author': author, 'Date': date, 'Признак удаления': 'Да'}, ignore_index=True)
                    else:
                        data.append({'Folder name': folder_name, 'File name': file_name, 'Commit Hash': commit, 'Author': author, 'Date': date, 'Признак удаления': 'Нет'}, ignore_index=True)
df = pd.DataFrame(data)
df = df.drop_dublicates()
df = df.reset_index(drop=True)

