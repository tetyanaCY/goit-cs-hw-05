import string
import requests
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
from matplotlib import pyplot as plt

def get_text(url):
    """Отримання тексту за URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Помилка при отриманні тексту: {e}")
        return None

def remove_punctuation(text):
    """Видалення знаків пунктуації з тексту."""
    return text.translate(str.maketrans("", "", string.punctuation))

def map_function(word):
    """Відображення: перетворення слова у пару (слово, 1)."""
    return word.lower(), 1  # Перетворення до нижнього регістру для уникнення чутливості до регістру

def reduce_function(mapped_values):
    """Зведення: підрахунок загальної кількості для кожного слова."""
    counter = Counter()
    for word, count in mapped_values:
        counter[word] += count
    return counter

def map_reduce(text):
    """Функція MapReduce для аналізу частоти слів."""
    text = remove_punctuation(text)
    words = text.split()
    
    # Відображення (Map)
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    # Зведення (Reduce)
    reduced_values = reduce_function(mapped_values)

    return reduced_values

def visualize_top_words(word_counts, top_n=10):
    """Візуалізація топ-N найчастіше вживаних слів."""
    top_words = word_counts.most_common(top_n)
    words, counts = zip(*top_words)
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts, color='skyblue')
    plt.xlabel('Слова')
    plt.ylabel('Частота')
    plt.title(f'Топ {top_n} найчастіше вживаних слів')
    plt.xticks(rotation=45)
    plt.show()

if __name__ == '__main__':
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    text = get_text(url)
    if text:
        result = map_reduce(text)
        print("Топ 10 найчастіше вживаних слів:")
        for word, count in result.most_common(10):
            print(f"{word}: {count}")
        visualize_top_words(result)
    else:
        print("Помилка: Не вдалося отримати вхідний текст.")
