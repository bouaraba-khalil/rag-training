# Atelier de Prompt Engineering — Corrigé

**Public :** débutants en intelligence artificielle  
**Contexte métier :** ingénieur NOC junior chez un opérateur télécom algérien

> Les propositions ci-dessous sont des exemples de bonnes formulations, et non des réponses uniques. Les résultats générés peuvent varier selon le modèle utilisé. Dans un contexte opérationnel, les procédures et consignes de l'opérateur restent prioritaires.

---

## Exercice 1 — Comprendre une technologie

**Technique :** prompt structuré (rôle + public + tâche + format + contraintes).

**Prompt amélioré :**

```text
Tu es un ingénieur télécom senior spécialisé dans les réseaux mobiles.

Explique à un ingénieur NOC junior le fonctionnement de la 4G LTE.

Présente les notions suivantes :
1. Le principe général de la 4G.
2. Le rôle de la station de base (eNodeB).
3. Le rôle du cœur de réseau (EPC).
4. Le chemin parcouru par les données entre le téléphone et Internet.
5. Les principaux éléments qu'un ingénieur NOC doit surveiller.

Utilise un langage simple, donne des exemples concrets et limite
ta réponse à 400 mots.
```

**Résultat attendu :**

Une explication structurée de l'architecture 4G, du rôle de ses principaux composants et des éléments à surveiller en supervision.

**Pourquoi c'est mieux :** le modèle connaît le public, le périmètre du sujet et les attentes de la réponse.

---

## Exercice 2 — Diagnostiquer un problème réseau

**Technique :** contextualisation + demande de démarche structurée.

**Prompt amélioré :**

```text
Tu es un ingénieur réseau senior dans un opérateur télécom.

Plusieurs utilisateurs signalent une perte de connexion Internet
sur le réseau 4G depuis quelques minutes.

Propose une méthode de diagnostic destinée à un ingénieur NOC junior.

Présente les vérifications dans un tableau avec :
- Étape
- Élément à contrôler
- Information à collecter
- Résultat possible
- Prochaine action

Commence par les vérifications générales et ne suppose pas
une cause avant d'avoir des éléments pour la confirmer.

Ne propose pas de commande spécifique à un équipement
dont le modèle n'est pas connu.
```

**Résultat attendu :**

Une démarche progressive : vérifier l'étendue de l'incident, les alarmes, l'état des équipements et les indicateurs disponibles, puis orienter l'investigation selon les observations.

**Pourquoi c'est mieux :** le prompt fournit les symptômes et demande une méthode plutôt qu'une réponse spéculative.

---

## Exercice 3 — Obtenir une réponse dans un format précis

**Technique :** format prompting.

**Prompt amélioré :**

```text
Tu es un formateur spécialisé dans la supervision réseau.

Présente 5 exemples d'alarmes courantes qu'un ingénieur NOC
peut rencontrer.

Utilise un tableau avec les colonnes suivantes :
- Nom de l'alarme
- Signification
- Gravité indicative
- Impact potentiel
- Première vérification

Explique les termes techniques simplement.
Précise que la gravité réelle dépend des règles de l'opérateur.
```

**Résultat attendu :**

| Alarme        | Signification                                 | Première vérification                                  |
| ------------- | --------------------------------------------- | ------------------------------------------------------ |
| Link Down     | Une liaison est indisponible                  | Vérifier l'état de la liaison et les alarmes associées |
| High CPU      | Utilisation élevée du processeur              | Examiner l'évolution de la charge                      |
| High Memory   | Utilisation élevée de la mémoire              | Vérifier les tendances et les alertes                  |
| Packet Loss   | Des paquets n'atteignent pas leur destination | Vérifier les mesures de perte et le périmètre          |
| Power Failure | Une anomalie d'alimentation est signalée      | Vérifier les alarmes électriques associées             |

**Pourquoi c'est mieux :** la structure est définie à l'avance et facilite la lecture et la comparaison.

---

## Exercice 4 — Définir un rôle

**Technique :** Role Prompting.

**Prompt amélioré :**

```text
Agis comme un ingénieur radio senior spécialisé dans les réseaux LTE.

Explique à un ingénieur NOC débutant le rôle d'une station
de base 4G (eNodeB).

Présente :
1. Son rôle dans le réseau.
2. Les principaux équipements et fonctions associés.
3. Sa communication avec le cœur de réseau.
4. Les problèmes courants qui peuvent être visibles en supervision.

Utilise des analogies simples et des exemples concrets.
Évite les détails trop avancés.
```

