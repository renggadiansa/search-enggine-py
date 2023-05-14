import math

# fungsi ini menerima daftar kata words dan dokumen doc
def words_in_doc(words, doc):
  return any(word in doc for word in words)

def jaccard_sim(query, doc):
  intersection = len(set(query).intersection(doc))
  union = len(set(query).union(doc))
  return intersection / union

def word_count(text):
  word_freq = {}
  for word in text:
    if word in word_freq:
      word_freq[word] += 1
    else:
      word_freq[word] = 1
  return word_freq

def dot_product(query, doc):
  query_freq = word_count(query)
  doc_freq = word_count(doc)
  total = 0
  for word in set(query).intersection(doc):
    total += query_freq[word] * doc_freq[word]
  return total

def norm(text):
  word_freq = word_count(text)
  total = sum(freq ** 2 for freq in word_freq.values())
  return math.sqrt(total)

def cosine_sim(query, doc):
  dot_prod = dot_product(query, doc)
  norm_query = norm(query)
  norm_doc = norm(doc)
  return dot_prod / (norm_query * norm_doc)

# bagian yang akan dieksekusi saat file ini dijalankan sebagai program utama.
if __name__ == "__main__":
  # tester
  query = ["hello", "hello", "hello", "world"]
  doc = ["hello", "hello", "selamat", "world", "world"]
  print("cosine similarity =", cosine_sim(query, doc))
  print("jaccard similarity =", jaccard_sim(query, doc))
