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
        
    
        