**Résultat attendu :**

Le modèle explique que l'eNodeB assure notamment la communication radio avec les terminaux et leur connexion au réseau LTE. Il présente ses interactions avec le cœur de réseau et quelques exemples d'événements visibles en supervision.

**Pourquoi c'est mieux :** le rôle oriente le niveau d'expertise et l'angle de la réponse.

---

## Exercice 5 — Ajouter des contraintes

**Technique :** Constraint Prompting.

**Prompt amélioré :**

```text
Explique le fonctionnement du DNS à un ingénieur NOC débutant.

Contraintes :
- Maximum 100 mots.
- Utilise un vocabulaire simple.
- Donne un seul exemple concret.
- Évite les détails avancés.
- Termine par une phrase résumant son importance dans un réseau.
```

**Résultat attendu — exemple :**

Le DNS (Domain Name System) permet de traduire un nom de domaine, comme `example.com`, en adresse IP que les machines utilisent pour communiquer. Lorsqu'un utilisateur ouvre un site, son appareil interroge généralement un serveur DNS pour obtenir l'adresse correspondante. Si le DNS rencontre un problème, un site peut devenir inaccessible par son nom, même si la connectivité IP fonctionne.

**Pourquoi c'est mieux :** les contraintes limitent la longueur et évitent de surcharger le débutant.

---

## Exercice 6 — Apprendre à partir d'exemples (Few-Shot)

**Technique :** Few-Shot Prompting.

**Prompt amélioré :**

```text
Tu es un assistant qui aide à classer les incidents d'un NOC.

Voici des exemples de classification :

Incident : Une cellule 4G est totalement indisponible.
Priorité : Critique.

Incident : Un équipement présente une utilisation CPU élevée,
sans impact de service confirmé.
Priorité : Moyenne.

Incident : Une légère hausse de latence est observée,
sans dégradation notable du service.
Priorité : Faible.

Classe maintenant cet incident :

Incident : Plusieurs stations de base d'une même région
sont indisponibles.

Utilise le même format et explique brièvement ton choix.
Si des informations importantes manquent, indique-le.

Attention : cette classification est illustrative.
La priorité réelle doit suivre la matrice d'incident
de l'opérateur.
```

**Résultat attendu :**

Priorité proposée : Critique.

Explication : l'indisponibilité de plusieurs stations de base peut affecter un grand nombre d'utilisateurs et nécessite une évaluation rapide de l'impact.

**Pourquoi c'est mieux :** les exemples montrent au modèle le format et les critères de classification souhaités.

---

## Exercice 7 — Décomposer une tâche complexe

**Technique :** Task Decomposition.

**Prompt amélioré :**

```text
Tu es un ingénieur NOC expérimenté chargé de rédiger
des comptes rendus d'incidents.

Prépare un rapport à partir des informations suivantes :

Une panne électrique a provoqué l'indisponibilité
d'une station de base 4G pendant 30 minutes.

Organise le rapport en 4 parties :
1. Résumé de l'incident.
2. Impact potentiel sur le service.
3. Actions effectuées et résolution.
4. Recommandations et suivi.

Pour chaque partie, utilise uniquement les informations fournies.
Ne présente pas une cause supposée comme un fait confirmé.
Indique clairement les informations manquantes.
Adopte un ton professionnel et concis.
```

**Résultat attendu :**

Un rapport organisé en quatre parties. Il doit signaler que la panne électrique est la cause indiquée dans le scénario, mais ne doit pas inventer le nombre d'utilisateurs affectés, les équipements concernés au-delà de la station mentionnée ou les actions réellement effectuées.

**Pourquoi c'est mieux :** la décomposition donne un plan au modèle et réduit les risques d'oubli.

---

## Exercice 8 — Demander des précisions avant de répondre

**Technique :** Clarification Prompting.

**Prompt amélioré :**

