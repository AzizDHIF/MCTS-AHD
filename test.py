"""
Script de debug : affiche le texte COMPLET de chaque prompt que evolution.py
peut générer, sans jamais appeler le LLM (get_prompt_* sont de purs
constructeurs de string, ils ne touchent pas self.interface_llm).

A adapter : la construction de `problem` / `prompts` ci-dessous doit
correspondre exactement à ce que fait ton vrai point d'entrée (main.py /
Hydra) pour charger la config du problème mo_mkp_aco. Remplace le bloc
marqué "ADAPTE ICI" par ton propre chargement de config si besoin.
"""

import logging
from evolution import Evolution
from prob import Problem  # adapte le nom du module si prob.py a un autre nom d'import

logging.basicConfig(level=logging.INFO)


def print_block(title, content):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)
    print(content)
    print("=" * 80 + "\n")


# -----------------------------------------------------------
# ADAPTE ICI : construction de la config / du problème réel.
# Exemple minimal si tu utilises Hydra ailleurs dans le projet ; remplace par
# ton propre chargement (souvent une fonction déjà présente dans ton main.py).
# -----------------------------------------------------------
import hydra
from omegaconf import DictConfig


@hydra.main(version_base=None, config_path="cfg", config_name="config")
def main(cfg: DictConfig):

    root_dir = hydra.utils.get_original_cwd()
    problem = Problem(cfg, root_dir)

    # kwargs minimaux attendus par Evolution.__init__ / InterfaceAPI
    evol = Evolution(
        api_endpoint=cfg.llm_api_endpoint,
        api_key=cfg.llm_api_key,
        model_LLM=cfg.llm_model,
        debug_mode=False,
        prompts=problem.prompts,
        use_local_llm=cfg.llm_use_local,
        url=cfg.llm_local_url,
    )

    # Individus factices pour pouvoir construire les prompts e1/e2/m1/m2/s1,
    # qui ont besoin d'algorithmes "existants" pour être assemblés.
    dummy_indiv_1 = {
        "algorithm": "DUMMY design idea 1: sort by profit/weight ratio.",
        "code": "double heuristic_v2(...) { /* dummy code 1 */ }",
        "objective": 123.456,
    }
    dummy_indiv_2 = {
        "algorithm": "DUMMY design idea 2: greedy remaining capacity.",
        "code": "double heuristic_v2(...) { /* dummy code 2 */ }",
        "objective": 98.765,
    }
    dummy_pop = [dummy_indiv_1, dummy_indiv_2]

    print_block("PROMPT i1 (initialisation)", evol.get_prompt_i1())
    print_block("PROMPT e1 (exploration)", evol.get_prompt_e1(dummy_pop))
    print_block("PROMPT e2 (exploitation)", evol.get_prompt_e2(dummy_pop))
    print_block("PROMPT m1 (mutation 1)", evol.get_prompt_m1(dummy_indiv_1))
    print_block("PROMPT m2 (mutation 2 - parametres)", evol.get_prompt_m2(dummy_indiv_1))
    print_block("PROMPT s1 (synthese population)", evol.get_prompt_s1(dummy_pop))
    print_block("PROMPT post (description initiale)", evol.get_prompt_post(dummy_indiv_1["code"], dummy_indiv_1["algorithm"]))
    print_block("PROMPT refine (re-description)", evol.get_prompt_refine(dummy_indiv_1["code"], dummy_indiv_1["algorithm"]))

    print_block("INSTRUCTIONS C COMMUNES (_c_instructions, injectees dans i1/e1/e2/m1/m2/s1)", evol._c_instructions())


if __name__ == "__main__":
    main()