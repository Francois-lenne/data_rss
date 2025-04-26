import re
import dataclasses


class r_code:

    def __init__(self, r_code: str):
        self.r_code  = r_code

def add_comment_code(texte:str, caractere_a_ajouter:str ) -> str:
    """
    Put in comment all the lines thar are not in the <code> and </code></pre> tags
    :param texte: the code as a string
    :param caractere_a_ajouter: the character to add at the beginning of the line in order to comment it
    :return: the code with the comments added
    """
    # add the carriage return before the <code> and </code></pre> tags
    texte = re.sub(r'(?=<code>)', '\n', texte)
    texte = re.sub(r'(?=</code></pre>)', '\n', texte)
    texte = re.sub(r'(<code>)', r'\1\n', texte)
    texte = re.sub(r'(</code></pre>)', r'\1\n', texte)

    lignes = texte.splitlines() # separate the lines for the for loop
    to_comment = True # initialisation de la variable to_comment

    for i, ligne in enumerate(lignes):
        if ligne.strip() == "<code>":
            to_comment = False
        elif ligne.strip() == "</code></pre>":
            to_comment = True
        if to_comment and ligne.strip() not in ["<code>", "", "</code></pre>"]:
            lignes[i] = lignes[i][:0] + caractere_a_ajouter + lignes[i][0:]

    texte_modifie = "\n".join(lignes)

    return texte_modifie