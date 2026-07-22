"""
Script de démonstration : affiche tous les prompts possibles générés par la
classe Evolution (i1, e1, e2, m1, m2, s1, post/refine), en utilisant :
  - un faux objet `prompts` (mock de problem_adapter) qui fournit
    get_task / get_func_name / get_inout_inf / get_func_signature
  - un faux LLM (mock de InterfaceLLM) pour ne jamais appeler une vraie API
  - des individus factices (algorithme + code + objective)

Aucune dépendance externe n'est nécessaire. Placez ce fichier au même niveau
que le package contenant evolution.py (ou adaptez l'import ci-dessous),
puis lancez : python show_all_prompts.py
"""

import sys
import types


# -----------------------------------------------------------------------
# 1) Mock de prompts (remplace ce que fournirait normalement problem_adapter)
# -----------------------------------------------------------------------
class MockPrompts:
    def get_task(self):
        return (
            "You are solving the Traveling Salesman Problem (TSP): given a set "
            "of city coordinates, design a heuristic construction algorithm "
            "that produces a short tour visiting every city exactly once."
        )

    def get_func_name(self):
        return "construct_tour"

    def get_inout_inf(self):
        return (
            "The function takes as input the number of cities 'n', a 2D array "
            "'dist' of pairwise distances (n x n), and must output an array "
            "'tour' of length n containing a permutation of city indices "
            "[0, n-1]."
        )

    def get_func_signature(self):
        return "void construct_tour(int n, double **dist, int *tour)"


# -----------------------------------------------------------------------
# 2) Mock du LLM pour ne pas dépendre de .interface_LLM / d'une vraie API
#    (utile si vous voulez aussi tester _get_alg / i1 / e1 etc. de bout en
#    bout, pas seulement les prompts bruts)
# -----------------------------------------------------------------------
class MockLLM:
    def __init__(self, *args, **kwargs):
        pass

    def get_response(self, prompt_content, *args, **kwargs):
        # Réponse factice plausible : accolade + code C fictif
        return (
            "{This heuristic builds the tour greedily by always moving to the "
            "nearest unvisited city, a classic nearest-neighbour construction "
            "with O(n^2) complexity.}\n\n"
            "```c\n"
            "#include <stdbool.h>\n"
            "void construct_tour(int n, double **dist, int *tour) {\n"
            "    bool visited[1000] = {false};\n"
            "    int current = 0;\n"
            "    tour[0] = current;\n"
            "    visited[current] = true;\n"
            "    for (int k = 1; k < n; k++) {\n"
            "        int best = -1;\n"
            "        double best_d = 1e18;\n"
            "        for (int j = 0; j < n; j++) {\n"
            "            if (!visited[j] && dist[current][j] < best_d) {\n"
            "                best_d = dist[current][j];\n"
            "                best = j;\n"
            "            }\n"
            "        }\n"
            "        tour[k] = best;\n"
            "        visited[best] = true;\n"
            "        current = best;\n"
            "    }\n"
            "}\n"
            "```"
        )


# -----------------------------------------------------------------------
# 3) Import de la vraie classe Evolution, en patchant .interface_LLM avant
#    l'import pour éviter toute dépendance réseau / clé API.
#    -> Adaptez "your_package" au nom réel du package contenant evolution.py
# -----------------------------------------------------------------------
PACKAGE_NAME = "your_package"  # <-- remplacez par le vrai nom du package

fake_interface_module = types.ModuleType(f"{PACKAGE_NAME}.interface_LLM")
fake_interface_module.InterfaceAPI = MockLLM
sys.modules[f"{PACKAGE_NAME}.interface_LLM"] = fake_interface_module

try:
    evolution_module = __import__(f"{PACKAGE_NAME}.evolution", fromlist=["Evolution"])
    Evolution = evolution_module.Evolution
except ImportError:
    print(
        f"[!] Impossible d'importer {PACKAGE_NAME}.evolution automatiquement.\n"
        "    -> Modifiez PACKAGE_NAME en haut du script pour qu'il corresponde\n"
        "       au vrai nom de votre package (celui qui contient evolution.py),\n"
        "       OU copiez evolution.py dans le même dossier que ce script et\n"
        "       adaptez l'import ci-dessus en 'from evolution import Evolution'.\n"
    )
    raise


