# 🧠 ConnectX — Recherche adversariale et réseau de neurones de valeur

## 🎯 Mise en contexte

Ce projet propose un agent pour le jeu **ConnectX** (variante du Puissance 4) en combinant :

- une **recherche adversariale classique** (*Negamax + Alpha-Beta*),
- un **réseau de neurones convolutionnel de valeur (CNN)**,
- des **heuristiques simples** (victoire immédiate, blocage adverse).

Contrairement à une approche en *reinforcement learning pur*, nous exploitons le caractère **déterministe** et **à information parfaite** du jeu pour obtenir un agent :

- plus **stable**,
- plus **interprétable**,
- et plus **efficace en temps de calcul**.

L’apprentissage est réalisé via du *self-play*.  
Pendant la partie, l’agent n’apprend plus : il utilise le réseau uniquement comme **fonction d’évaluation** intégrée à une recherche dans l’arbre des coups.


## 🚀 Objectifs du projet

L’objectif principal de ce projet est de concevoir un **agent compétitif pour ConnectX** en tirant parti des propriétés du jeu :  
déterministe, à information parfaite et à espace d’état relativement restreint.

Plus précisément, nos objectifs sont :

- 🎯 **Construire un agent capable de battre systématiquement un joueur aléatoire**
- 🧠 **Atteindre un score élevé face à un agent Negamax de référence**
- 🔍 **Combiner apprentissage et recherche**, plutôt que d’utiliser du reinforcement learning pur


## 🎮 Règles du jeu (ConnectX)

ConnectX est un jeu de type *Puissance 4* opposant deux joueurs sur un plateau rectangulaire.

### Plateau

- Le plateau est composé de **6 lignes** et **7 colonnes**
- Les joueurs jouent à tour de rôle
- Un coup consiste à **insérer un pion dans une colonne**
- Le pion tombe automatiquement dans la **case libre la plus basse** de la colonne

### Objectif

Le but du jeu est d’aligner **4 pions consécutifs** (*inarow = 4*) :

- horizontalement  
- verticalement  
- ou en diagonale  

avant l’adversaire.

### Fin de partie

Une partie se termine dans l’un des cas suivants :

- ✅ un joueur aligne 4 pions → **victoire**
- 🤝 le plateau est rempli sans alignement → **match nul**

### Informations supplémentaires

ConnectX est un jeu :

- **déterministe** : aucune part de hasard
- à **information parfaite** : les deux joueurs voient l’intégralité du plateau
- à **deux joueurs en opposition directe**

Ces propriétés rendent le jeu particulièrement adapté à :

- la recherche adversariale (Minimax / Negamax)
- les algorithmes d’élagage (Alpha-Beta)
- l’apprentissage par self-play

## 🧪 Approches testées

Avant d’aboutir à la solution finale, plusieurs approches ont été explorées et comparées.


### Approches de Reinforcement Learning pur

Nous avons initialement testé des méthodes classiques de reinforcement learning, notamment :

- **Q-learning**
- **PPO (Proximal Policy Optimization)**

#### Limites observées

Ces approches se sont révélées peu adaptées au jeu ConnectX :

- apprentissage lent et instable
- difficulté à explorer efficacement l’espace des états
- performances faibles contre un adversaire déterministe (Negamax)
- absence d’exploitation explicite de la structure du jeu (alignements, symétries, coups forcés)

👉 Ces méthodes sont généralement plus efficaces dans des environnements **stochastiques** ou à **information imparfaite**, alors que ConnectX est un jeu **déterministe à information parfaite**.


### Recherche adversariale classique seule

Nous avons également testé une approche basée uniquement sur :

- **Negamax + Alpha-Beta**
- sans apprentissage

#### Limites observées

- performances dépendantes de la profondeur de recherche
- coût computationnel élevé pour des profondeurs importantes
- incapacité à évaluer finement les positions non terminales profondes


### Conclusion des essais

Aucune de ces approches prises isolément n’a permis d’obtenir des performances satisfaisantes.

## 🧠 Stratégie finale retenue

Face aux limites du reinforcement learning pur, nous avons retenu une approche **hybride**, combinant des méthodes classiques de recherche et de l’apprentissage supervisé.

### 🎯 Idée clé

**Combiner la recherche exacte (Negamax + Alpha-Beta) avec un réseau de neurones de valeur**, afin de bénéficier à la fois :

- de la rigueur des algorithmes déterministes,
- et de la capacité d’approximation d’un CNN.


### 🧩 Composants de la solution

#### 1️⃣ Réseau de neurones de valeur (CNN)

