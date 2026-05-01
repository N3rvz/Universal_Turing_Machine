import argparse
##############
##Question 1##
##############
class MT:
    def __init__(self, etats, alphabet_entree, alphabet_travail, transitions, rub=1):
        self.etats = etats #ensemble fini des états
        self.alphabet_entree = alphabet_entree 
        self.alphabet_travail = alphabet_travail
        self.transitions = transitions #ensemble des transitions (dictionnaire de tuples) {(q0, (0, 1)): (q1, _, >)}
        self.rub = rub #nombre de rubans
        self.etat_initial = "I"
        self.etat_final = "F"
    
    def __str__(self):
        return f"""Définition formelle de la MT : 
        Alphabet d'entrée : {self.alphabet_entree}, 
        Alphabet de travail : {self.alphabet_travail},
        Ensemble des états : {self.etats}, 
        Etat initial: {self.etat_initial}, 
        Ensemble de transitions : {self.transitions}"""
        

class Configuration:
    def __init__(self, etat_courant, rubans, pos_tete):
        self.etat_courant = etat_courant
        self.rubans = rubans #liste de listes
        self.pos_tete = pos_tete #liste de rub positions
        
    def __str__(self):
        result = f"Etat : {self.etat_courant}\n"
        for i, ruban in enumerate(self.rubans):
            pos = self.pos_tete[i]
            prefixe = f"Ruban {i+1} : "
            result += f"Ruban {i+1} : {' '.join(ruban)}\n"
            result += f"{' ' * len(prefixe)}{' ' * (2 * pos)}^\n"
        return result


##############
##Question 2##
##############

def parse_file(MT_file):
    with open(MT_file, "r") as f:
        lines = f.readlines()
    
    etats = set()
    alphabet_entree = set()
    alphabet_travail = set(['_'])
    transitions = {}
    etat_initial = "I"
    etat_final = "F"
    rub = 1
    
    clean_lines = []
    for line in lines:
        line = line.strip()
        
        if line == "" or line.startswith("//"):
            continue
        clean_lines.append(line)
    
    
    etat_init_file = None #variable qui va prendre la valeur "init:q0" qui est la convention sur les fichiers de TMSimulator
    etat_finale_file = None #valeur "accept:qAccept"
    
    for line in clean_lines:
        if line.startswith("init"):
            etat_init_file = line.split(":")[1].strip()
        elif line.startswith("accept"):
            etat_finale_file = line.split(":")[1].strip()
    
    def mapper(nom):
        """Cette fonction va mapper les valeurs du site sur les valeurs par défaut du projet"""
        if nom == etat_init_file: return 'I'
        if nom == etat_finale_file: return 'F'
        return nom
    
    i = 0
    while i < len(clean_lines):
        line = clean_lines[i]
        
        if line.startswith(("name", "init", "accept")):
            i += 1
            continue
        
        else: #Transitions
            #ligne 1
            ligne_1 = [p.strip() for p in line.split(",")]
            etat_courant = mapper(ligne_1[0]) # "q0" -> "I"
            symboles_lus = tuple(ligne_1[1:])
            
            etats.add(etat_courant)
            alphabet_travail.update(symboles_lus)
            
            #ligne 2
            i += 1
            if i < len(clean_lines):
                line_out = clean_lines[i]
                ligne_2 = [p.strip() for p in line_out.split(",")]
                
                etat_suivant = mapper(ligne_2[0]) # qRight0,_,>
                rub = len(symboles_lus) #Déduit le nombre de rubans
                symboles_ecrits = tuple(ligne_2[1:rub+1])
                direction = tuple(ligne_2[rub+1:])
                
                alphabet_travail.update(symboles_ecrits)
                transitions[(etat_courant, symboles_lus)] = (etat_suivant, symboles_ecrits, direction)
            i += 1
    return MT(etats, alphabet_entree, alphabet_travail, transitions, rub)


