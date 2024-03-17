import requests
import re
import matplotlib.pyplot as plt
from multiprocessing import Pool
from functools import reduce
from collections import Counter

def map_func(text):
    # Знаходження та підрахунок слів у тексті, повернення як Counter об'єкт
    words = re.findall(r'\w+', text.lower())
    return Counter(words)

def reduce_func(counter1, counter2):
    # Об'єднання двох Counter об'єктів
    return counter1 + counter2

def visualize_top_words(word_counts):
    # Візуалізація топ-10 слів
    words, counts = zip(*word_counts.most_common(10))
    plt.figure(figsize=(10, 8))
    plt.bar(words, counts)
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.title('Top 10 Most Frequent Words')
    plt.show()

if __name__ == '__main__':
    # Завантаження тексту за URL
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"  # Замініть це на вашу URL-адресу
    response = requests.get(url)
    text = response.text

    # Розділення тексту на частини для паралельної обробки
    parts = text.split('\n')

    with Pool(4) as p:  # Використовуйте стільки процесів, скільки дозволяє ваша система
        map_results = p.map(map_func, parts)
        word_counts = reduce(reduce_func, map_results)

    # Візуалізація результатів
    visualize_top_words(word_counts)
