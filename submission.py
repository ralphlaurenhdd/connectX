#Réseau de Neurones Convolutif

import numpy as np

#Préprocessing de l'observation pour un réseau de neurones convolutionnel
def preprocess(observation, configuration):
    # 1. On transforme la liste plate en grille 2D (6, 7)
    grid = np.array(observation.board).reshape(configuration.rows, configuration.columns)
    
    # 2. On crée les 3 couches (canaux)
    # Couche 1 : Tes pions (1 si c'est ton mark, 0 sinon)
    # Couche 2 : Les pions de l'adversaire (1 si c'est l'autre mark, 0 sinon)
    # Couche 3 : Les cases vides (1 si c'est 0, 0 sinon)
    
    mark = observation.mark
    opp_mark = 3 - mark
    
    layer_me = (grid == mark).astype(np.float32)
    layer_opp = (grid == opp_mark).astype(np.float32)
    layer_empty = (grid == 0).astype(np.float32)
    
    # 3. On empile les couches pour créer un bloc de forme (3, 6, 7)
    # C'est le format standard pour les réseaux de neurones (Channels, Height, Width)
    tensor = np.stack([layer_me, layer_opp, layer_empty], axis=0)
    
    return tensor #tenseur (3, 6, 7)

#Architecture CNN

import torch
import torch.nn as nn
import torch.nn.functional as F

class ConnectXNet(nn.Module):
    def __init__(self):
        super(ConnectXNet, self).__init__()
        
        # 1. ÉTAPE DE SCAN (Convolution)
        # On utilise 32 filtres de taille 4x4 pour repérer les alignements
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=32, kernel_size=4, padding=1)
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1)
        
        # 2. ÉTAPE D'APLATISSEMENT (Flatten)
        # On transforme les grilles en une liste de chiffres pour la logique
        self.flatten = nn.Flatten()
        
        # 3. ÉTAPE DE RAISONNEMENT (Couches Linéaires)
        # On calcule le nombre de neurones après convolution : 64 filtres * 5 lignes * 6 colonnes
        self.fc1 = nn.Linear(64 * 5 * 6, 128) # 128 neurones pour réfléchir
        
        # 4. DÉCISION FINALE
        # 7 neurones de sortie (un pour chaque colonne du jeu)
        self.fc2 = nn.Linear(128, 7)

    def forward(self, x):
        # Passage dans les scanners avec activation ReLU
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        
        # Transformation en liste
        x = self.flatten(x)
        
        # Réflexion logique
        x = F.relu(self.fc1(x))
        
        # Scores finaux pour les 7 colonnes
        return self.fc2(x)