- Le CNN ne prédit **pas un coup**, mais la **qualité d’une position**.
- Il estime une valeur dans l’intervalle **[-1, 1]** :
  - +1 : position gagnante
  - 0 : position équilibrée
  - −1 : position perdante
- Il est entraîné à partir de parties jouées en **self-play**.

➡️ Le réseau agit comme **fonction d’évaluation** pour la recherche.

#### 2️⃣ Recherche Negamax + Alpha-Beta

- Exploration de l’arbre des coups possibles.
- Alternance automatique joueur / adversaire (Negamax).
- **Élagage Alpha-Beta** pour réduire fortement le nombre de positions explorées.
- Deux cas lors de la recherche :
  - position terminale → score exact
  - profondeur limite atteinte → évaluation par le CNN

➡️ La décision finale est toujours prise par la recherche, pas par le réseau seul.


#### 3️⃣ Heuristiques déterministes

Pour améliorer l’efficacité et la stabilité :

- victoire immédiate si possible
- blocage d’une victoire adverse immédiate
- ordre de coups centré (meilleur élagage Alpha-Beta)

### ✅ Pourquoi cette approche fonctionne

- **Negamax** assure un raisonnement exact sur les coups proches.
- **CNN** fournit une estimation rapide des positions profondes.
- **Alpha-Beta** réduit massivement le temps de calcul.

👉 Cette combinaison s’est révélée nettement la plus efficace.


## 🔁 Pipeline complet de la solution

L’idée centrale est la suivante :

> **Plateau → Évaluation → Recherche → Décision**


### 1️⃣ Évaluation d’une position

Toute position de jeu est évaluée selon une règle hiérarchique :

1. **Position terminale**
   - victoire → `+1`
   - défaite → `-1`
   - match nul → `0`

2. **Position non terminale**
   - estimation fournie par le **CNN de valeur**

➡️ Le réseau n’est donc utilisé **uniquement** lorsque l’évaluation exacte n’est pas possible.

### 2️⃣ Recherche adversariale (Negamax + Alpha-Beta)

À partir de la fonction d’évaluation, l’agent effectue une recherche dans l’arbre des coups :

- exploration des coups légaux
- alternance automatique joueur / adversaire (Negamax)
- maximisation de la valeur du joueur courant

#### Optimisations intégrées

- **Alpha-Beta pruning**  
  → coupe les branches qui ne peuvent pas influencer la décision finale

- **ordre de coups centré**  
  → améliore fortement l’efficacité de l’élagage

Deux situations durant la recherche :

- **profondeur maximale atteinte** → appel au CNN
- **position terminale rencontrée** → score exact immédiat


### 3️⃣ Sélection du meilleur coup

Pour chaque coup possible :

1. simulation du coup
2. lancement de la recherche Negamax
3. récupération du score associé

Le coup ayant le **score maximal** est sélectionné.

Des heuristiques simples sont appliquées en priorité :

- gagner immédiatement si possible
- bloquer une victoire adverse immédiate


### 4️⃣ Génération des données par self-play

L’apprentissage du CNN est réalisé **en dehors des parties réelles**, via du self-play :

- l’agent joue contre lui-même
- chaque partie est jouée jusqu’à son terme
- chaque coup génère un exemple :
  - état du plateau
  - joueur courant
  - résultat final de la partie (`+1 / 0 / -1`)

### 5️⃣ Apprentissage par cycles

L’entraînement est organisé en **cycles successifs** :

1. self-play avec le modèle courant
2. augmentation de données par symétrie gauche ↔ droite
3. entraînement léger du CNN (peu d’epochs)
4. évaluation contre :
   - un agent aléatoire
   - un Negamax de référence
5. sauvegarde uniquement du meilleur modèle


### 6️⃣ Utilisation finale en compétition

Lors d’une partie Kaggle :

- le modèle est chargé une seule fois
- aucun apprentissage n’a lieu
- l’agent ne fait que :
  - appeler la recherche
  - utiliser le CNN comme fonction d’évaluation
  - retourner le coup optimal


## 🧩 Architecture du réseau de neurones de valeur (CNN)

Le réseau de neurones utilisé dans ce projet est un **CNN de valeur** :  

Son rôle est d’approximer la fonction : *valeur(position, joueur)* → **[-1, 1]**


### 🎯 Entrée du réseau

Le plateau est encodé sous forme de **3 canaux** :

1. pions du joueur courant  
2. pions de l’adversaire  
3. cases vides  

Chaque canal est une matrice binaire de taille : (lignes × colonnes)


Ce format permet :

- de distinguer clairement les rôles des joueurs
- de rester invariant au joueur courant
- de capter naturellement les motifs spatiaux (alignements, menaces)


