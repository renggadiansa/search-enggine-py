import os
from similarity import words_in_doc, jaccard_sim, cosine_sim

# Fungsi recursive_visit_documents digunakan untuk mengunjungi secara rekursif semua dokumen dalam folder koleksi.
def recursive_visit_documents(path):
    obj = os.scandir(path)
    doc_names = []

    for entry in obj:
        if entry.is_file():
            doc_names.append(entry.name)
        elif entry.is_dir():
            sub_dir = os.path.join(path, entry.name)
            sub_doc_names = recursive_visit_documents(sub_dir)
            for sub_doc in sub_doc_names:
                doc_names.append(os.path.join(entry.name, sub_doc))

    obj.close()
    return doc_names

# Fungsi rank_documents digunakan untuk mengurutkan dokumen berdasarkan kesamaan dengan query.
def rank_documents(query, folder_name, similarity="jaccard"):
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

# Variabel search_query dan exclude_query digunakan untuk menyimpan query pencarian dan query yang harus dikecualikan (jika ada).

    documents = recursive_visit_documents(folder_name)
    for doc in documents:
        with open(os.path.join(folder_name, doc), "r", encoding="utf8") as file:
            content = file.read().lower().split()
            if not words_in_doc(exclude_query, content):
                sim = sim_func(search_query, content)
                doc_sim.append((doc, sim))

    doc_sim.sort(key=lambda x: x[1], reverse=True)
    return doc_sim

if __name__ == "__main__":
    print(".:Mesin Pencari Pribadi:.")

    RUNNING = True

    while RUNNING:
        try:
            query = input("Masukkan query pencarian: ")
            collection_folder = input("Masukkan nama folder koleksi (e.g. collection): ")
            sim_func = input("Masukkan fungsi similaritas (cosine OR jaccard): ")
            num_results = int(input("Masukkan jumlah hasil pencarian yang ingin ditampilkan: "))

            ranked_docs = rank_documents(query, collection_folder, similarity=sim_func.lower())

            if num_results < 0:
                raise ValueError("Jumlah hasil pencarian harus positif")

            print(f"Berikut {num_results} dokumen paling relevan terhadap query:")
            for i, (doc, sim) in enumerate(ranked_docs[:num_results], 1):
                print(f"{os.path.join(collection_folder, doc)} {sim}")

            next_action = input("Apakah Anda ingin melakukan pencarian lain? (Y/N): ")
            if next_action.upper() != "Y":
                RUNNING = False
        except ValueError as e:
            print("Terjadi kesalahan: ", e)
            RUNNING = False
