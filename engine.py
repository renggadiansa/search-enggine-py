import os
from similarity import words_in_doc, jaccard_sim, cosine_sim

# Fungsi ini melakukan kunjungan rekursif ke dalam folder koleksi dan mengumpulkan daftar semua dokumen yang ada.

def recursive_visit_documents(path):
    obj = os.scandir(path)
    doc_names = []

    for entry in obj:
        if entry.is_file():
            doc_names.append(entry.name)
        elif entry.is_dir():
            sub_dir = path + '/' + entry.name
            sub_doc_names = recursive_visit_documents(sub_dir)
            for sub_doc in sub_doc_names:
                doc_names.append(entry.name + '/' + sub_doc)

    obj.close()
    return doc_names

#Fungsi ini melakukan peringkat dokumen berdasarkan similaritas dengan query

def rank_documents(query, documents, similarity="jaccard"):
    if similarity == "jaccard":
        sim_func = jaccard_sim
    elif similarity == "cosine":
        sim_func = cosine_sim
    else:
        raise ValueError("Argumen similarity tidak valid")

    search_query = ""
    exclude_query = ""

    if "EXCLUDE" in query:
        queries = query.split(" EXCLUDE ")
        search_query = queries[0].lower().split()
        exclude_query = queries[1].lower().split()
    else:
        search_query = query.lower().split()

    doc_sim = []

    for doc in documents:
        with open(doc, "r", encoding="utf8") as file:
            content = file.read().lower().split()
            if not words_in_doc(exclude_query, content):
                sim = sim_func(search_query, content)
                doc_sim.append((doc, sim))

    doc_sim.sort(key=lambda x: x[1], reverse=True)
    return doc_sim

# Bagian ini merupakan bagian utama program yang dijalankan saat file ini dieksekusi. 

if __name__ == "__main__":
    query = "ekonomi"
    documents = recursive_visit_documents("./collection")
    ranked_docs = rank_documents(query, documents, similarity="cosine")
    print("Query:", query)
    for doc, sim in ranked_docs:
        print(doc, sim)