def config_init(mot, mt):
    rubans = []
    
    if not mot:
        rubans_1 = ['_']
    else:
        rubans_1 = list(mot)
    rubans.append(rubans_1)
    
    for _ in range (1, mt.rub):
        rubans.append(['_'])
        
    pos_tete = [0]*mt.rub

    return Configuration(mt.etat_initial, rubans, pos_tete)
    
        
##############
##Question 3##
##############

def un_pas_de_calcul(mt, config):
    if config.etat_courant == mt.etat_final:
        return False

    symboles_lus = []
    for i in range(mt.rub):
        pos = config.pos_tete[i] #Recupere l'index de la tete de lecture sur ce ruban
        rubans = config.rubans[i] #recuperer le i-eme ruban

        if pos >= len(rubans):
            rubans.append('_') #simule le ruban infini
            
        symboles_lus.append(rubans[pos]) #Stocker les caracteres lus dans une liste temporaire
        
    cle_transition = (config.etat_courant, tuple(symboles_lus))
    
    if cle_transition not in mt.transitions:
        return False

    #Faire la transition
    etat_suivant, symboles_ecrits, direction = mt.transitions[cle_transition] #le Tuple unpacking c'est génial
    config.etat_courant = etat_suivant

    #On les appliques pour chaque ruban
    for i in range(mt.rub):
        pos = config.pos_tete[i]
        #Ecriture
        config.rubans[i][pos] = symboles_ecrits[i]

        #Deplacement
        if direction[i] in ('>', 'R'):
            config.pos_tete[i]+=1
            if config.pos_tete[i]>=len(config.rubans[i]):
                config.rubans[i].append('_')
        elif direction[i] in ('<', 'L'):
            if config.pos_tete[i]==0:
                config.rubans[i].insert(0, '_')
            else:
                config.pos_tete[i] -= 1
                
    return True



###############
##Question 4###
###############

def simuler(mot, mt):
    config = config_init(mot, mt) 
    while config.etat_courant != mt.etat_final:
        if not un_pas_de_calcul(mt, config): #on vérifie si le mot est accepté (cle_transition)
            break
        
    return config

################
###QUESTION 10##
################

def simuler_borne(mot, mt, n_max):
    """Simulateur avec limite de temps (Time-Bounded Emulator) pour la Q10"""
    config = config_init(mot, mt)
    etapes = 0
    
    print(f"--- Début de la simulation (Max {n_max} étapes) ---")
    
    while config.etat_courant != mt.etat_final:
        # LE PÉAGE : On vérifie si le crédit est épuisé (équivalent du Ruban 4 vide)
        if etapes >= n_max:
            print(f"[\u274c] ARRÊT FORCÉ : La machine n'a pas terminé après {n_max} étapes.")
            print("-> Prévention d'une boucle infinie réussie.")
            return config
        
        # Si on a encore du crédit, on fait un pas
        if not un_pas_de_calcul(mt, config):
            print("[\u26a0\ufe0f] Machine bloquée (pas de transition trouvée).")
            break
            
        etapes += 1
        
    if config.etat_courant == mt.etat_final:
        print(f"[\u2705] SUCCÈS : La machine a atteint l'état final en {etapes} étapes.")
        
    return config

################
###QUESTION 5###
################

def afficher_simulation(mot, mt):
    config = config_init(mot, mt)
    print(f"Voici la configuration initiale : \n {config}")
    while config.etat_courant != mt.etat_final:
        if not un_pas_de_calcul(mt, config):
            print("Machine bloquée (pas de transition)")
            break
        print(f"Voici une suite de config: \n {config}")
    return config
    










####################################
###### Machine Universelle##########
####################################


###############
## Question 7##
###############

