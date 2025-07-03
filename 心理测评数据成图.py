import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import matplotlib
import csv
from io import BytesIO

matplotlib.rcParams['font.family'] = 'SimHei'  
matplotlib.rcParams['axes.unicode_minus'] = False  

def read_data_from_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data

def extract_group_data(data, age_group):  #取平均值
    group_data = [row for row in data if row['年龄段'] == age_group]
    if not group_data:
        return None

    avg_scores = {}
    labels = group_data[0].keys() - {'年龄段'}
    for label in labels:
        avg_scores[label] = np.mean([float(row[label]) for row in group_data])
    return avg_scores

def create_plots(age_group, data):  #画BASE64的图         
    labels = np.array(list(data.keys()))
    scores = np.array(list(data.values()))
    
    fig = plt.figure(figsize=(18, 12))

    # 雷达图
    ax1 = fig.add_subplot(231, polar=True)
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    scores_concated = np.concatenate((scores, [scores[0]]))
    angles += angles[:1]
    ax1.plot(angles, scores_concated, marker='o', linestyle='-')
    ax1.fill(angles, scores_concated, alpha=0.25)
    ax1.set_xticks(angles[:-1])
    ax1.set_xticklabels(labels)
    ax1.set_title(f'{age_group} 雷达图')

    # 热力图
    scores_matrix = np.outer(scores, scores)
    ax2 = fig.add_subplot(232)
    sns.heatmap(scores_matrix, ax=ax2, cmap='viridis')
    ax2.set_title(f'{age_group} 热力图')

    # 柱状图
    ax3 = fig.add_subplot(233)
    ax3.bar(labels, scores)
    ax3.set_xticks(range(len(labels)))
    ax3.set_xticklabels(labels, rotation=45, ha="right")
    ax3.set_title(f'{age_group} 柱状图')

    # 条形图
    ax4 = fig.add_subplot(234)
    ax4.barh(labels, scores)
    ax4.set_title(f'{age_group} 条形图')

    # 饼图
    ax5 = fig.add_subplot(235)
    ax5.pie(scores, labels=labels, autopct='%1.1f%%')
    ax5.set_title(f'{age_group} 饼图')

    # 阶梯图
    ax6 = fig.add_subplot(236)
    ax6.step(range(len(scores)), scores, where='mid')
    ax6.set_xticks(range(len(labels)))
    ax6.set_xticklabels(labels, rotation=45, ha="right")
    ax6.set_title(f'{age_group} 阶梯图')

    plt.tight_layout()
    img_data = BytesIO()
    plt.savefig(img_data, format='png', bbox_inches="tight")
    plt.close()
    img_data.seek(0)

    return base64.b64encode(img_data.getvalue()).decode('utf8')

file_path = 'sample_data.csv'  
data = read_data_from_csv(file_path)

html_string = '''
<html>
<head>
<title>不同年龄段的数据分析图形展示</title>
</head>
<body>
'''

# 为每个年龄段生成图形，并将图片BASE64编码后嵌入HTML中
for age_group in ['10-18岁', '18-22岁', '22-30岁']:
    group_data = extract_group_data(data, age_group)
    if group_data:
        img_base64 = create_plots(age_group, group_data)
        html_string += f'<h2>{age_group}</h2>'
        html_string += f'<img src="data:image/png;base64,{img_base64}" /><br/>'

html_string += '''
</body>
</html>
'''

with open('age_group_plots.html', 'w', encoding='utf-8') as html_file:
    html_file.write(html_string)

print("输出完成")