### 🧠 Architecture interne

Le réseau est volontairement **simple et léger**, afin d’éviter l’overfitting.

#### Couches convolutionnelles

- **Conv2D (3 → 32)**
  - capte les motifs locaux simples (paires, débuts d’alignements)
- **Conv2D (32 → 64)**
  - capte des motifs plus complexes (menaces, configurations gagnantes)

Chaque couche est suivie d’une activation **ReLU**.


#### Couches entièrement connectées

- **Fully Connected**
  - transforme les caractéristiques spatiales en une représentation globale
- **Sortie : 1 neurone**

Activation finale :

- **tanh**, pour borner la sortie dans **[-1, 1]**


### 📤 Sortie et interprétation

La sortie du réseau est un **scalaire réel** :

- **+1** → position gagnante
- **0** → position équilibrée
- **−1** → position perdante

Cette valeur est utilisée **exclusivement comme fonction d’évaluation**  
lors de la recherche Negamax.


## 🔄 Entraînement du réseau de valeur

L’entraînement du CNN repose sur un **apprentissage supervisé** à partir de données générées par **self-play**.  

### 🎮 Génération des données par self-play

L’agent joue contre lui-même en utilisant :

- la recherche **Negamax + Alpha-Beta**
- le CNN courant comme fonction d’évaluation
- un **bruit contrôlé (epsilon-greedy)** en début de partie pour favoriser l’exploration

Chaque partie est jouée **jusqu’à une victoire ou un match nul**.


### 🧾 Construction du dataset

Pour chaque partie jouée :

- chaque position rencontrée est stockée
- on associe à chaque position :
  - l’état du plateau
  - le joueur courant
  - la valeur finale de la partie :
    - +1 si le joueur gagne
    - 0 en cas de match nul
    - −1 si le joueur perd

➡️ Une seule partie génère **des dizaines de positions annotées**.


### 🔁 Augmentation de données par symétrie

Pour chaque position collectée :

- on applique une **symétrie gauche ↔ droite** du plateau
- la valeur et le joueur restent identiques

Avantages :

- double instantanément la taille du dataset
- améliore la généralisation
- coût de calcul nul

### 🧠 Apprentissage supervisé

Le CNN est entraîné à prédire la **valeur finale de la position**.

- fonction de perte : **MSE (Mean Squared Error)**
- optimiseur : **Adam**
- learning rate réduit pour la stabilité
- entraînement sur **peu d’epochs** pour éviter l’overfitting

### 🔄 Apprentissage par cycles

L’entraînement est organisé en **cycles successifs** :

1. self-play avec le modèle courant  
2. collecte des positions  
3. entraînement léger du CNN  
4. évaluation du modèle


### 🎯 Évaluation continue

Après chaque cycle, le modèle est évalué contre :

- un joueur **Random** (sanity check)
- un agent **Negamax** de référence

Seul le modèle obtenant les **meilleures performances** est sauvegardé.


### ⚙️ Hyperparamètres clés

- nombre de cycles : progressif
- parties par cycle : limité pour éviter des données trop corrélées
- epochs par cycle : 2 à 3 maximum
- ε-greedy décroissant au fil des cycles


## 📊 Résultats et performances

Les performances de l’agent ont été évaluées de manière systématique après chaque cycle d’entraînement, en modifiant les hyperparamètres.

L’évaluation est réalisée via des matchs contre :

- un joueur **Random** (référence basse)
- un agent **Negamax** (référence forte et déterministe)


### 🧪 Configuration expérimentale

Exemple de configuration ayant donné les meilleurs résultats :

- **TOTAL_CYCLES** = 5  
- **GAMES_PER_CYCLE** = 200  
- **EPOCHS_PER_CYCLE** = 3  
- **Learning rate** = 0.0005  
- **ε-greedy initial** = 0.15 (décroissant)

---

### 🏆 Résultats obtenus

#### Performance contre Random

- Score moyen ≈ **1.0**
- Victoire quasi systématique

➡️ L’agent a appris des stratégies solides et ne commet plus d’erreurs grossières.


#### Performance contre Negamax

- Amélioration progressive au fil des cycles
- Score final atteint : **≈ 0.9**

Extrait des résultats :

Cycle 1 : Score vs Negamax ≈ 0.62
Cycle 2 : Score vs Negamax ≈ 0.66
Cycle 3 : Score vs Negamax ≈ 0.47
Cycle 4 : Score vs Negamax ≈ 0.63
Cycle 5 : Score vs Negamax ≈ 0.90


➡️ Le modèle final dépasse nettement la version Negamax de référence.


