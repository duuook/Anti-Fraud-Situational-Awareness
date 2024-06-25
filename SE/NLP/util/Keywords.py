
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import jieba

# 读取CSV文件
input_file = 'output.csv'
output_file = 'cleaned_text.csv'
df = pd.read_csv(input_file, encoding='GBK')

# 读取停用词表
def load_stopwords(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        stopwords = set(line.strip() for line in file)
    return stopwords

stopwords_file = 'stopwords.txt'
stopwords = load_stopwords(stopwords_file)

# 分词并过滤停用词
def tokenize_and_filter(text):
    words = jieba.cut(text)
    filtered_words = [word for word in words if word not in stopwords and word.strip()]
    return ' '.join(filtered_words)

# 提取内容列并进行分词和停用词过滤
contents = df['Content'].apply(tokenize_and_filter).tolist()

# 使用TF-IDF向量化器
vectorizer = TfidfVectorizer(max_features=200)
tfidf_matrix = vectorizer.fit_transform(contents)

# 提取tf-idf关键词
feature_names = vectorizer.get_feature_names_out()

# 生成简短的Content列
short_contents = []
for row in tfidf_matrix:
    top_200_indices = row.indices[row.data.argsort()[-200:][::-1]]
    short_content = ' '.join([feature_names[idx] for idx in top_200_indices])
    short_contents.append(short_content)

# 将简短的内容列添加到DataFrame中
df['cleaned_content'] = short_contents

# 保存到新的CSV文件
df.to_csv(output_file, index=False)

print(f"已生成新的CSV文件: {output_file}")

