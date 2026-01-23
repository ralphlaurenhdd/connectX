def check_winning_move(board, column, mark, config):
    # On récupère les dimensions
    columns = config.columns
    rows = config.rows
    inarow = config.inarow
    
    # 1. Trouver dans quelle ligne (row) le jeton tomberait
    # On cherche la ligne vide la plus basse dans cette colonne
    row = max([r for r in range(rows) if board[column + (r * columns)] == 0])
    
    # 2. Vérifier les alignements (Horizontal, Vertical, Diagonales)
    # Elle compte combien de jetons identiques sont alignés à partir d'une direction (dr, dc)
    def count_direction(dr, dc):
        count = 0
        for i in range(1, inarow): # On cherche au maximum 'inarow - 1' jetons autour
            r = row + dr * i
            c = column + dc * i
            # Vérifier si on est toujours dans les limites du plateau
            if 0 <= r < rows and 0 <= c < columns and board[r * columns + c] == mark:
                count += 1
            else:
                # Si on rencontre un vide, l'adversaire ou le bord, on s'arrête net
                break
        return count

    # VÉRIFICATION DES 4 AXES
    # 1. Horizontal : Gauche (0, -1) + Droite (0, 1)
    if (count_direction(0, -1) + count_direction(0, 1) + 1) >= inarow:
        return True
    
    # 2. Vertical : Uniquement vers le bas (1, 0) car rien n'est encore au-dessus
    if (count_direction(1, 0) + 1) >= inarow:
        return True
    
    # 3. Diagonale descendante : Haut-Gauche (-1, -1) + Bas-Droite (1, 1)
    if (count_direction(-1, -1) + count_direction(1, 1) + 1) >= inarow:
        return True
    
    # 4. Diagonale montante : Bas-Gauche (1, -1) + Haut-Droite (-1, 1)
    if (count_direction(1, -1) + count_direction(-1, 1) + 1) >= inarow:
        return True

    return False

def agent(observation, configuration):
    # 1. On extrait les données utiles
    columns = configuration.columns #Nombre de colonnes
    inarow = configuration.inarow #Nombre de jetons alignés nécessaires pour gagner
    row = configuration.rows #Nombre de lignes
    mark = observation.mark #Soit tu es le joueur 1, soit le joueur 2
    board = observation.board #liste de 42 chiffres (si 6x7).
    opp_mark = 3 - mark #le joueur adverse

    # 2. Le code 

    #Un agent ne peut pas jouer dans une colonne qui est déjà pleine
    valid_moves = [c for c in range(configuration.columns) if board[c] == 0]

    #Si je peux gagner tout de suite, je le fais
        # --- PRIORITÉ 1 : GAGNER ---
    for col in valid_moves:
        if check_winning_move(board, col, mark, configuration):
            return col # On a trouvé un coup gagnant, on le joue immédiatement !

        # --- PRIORITÉ 2 : BLOQUER ---
    for col in valid_moves:
        # On simule le coup comme si on était l'adversaire
        if check_winning_move(board, col, opp_mark, configuration):
            return col # On bloque l'adversaire avant qu'il ne gagne

        # --- PRIORITÉ 3 : JOUER (par défaut) ---
        # 1. Calculer l'index de la colonne centrale
    mid = configuration.columns // 2 # Donne 3 pour 7 colonnes

        # 2. Trier les coups valides : plus on est proche de 'mid', plus on arrive en début de liste
    # On trie par la valeur absolue de la distance au centre
    valid_moves.sort(key=lambda x: abs(x - mid))

        # 3. L'agent prend maintenant le premier élément du tri (le plus central)
    return valid_moves[0]