```text
Tu es un ingénieur réseau senior spécialisé dans le diagnostic NOC.

Je constate une dégradation des performances du réseau,
mais je ne dispose pas encore de suffisamment d'informations.

Avant de proposer un diagnostic, pose-moi les 5 questions
les plus importantes pour comprendre la situation.

Tes questions doivent couvrir :
- La zone géographique concernée.
- Le type de réseau concerné.
- Les symptômes observés.
- Les KPI affectés.
- L'heure de début de l'incident.

Pose une question à la fois.
Ne propose aucune cause avant d'avoir recueilli les informations.
```

**Résultat attendu :**

Le modèle commence par demander où se produit la dégradation, quel service est concerné, quels symptômes sont visibles, quels KPI évoluent et depuis quand.

**Pourquoi c'est mieux :** le modèle collecte le contexte nécessaire avant de produire des hypothèses.

---

## Exercice 9 — Adapter la réponse à son public

**Technique :** Audience Adaptation.

**Prompt amélioré :**

```text
Explique le concept de Packet Loss à un ingénieur NOC junior.

Structure ta réponse ainsi :
1. Définition simple.
2. Exemple concret dans un réseau 4G.
3. Conséquences possibles pour les utilisateurs.
4. Comment le détecter pendant la supervision.

Évite les formules mathématiques et le jargon avancé.
Maximum 150 mots.
```

**Résultat attendu :**

Une explication accessible : la perte de paquets correspond à des données envoyées qui n'arrivent pas à destination. Elle peut provoquer des interruptions, une mauvaise qualité d'appel ou des ralentissements. Un ingénieur NOC peut la repérer à l'aide des mesures de supervision et comparer les résultats selon les équipements et les périodes.

**Pourquoi c'est mieux :** la réponse est adaptée au niveau et aux besoins du destinataire.

---

## Exercice 10 — Transformer une information en procédure

**Technique :** Step-by-Step Prompting + contraintes de sécurité.

**Prompt amélioré :**

```text
Tu es un formateur NOC expérimenté.

Un ingénieur junior reçoit une alarme de perte de connectivité
sur un équipement réseau.

Rédige une procédure générale de première analyse.

Présente les étapes dans l'ordre :
1. Confirmer l'alarme.
2. Identifier l'équipement et le service concernés.
3. Vérifier les alarmes associées.
4. Consulter les mesures et événements disponibles.
5. Documenter les observations.
6. Escalader selon les procédures internes si nécessaire.

Pour chaque étape, indique ce qu'il faut vérifier
et ce qu'il faut noter.

N'invente aucune commande ou procédure constructeur.
Précise que les actions opérationnelles doivent respecter
les consignes de l'opérateur.
```

**Résultat attendu :**

Une procédure générale, ordonnée et prudente qui explique les contrôles, les informations à documenter et les conditions d'escalade.

**Pourquoi c'est mieux :** le prompt transforme une question vague en procédure exploitable, tout en évitant les instructions techniques non vérifiées.

---

## Exercice 11 — Résumer un compte rendu

**Technique :** Information Extraction + Structured Output.

**Prompt amélioré :**

```text
Tu es un assistant chargé de préparer les comptes rendus
d'incidents d'un centre NOC.

Analyse le texte suivant :

« À 02 h 10, une alarme a signalé une perte de connectivité
sur un équipement de transmission. L'équipe NOC a commencé
les vérifications à 02 h 15. À 02 h 25, l'équipe terrain
a été contactée. La connectivité a été rétablie à 02 h 50.
La cause exacte reste à confirmer. »

Produis les sections suivantes :
- Résumé de l'incident.
- Chronologie.
- Actions réalisées.
- État actuel.
- Informations encore inconnues.

N'ajoute aucun fait absent du texte.
Utilise un ton professionnel et concis.
```

**Résultat attendu :**

### Résumé

Une perte de connectivité a été signalée sur un équipement de transmission à 02 h 10. Le service a été rétabli à 02 h 50.

### Chronologie

- 02 h 10 : alarme signalée.
- 02 h 15 : début des vérifications NOC.
- 02 h 25 : contact de l'équipe terrain.
- 02 h 50 : rétablissement de la connectivité.

### Informations inconnues

La cause exacte de l'incident reste à confirmer.

**Pourquoi c'est mieux :** le modèle extrait les informations importantes sans ajouter de détails non fournis.

---

## Exercice 12 — Vérifier les limites d'une réponse IA

**Technique :** Evidence-Based Prompting + distinction faits / hypothèses.