### 📉 Évolution de la perte (loss)

- Diminution régulière de la loss au fil des cycles
- Stabilisation rapide avec peu d’epochs
- Absence de divergence ou d’explosion du gradient

➡️ Cela confirme que le CNN apprend une **fonction de valeur cohérente**.

### 🔍 Observations clés

- Plus de données ≠ meilleur modèle
- Trop d’epochs dégrade parfois les performances contre Negamax
- L’apprentissage par cycles est plus efficace qu’un entraînement massif
- Le bruit contrôlé (ε-greedy) améliore la diversité des positions


## ⚠️ Difficultés rencontrées

Le développement de cet agent a soulevé plusieurs difficultés, aussi bien techniques que méthodologiques.  


### 🎛️ Choix des hyperparamètres

L’un des principaux défis a été le réglage des hyperparamètres :

- **Learning rate trop élevé**  
  → convergence rapide mais surapprentissage  
- **Trop d’epochs**  
  → baisse des performances contre Negamax malgré une loss faible  
- **Trop de parties par cycle**  
  → données fortement corrélées, peu informatives

➡️ Ces phénomènes ont montré que **minimiser la loss ne garantit pas de meilleures performances en jeu**.

### 🔁 Corrélation des données en self-play

L’apprentissage par self-play présente un risque majeur :

- l’agent joue contre lui-même
- il peut renforcer ses propres biais
- certaines stratégies deviennent sur-représentées

➡️ Pour limiter ce problème :

- entraînement **par cycles**
- ajout de **bruit contrôlé (ε-greedy)** en début de partie
- évaluation régulière contre des adversaires externes (Random, Negamax)


### ⏱️ Contraintes de temps de calcul

La recherche Negamax combinée au CNN est coûteuse :

- profondeur de recherche limitée
- nécessité d’optimiser l’ordre des coups
- compromis constant entre profondeur et temps d’inférence

➡️ Cela a conduit à l’utilisation de heuristiques simples pour réduire l’arbre


### 🐞 Débogage et intégration

Le projet a nécessité un débogage long et rigoureux :

- erreurs silencieuses dans la gestion des joueurs
- incohérences entre entraînement et inférence
- différences de comportement CPU / GPU
- gestion correcte des tenseurs et des dimensions

➡️ Chaque erreur avait un impact direct sur les performances finales.

### 📌 Enseignement clé

Le principal enseignement est que :

**La qualité du pipeline global est plus importante que la complexité du modèle.**


## 🎓 Compétences acquises

Ce projet a permis de développer et de consolider de nombreuses compétences, à la fois **techniques**, **algorithmiques** et **méthodologiques**, autour de l’intelligence artificielle appliquée aux jeux.

### 🧠 Compétences en intelligence artificielle

- Compréhension approfondie des **jeux déterministes à information parfaite**
- Mise en œuvre de **recherche adversariale** :
  - Minimax / Negamax
  - Élagage Alpha-Beta
- Intégration d’un **réseau de neurones de valeur** dans une recherche classique
- Différence entre :
  - policy network
  - value network


### 🤖 Apprentissage automatique & Deep Learning

- Conception d’un **CNN adapté à un problème spécifique**
- Encodage efficace d’un plateau de jeu en tenseur multi-canaux
- Gestion du **surapprentissage** et de la généralisation
- Analyse critique de la loss vs performance réelle
- Utilisation de PyTorch pour :
  - définition de modèles
  - entraînement
  - inférence


### 🔁 Self-play et pipelines d’apprentissage

- Mise en place d’un **apprentissage par self-play**
- Génération et gestion de datasets dynamiques
- Apprentissage par cycles :
  - jeu
  - entraînement
  - évaluation
- Ajout de **bruit contrôlé** pour favoriser l’exploration
- Sauvegarde conditionnelle du meilleur modèle


### ⚙️ Optimisation et performance

- Optimisation de la recherche par :
  - ordre des coups
  - heuristiques déterministes
  - profondeur dynamique
- Gestion du compromis :
  - profondeur de recherche
  - temps de calcul
- Compréhension des contraintes liées à l’inférence temps réel


### 🧪 Méthodologie et rigueur scientifique

- Comparaison systématique des approches
- Analyse des résultats sur plusieurs runs
- Interprétation critique des performances
- Prise de décision basée sur l’observation expérimentale


### 📌 Conclusion personnelle

Ce projet a montré que des solutions **hybrides**, combinant recherche algorithmique et apprentissage, peuvent être :

- plus performantes,
- plus robustes,
- et plus interprétables

qu’une approche de deep reinforcement learning seule sur des jeux déterministes.