def codage_mu(mt):
    """
    Encode une définition de Machine de Turing (MT) en une chaîne de caractères unique,
    représentant la première étape vers une Machine de Turing Universelle.
    L'encodage est spécifique aux machines à un seul ruban pour cette implémentation.

    Le format de sortie est une chaîne de transitions séparées par '|', où chaque
    transition est de la forme: etat_depart|symbole_lu|symbole_ecrit|direction|etat_arrivee
    """
    morceaux = []
    # 'I' est mappé à '0', 'F' à '1'. Les autres états sont mappés à leur représentation binaire.
    map_etat = {mt.etat_initial: '0', mt.etat_final: '1'}
    compteur_etat = 2 # Commence à 2 car 0 et 1 sont réservés.
    
    def mapping_etats(nom):
        nonlocal compteur_etat # Permet de modifier la variable de la fonction parente.
        if nom not in map_etat:
            map_etat[nom] = bin(compteur_etat)[2:]
            compteur_etat += 1
        return map_etat[nom]    
        
    for (etat_courant, symboles_lus), (etat_suivant, symboles_ecrits, directions) in mt.transitions.items():
        e1 = mapping_etats(etat_courant)
        e2 = mapping_etats(etat_suivant)
        

        # NOTE: Cette version ne gère que les machines à un seul ruban pour le codage.
        s1 = symboles_lus[0]
        s2 = symboles_ecrits[0]
        
        d = directions[0]        
        # On construit le bloc de transition sans saut de ligne.
        bloc = f"{e1}|{s1}|{s2}|{d}|{e2}"
        morceaux.append(bloc)
        
    
    # On joint toutes les représentations de transition avec '|'.
    return "|".join(morceaux)

################
###QUESTION 8###
################

def codage_binaire(mt):
    # 1. On récupère le code de la Question 7
    code_str = codage_mu(mt)
    
    # 2. Notre dictionnaire de traduction défini arbitrairement sur 4 bits
    table_binaire = {
        '0': '0000',
        '1': '0001',
        '|': '0010',
        '>': '0011',
        '<': '0100',
        '-': '0101',
        '_': '0110',
        '#': '0111'
    }
    
    # Sécurité : Si un caractère inconnu de l'alphabet apparaît, on lui crée un code dynamique
    compteur_inconnu = 8 
    
    code_bin = ""
    for char in code_str:
        if char not in table_binaire:
            # zfill(4) permet de toujours garder un bloc de 4 chiffres (ex: '1000')
            table_binaire[char] = bin(compteur_inconnu)[2:].zfill(4)
            compteur_inconnu += 1
            
        code_bin += table_binaire[char]
        
    # 3. Interprétation mathématique (on dit à Python de lire le texte comme un nombre en base 2)
    entier_associe = int(code_bin, 2)
    
    return code_str, code_bin, entier_associe