**Prompt amélioré :**

```text
Tu es un ingénieur réseau senior spécialisé dans les réseaux LTE.

Situation :
Une augmentation du taux d'échec d'établissement
des connexions est observée sur plusieurs cellules 4G.

Aucune autre donnée n'est disponible pour le moment.

Présente :
1. Les causes possibles, sous forme d'hypothèses.
2. Les données à collecter pour vérifier chaque hypothèse.
3. Les vérifications générales à envisager.
4. Les informations qui manquent pour conclure.

Sépare clairement les faits des hypothèses.
Ne désigne aucune cause comme confirmée sans preuve.
Ne propose pas d'action corrective risquée sans validation.
```

**Résultat attendu :**

Le modèle présente plusieurs pistes possibles et précise les indicateurs ou informations nécessaires pour les examiner. Il indique qu'il est impossible de déterminer la cause exacte avec les seules informations disponibles.

**Pourquoi c'est mieux :** le prompt encourage une réponse prudente et évite de confondre une possibilité avec un diagnostic confirmé.

---

## Défi final — Construire un prompt complet

**Technique :** combinaison des techniques étudiées.

**Prompt amélioré — Exemple de solution :**

```text
RÔLE
Tu es un ingénieur NOC senior spécialisé dans les réseaux mobiles LTE.

PUBLIC
Ta réponse s'adresse à un ingénieur NOC junior qui débute
chez un opérateur télécom algérien.

CONTEXTE
Pendant un quart de nuit, un signalement indique une dégradation
de la qualité du réseau 4G dans une zone géographique.
Les détails de l'incident ne sont pas encore disponibles.

TÂCHE
Aide-moi à préparer une première analyse de l'incident.

Commence par identifier les informations manquantes.
Pose jusqu'à 5 questions prioritaires avant de proposer
des hypothèses.

FORMAT
Présente ensuite ton analyse sous forme de sections :
1. Résumé de la situation.
2. Informations confirmées.
3. Hypothèses possibles.
4. Vérifications à effectuer.
5. Informations à transmettre au responsable.

CONTRAINTES
- Utilise un langage simple et professionnel.
- Maximum 400 mots après réception des informations.
- Ne présente jamais une hypothèse comme un fait.
- N'invente aucune mesure ou donnée.
- Ne propose pas de commande propre à un équipement
  dont le modèle n'est pas connu.
- Rappelle que les procédures internes de l'opérateur
  doivent être respectées.
```

**Résultat attendu :**

Un prompt complet qui guide le modèle dans une première analyse, commence par collecter les informations manquantes et distingue les faits, les hypothèses et les vérifications proposées.

**Pourquoi c'est mieux :** cet exercice combine les principaux éléments d'un prompt efficace au lieu de travailler une seule technique à la fois.

---

# Synthèse — Les techniques apprises

| Technique                | Utilité                                    |
| ------------------------ | ------------------------------------------ |
| Prompt structuré         | Organiser une demande complète             |
| Context Prompting        | Donner les informations de situation       |
| Format Prompting         | Définir la forme de la réponse             |
| Role Prompting           | Orienter le point de vue du modèle         |
| Constraint Prompting     | Contrôler la longueur et le niveau         |
| Few-Shot Prompting       | Montrer des exemples de résultats attendus |
| Task Decomposition       | Diviser une tâche complexe                 |
| Clarification Prompting  | Faire préciser les informations manquantes |
| Audience Adaptation      | Adapter la réponse au destinataire         |
| Step-by-Step Prompting   | Organiser une procédure                    |
| Information Extraction   | Extraire des données d'un texte            |
| Evidence-Based Prompting | Distinguer faits et hypothèses             |

## Règle à retenir

Un bon prompt répond généralement à ces questions :

1. **Qui ?** Quel rôle doit jouer le modèle ?
2. **Pour qui ?** À quel public s'adresse la réponse ?
3. **Pourquoi ?** Quel est le contexte ?
4. **Quoi ?** Quelle tâche doit être réalisée ?
5. **Comment ?** Quel format est attendu ?
6. **Quelles limites ?** Quelles contraintes faut-il respecter ?

Plus la demande est claire et pertinente, plus le modèle a de chances de produire une réponse utile. Cela ne garantit toutefois pas que les informations générées soient exactes : elles doivent être vérifiées.
