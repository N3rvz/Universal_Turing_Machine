##############
##Question 1##
##############

class MT:
    def __init__(self, etats, alphabet_entree, alphabet_travail, transitions, rub=1):
        self.etats = etats #ensemble fini des états
        self.alphabet_entree = alphabet_entree 
        self.alphabet_travail = alphabet_travail
        self.transitions = transitions #ensemble des transitions (dictionnaire)
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
        self.pos_tete = pos_tete #liste de r positions?
        
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
    
    
    etat_init_file = None
    etat_finale_file = None
    
    for line in clean_lines:
        if line.startswith("init"):
            etat_init_file = line.split(":")[1].strip()
        elif line.startswith("accept"):
            etat_finale_file = line.split(":")[1].strip()
    
    def mapper(nom):
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
            parts_in = [p.strip() for p in line.split(",")]
            etat_courant = mapper(parts_in[0]) # q0,0
            symboles_lus = tuple(parts_in[1:])
            
            etats.add(etat_courant)
            alphabet_travail.update(symboles_lus)
            
            #ligne 2
            i += 1
            if i < len(clean_lines):
                line_out = clean_lines[i]
                parts_out = [p.strip() for p in line_out.split(",")]
                
                etat_suivant = mapper(parts_out[0]) # qRight0,_,>
                rub = len(symboles_lus) #Déduit le nombre de rubans
                symboles_ecrits = tuple(parts_out[1:rub+1])
                direction = tuple(parts_out[rub+1:])
                
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
        pos = config.pos_tete[i]
        rubans = config.rubans[i]

        if pos >= len(rubans):
            rubans.append('_')
            
        symboles_lus.append(rubans[pos])
        
    cle_transition = (config.etat_courant, tuple(symboles_lus))
    
    if cle_transition not in mt.transitions:
        return False
    
    #Les actions
    etat_suivant, symboles_ecrits, direction = mt.transitions[cle_transition]
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
        if not un_pas_de_calcul(mt, config):
            break
        
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
    








#TESTS
mt = parse_file("palindrome.txt")
config = config_init("10101", mt)
print(config)

resultat = un_pas_de_calcul(mt, config)
print(config)
print("Transition appliquée :", resultat)

details_simulation = afficher_simulation("10101", mt)
print(f"Voici chaque étape de la simulation: \n {details_simulation}")
simulation_complete = simuler("10101", mt)
print(f"Voici une simulation complète : \n {simulation_complete}")

