import csv

def convert_csv_to_txt(csv_path, txt_path):
    """
    Transforme le CSV enrichi (Catégorie, Sous_Catégorie, Question_Apprenant,
    Réponse_Détaillée_Chatbot, Exemple_Pratique_Ou_Formule) en un texte
    structuré qui servira de base de connaissances système.
    """
    with open(csv_path, 'r', encoding='utf-8') as f:
        # Délimiteur point-virgule car les virgules sont dans le texte
        reader = csv.DictReader(f, delimiter=';')
        blocks = []
        for row in reader:
            categorie = row['Catégorie'].strip()
            sous_cat = row['Sous_Catégorie'].strip()
            question = row['Question_Apprenant'].strip()
            reponse = row['Réponse_Détaillée_Chatbot'].strip()
            exemple = row['Exemple_Pratique_Ou_Formule'].strip()

            block = (
                f"### {categorie} > {sous_cat}\n"
                f"**Question type** : {question}\n"
                f"**Réponse experte** : {reponse}\n"
                f"**Exemple concret** : {exemple}\n"
            )
            blocks.append(block)

    preamble = (
        "Tu es un assistant expert en Excel et en ingénierie de prompts. "
        "Tu disposes ci-dessous d'une base de connaissances organisée en questions/réponses détaillées avec exemples. "
        "Réponds uniquement en t'appuyant sur ces données lorsque la question concerne Excel, la gestion de stocks, "
        "les calculs financiers, les diagrammes de Pareto ou l'ingénierie des prompts. "
        "Si la question est hors sujet, réponds poliment que tu n'es pas qualifié.\n\n"
        "BASE DE CONNAISSANCES :\n"
    )
    full_text = preamble + "\n---\n".join(blocks)

    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(full_text)

if __name__ == "__main__":
    convert_csv_to_txt("knowledge_base.csv", "knowledge.txt")
    print("knowledge.txt généré avec succès à partir du CSV enrichi.")