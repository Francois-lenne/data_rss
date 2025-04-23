import re

class r_code:

    def __init__(self, r_code: str):
        self.r_code  = r_code

    @staticmethod
    def retrieve_line_index_code(self,r_code: str) -> dict:
        """

        retrieve a dict of the emplacement of the balise <code> and </code></pre> in the R file
        :param r_code: the R code as a string
        :return: a dict with the index of the <code> and </code></pre> tags
        """
        # Initialize an empty dict to store the positions
        ref_ligne_code = {
            "begin_code": [],
            "and_code": []
        }
        # add a carriage return before the <code> and </code></pre> tags
        r_code = re.sub(r'(?=<code>)', '\n', r_code)

        r_code = re.sub(r'(?=</code></pre>)', '\n', r_code)

        # add a carriage return after the <code> and </code></pre> tags

        r_code = re.sub(r'(<code>)', r'\1\n', r_code)

        r_code = re.sub(r'(</code></pre>)', r'\1\n', r_code)

        for i, line in enumerate(r_code.splitlines()):  # start à 1 si tu veux une indexation humaine
            if line == "<code>":
                ref_ligne_code["begin_code"].append(i)

            if line == "</code></pre>":
                ref_ligne_code["and_code"].append(i)

        return ref_ligne_code
    

    @staticmethod
    def janitor_code(self,r_code: str) -> str:
        """
        Clean the R code by removing the <code> and </code></pre> tags
        :param r_code: the R code as a string
        :return: the cleaned R code as a string
        """
        # remove the <code> and </code></pre> tags
        r_code = re.sub(r'<code>', '', r_code)
        r_code = re.sub(r'</code></pre>', '', r_code)
        # remove the <pre> and </pre> tags
        r_code = re.sub(r'<pre>', '', r_code)
        r_code = re.sub(r'</pre>', '', r_code)

        bornes_code = r_code.retrieve_line_index_code(r_code)

        code_list = []

    # Maintenant, vérifions chaque ligne
        lignes = r_code.splitlines()
        
        for i, line in enumerate(lignes):
            est_dans_code = False
        for j in range(len(bornes_code["begin_code"])):
            debut = bornes_code["begin_code"][j]
            fin = bornes_code["and_code"][j]
            if debut <= i <= fin:
                est_dans_code = True
                code_list.append(line)
            
                break
    
        if est_dans_code:
            print(f"ligne {i} dans le code")

        else:
            print(f"ligne {i} pas dans le code")

        return r_code
        
    
        
with open("requirements.txt", "r") as f:
    lignes = f.readlines()

ligne_a_modifier = [2,4,5]   # attention : index 2 = 3ème ligne
position = 0
caractere_a_ajouter = "#"

for numero in ligne_a_modifier:
    if lignes[numero].strip()  != "":
        lignes[numero] = (
            lignes[numero][:position] +
            caractere_a_ajouter +
            lignes[numero][position:]
        )

with open("fichier.txt", "w") as f:
    f.writelines(lignes)