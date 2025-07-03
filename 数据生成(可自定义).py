import csv
import numpy as np

def generate_sample_data(age_groups, indicators, target_averages, score_range=(1, 5), sample_size=None):
    """
    为给定的年龄段生成整数样本数据。
    参数：
    - age_groups: 年龄分组列表
    - indicators: 指标列表
    - target_averages: 各个年龄分组和指标的目标平均值字典
    - score_range: 得分可能的最小和最大值范围
    - sample_size: 自定义的每个年龄分组的样本容量，如果为None，则使用默认的100
    """
    data = []
    for age_group in age_groups:
        avg_values = target_averages.get(age_group)

        group_size = sample_size if sample_size else 100

        group_data = {
            indicator:
            np.round(np.random.normal(loc=avg_values[indicator], scale=0.5, size=group_size))
            .clip(*score_range)
            .astype(int)
            for indicator in indicators
        }
        
        group_data['年龄段'] = [age_group] * group_size
        
        group_scores = [dict(zip(group_data, t)) for t in zip(*group_data.values())]
        data.extend(group_scores)
    return data

def save_data_to_csv(data, file_path):
    """
    将数据保存到CSV文件中。
    """
    if data and isinstance(data[0], dict):
        with open(file_path, mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            for row in data:
                writer.writerow(row)
    else:
        print("数据为空或格式不正确。")

# 定义年龄段、指标和预期平均值
age_groups = ['10-18岁', '18-22岁', '22-30岁']
indicators = ['抑郁值', '焦虑值', '憔悴值', '愤怒值', '压力程度', '幸福感', '自尊', '睡眠质量']
target_averages = {
    '10-18岁': {'抑郁值': 3, '焦虑值': 3, '憔悴值': 3, '愤怒值': 3, '压力程度': 3, '幸福感': 3, '自尊': 3, '睡眠质量': 3},
    '18-22岁': {'抑郁值': 2, '焦虑值': 2, '憔悴值': 2, '愤怒值': 2, '压力程度': 2, '幸福感': 2, '自尊': 2, '睡眠质量': 2},
    '22-30岁': {'抑郁值': 4, '焦虑值': 4, '憔悴值': 4, '愤怒值': 4, '压力程度': 4, '幸福感': 4, '自尊': 4, '睡眠质量': 4}
}

# 生成样本数据，并使用提供的规范生成大小为150的样本
custom_sample_size = 150
sample_data = generate_sample_data(age_groups, indicators, target_averages, sample_size=custom_sample_size)

# 设置CSV文件名称为sample_data.csv
file_path = 'sample_data.csv'

# 保存生成的数据到CSV文件中
save_data_to_csv(sample_data, file_path)

print(f"数据已保存到文件：{file_path}")