def main():
    #On créé l'analyseur
    parser = argparse.ArgumentParser(description = "Simulateur et Interpreteur de machine de Turing")
    
    #Creation des arguments
    parser.add_argument("-q", "--question", type=int, required=True,
                        help="Numéro de la question à exécuter (ex: 4, 5, 6...)")
    parser.add_argument("-f", "--file", type=str, help="Chemin vers le fichier de la machine au format Turing machine simulator")
    parser.add_argument("-w", "--word", type=str, help="Mot d'entrée pour la simulation sur le ruban")
    
    #Lecture des args
    args = parser.parse_args()
    
    if args.question == 1:
        print('La question 1 correspond aux structures de données (classes MT et Configuration)')
    
    elif args.question == 2:
        if not args.file or args.word is None:
            print(f" Erreur, Q2 nécessite -f et -w")
            return
        print(f"===== Q2 : Initialisation MT et Configuration ====")
        mt = parse_file(args.file)
        config = config_init(args.word, mt)
        print(config)
        
    elif args.question == 3:
        if not args.file or args.word is None:
            print("Erreur : Q3 nécessite --file et --word")
            return
        print(f"==== Question 3 =====")
        mt = parse_file(args.file)
        config = config_init(args.word, mt)
        print(f"Configuration initiale :\n")
        print(config)
        un_pas_de_calcul(mt, config)
        print(f"Configuration après un pas de calcul :\n {config}")
    
    
    elif args.question == 4:
        if not args.file or args.word is None:
            print(f"Erreur, la question 4 nécessite un fichier (--file) et un mot d'entrée (--word)")
            return
        print(f"========Simulation (Q4) de {args.file} avec le mot {args.word} ==========")
        mt = parse_file(args.file)
        simule = simuler(args.word ,mt)
        print(simule)
    
    elif args.question == 5:
        if not args.file or args.word is None:
            print(f"----- Erreur: Q5 nécessite --file et --word")
            return
        print(f"=== Q5 : Simulation avec affichages")
        mt = parse_file(args.file)
        print(afficher_simulation(args.word, mt))
        
    elif args.question == 6:
        if not args.file or args.word is None:
            print("Erreur: Question 6 nécessite un fichier -f et un mot d'entrée -w")
            return
        print(f"==== Q6: Test de la machine: {args.file} ====")
        mt = parse_file(args.file)
        afficher_simulation(args.word, mt)
    
    elif args.question == 7:
        if not args.file:
            print(f"Erreur: Q7 nécessite un fichier -f (MTS)")
            return
        print(f"==== Question 7 : Traduction en code <M> ====")
        mt = parse_file(args.file)
        code_machine = codage_mu(mt)
        print(code_machine)
      
    elif args.question == 8:
        if not args.file:
            print("Erreur: Q8 nécessite un fichier -f (MTS)")
            return
        print("==== Question 8 : Codage binaire et Entier ====")
        mt = parse_file(args.file)
        code_str, code_bin, entier = codage_binaire(mt)
        
        print(f"Codage <M> d'origine : \n{code_str}\n")
        print(f"Codage purement binaire : \n{code_bin}\n")
        print(f"Interprétation en entier (Nombre de Gödel) : \n{entier}\n")    
    
    elif args.question == 9:
        if not args.file or not args.word:
            print("Erreur: Q9 nécessite la machine à simuler (-f) et le mot de départ (-w)")
            return
            
        print("==== Question 9 : Préparation de la Machine Universelle ====")
        
        # 1. On charge la petite machine (ex: le palindrome) pour récupérer son code
        mt_cible = parse_file(args.file)
        code_M = codage_mu(mt_cible)
        mot_x = args.word
        
        # 2. On génère le ruban d'entrée de la Machine Universelle : <M>#x
        ruban_entree_mu = f"{code_M}#{mot_x}"
        print(f"Ruban d'entrée généré pour la MU :\n{ruban_entree_mu}\n")
        
        print("Note : La simulation complète d'une MU nécessite un fichier texte MU.txt très lourd.")
        print("Si un fichier MU.txt est fourni, on le lance comme ceci :")
        print("# mt_mu = parse_file('MU.txt')")
        print("# simuler(ruban_entree_mu, mt_mu)")
        
        # On valide la démonstration en montrant qu'on sait créer la configuration à 3 rubans
        print("Aperçu de la configuration initiale de la MU (3 rubans) :")
        # On force temporairement la machine cible à 3 rubans pour l'affichage de la config initiale
        mt_cible.rub = 3 
        config_mu = config_init(ruban_entree_mu, mt_cible)
        print(config_mu)

   elif args.question == 10:
        if not args.file or not args.word or args.steps is None:
            print("Erreur: Q10 nécessite un fichier (-f), un mot (-w) et un nombre d'étapes (-n)")
            return
            
        print(f"==== Question 10 : Simulation de {args.file} avec limite de {args.steps} étapes ====")
        mt_cible = parse_file(args.file)
        
        # On lance notre processeur borné (Time-Bounded Emulator)
        simuler_borne(args.word, mt_cible, args.steps) 
        
    else:
        print(f"La question {args.question} n'es pas encore implémentée ou reconnue.")
        
if __name__ == "__main__":
    main()