# -----------------------------------------------------------------------
# 4) Individus factices
# -----------------------------------------------------------------------
FAKE_INDIVIDUALS = [
    {
        "algorithm": "Nearest-neighbour construction: always jump to the closest unvisited city.",
        "code": (
            "#include <stdbool.h>\n"
            "void construct_tour(int n, double **dist, int *tour) {\n"
            "    /* nearest-neighbour, version simplifiée */\n"
            "    tour[0] = 0;\n"
            "}\n"
        ),
        "objective": 4213.7,
    },
    {
        "algorithm": "Greedy edge insertion: repeatedly insert the city that increases tour length the least.",
        "code": (
            "#include <float.h>\n"
            "void construct_tour(int n, double **dist, int *tour) {\n"
            "    /* insertion gloutonne, version simplifiée */\n"
            "    tour[0] = 0;\n"
            "}\n"
        ),
        "objective": 3980.2,
    },
    {
        "algorithm": "Savings algorithm adapted from vehicle routing: merge routes with highest savings first.",
        "code": (
            "void construct_tour(int n, double **dist, int *tour) {\n"
            "    /* algorithme des savings, version simplifiée */\n"
            "    tour[0] = 0;\n"
            "}\n"
        ),
        "objective": 4102.9,
    },
]


# -----------------------------------------------------------------------
# 5) Instanciation d'Evolution avec le mock, puis affichage de tous les
#    prompts (get_prompt_* ET les méthodes publiques i1/e1/e2/m1/m2/s1 qui
#    passent aussi par le mock LLM).
# -----------------------------------------------------------------------
def print_section(title):
    print("\n" + "=" * 90)
    print(title)
    print("=" * 90)


def main():
    evo = Evolution(
        api_endpoint="mock-endpoint",
        api_key="mock-key",
        model_LLM="mock-model",
        debug_mode=False,
        prompts=MockPrompts(),
        use_local_llm=False,
        url="",
    )

    # ---- Prompts "bruts" (juste construction de texte, pas d'appel LLM) ----
    print_section("PROMPT i1 (initialisation, aucun individu)")
    print(evo.get_prompt_i1())

    print_section("PROMPT e1 (exploration : algorithme totalement différent)")
    print(evo.get_prompt_e1(FAKE_INDIVIDUALS))

    print_section("PROMPT e2 (exploration guidée par 2 individus)")
    print(evo.get_prompt_e2(FAKE_INDIVIDUALS))

    print_section("PROMPT m1 (mutation : nouvelle forme)")
    print(evo.get_prompt_m1(FAKE_INDIVIDUALS[0]))

    print_section("PROMPT m2 (mutation : nouveaux paramètres)")
    print(evo.get_prompt_m2(FAKE_INDIVIDUALS[0]))

    print_section("PROMPT s1 (synthèse inspirée de tous les individus)")
    print(evo.get_prompt_s1(FAKE_INDIVIDUALS))

    print_section("PROMPT post (description a posteriori du code)")
    print(evo.get_prompt_post(FAKE_INDIVIDUALS[0]["code"], FAKE_INDIVIDUALS[0]["algorithm"]))

    print_section("PROMPT refine (re-description raffinée)")
    print(evo.get_prompt_refine(FAKE_INDIVIDUALS[0]["code"], FAKE_INDIVIDUALS[0]["algorithm"]))

    # ---- Appels de bout en bout (prompt + réponse mockée + parsing) ----
    print_section("APPEL COMPLET i1() -> [code, algorithme] (via MockLLM)")
    code, algo = evo.i1()
    print("Algorithme extrait :", algo)
    print("\nCode extrait :\n", code)

    print_section("APPEL COMPLET e1(parents) -> [code, algorithme] (via MockLLM)")
    code, algo = evo.e1(FAKE_INDIVIDUALS)
    print("Algorithme extrait :", algo)
    print("\nCode extrait :\n", code)


if __name__ == "__main__":
    main()