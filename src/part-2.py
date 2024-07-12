def extract_commit_info(commit_list):
    commit_info=[]
    commit_start = False
    commit_data = []
    for line in commit_list:
        if line.startswith('commit'):
            if commit_start:
                commit_info.append(commit_data)
            commit_data = [line]
            commit_start= True
        else:
            commit_data.append(line)
    commit_info.append(commit_data)
    return commit_info
filtered_df = df[df['Признак удаления'] == 'Да']
 # Переходим в директорию репозитория
for index, row in filtered_df.iterrows():
    commit_hash = row['Commit Hash']
    file_path = row['File Path']
        
    if commit_hash and file_path:  # Проверяем, что есть и commit_hash, и file_path
        try:
                # Указываем кодировку ISO-8859-1 для команды git show
            commit_info = subprocess.check_output(['git', 'show', '--unified=0', commit_hash, file_path], encoding='ISO-8859-1')
        except Exception as e:
            print(f"Error running git show: {e}")
            continue

        l = ['/dev/null', '-->']
        include_df = "|".join(re.escape(s) for s in l)
        plus_lines = re.findall(r'(?<=\-\s)(?!' + include_df + ')(?!.*a/)(.*?)(?=\s-|$)', commit_info)
        for line in plus_lines:
            search_output = subprocess.check_output(['git', 'log', '-S', line,file_path], universal_newlines=True).splitlines()
        commit_info_2 = extract_commit_info(search_output)
        if len(commit_info_2) > 1:
            found = False
            result = []
        for t6 in commit_info_2:
            t = ''.join(re.findall(r'commit\s+(\w+)', str(t6)))
            t1= ''.join(re.findall(r'Author\s+(\D+)', str(t6)))
            t2 = ''.join(re.findall(r'Date:\s+(.+?)\s+\+',str(t6)))
            first_commit_hash = row['Commit Hash']
            if found:
                result.append(t)
                commit2 = t 
                author2 = t1 
                date2 = t2
                found = False
            if t == first_commit_hash:
                found = True
                second_commit_info = commit_info_2[-1]
                first_commit_info  = commit_info_2[0]
            else:
                second_commit_info ='-'
                first_commit_info = '-'

            search_result_df = search_result_df.append({'First_commit_hash':first_commit_info,
                                                        'Second_commit_hash':second_commit_info,
                                                        'Commit Hash':row['Commit Hash'],
                                                        'Line':s,
                                                        'File Path':current_file,
                                                        'Commit Hash2':commit2,
                                                        'Author2': author2,
                                                        'Date2': date2
                                                        })


