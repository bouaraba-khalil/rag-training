# Module 4 – Les sorties structurées et l'extraction d'informations en JSON

## Objectifs pédagogiques

À la fin de ce module, l'apprenant sera capable de :

- Demander à une IA de produire une réponse au format JSON.
- Définir un schéma précis avec des champs et des types de données.
- Éviter les informations inventées par le modèle.
- Gérer les informations absentes avec la valeur `null`.
- Obtenir une réponse exploitable directement par un programme.

# PARTIE 1 – COURS ET EXERCICES

## 1. Introduction aux sorties structurées

Une IA peut répondre à une question de plusieurs manières : sous forme de texte, de liste, de tableau ou de données structurées.

Cependant, lorsqu'on souhaite utiliser les réponses d'une IA dans une application, un logiciel ou une API, il est préférable d'imposer un format précis.

**Exemple :**

Prompt classique :

> Extrais les informations de cette offre d'emploi.

Réponse possible :

> L'offre concerne un poste d'Ingénieur Réseau Radio chez Ooredoo Algérie, situé à Alger. Le poste nécessite des compétences en LTE, Python et SQL.

Cette réponse est compréhensible pour un humain, mais difficile à exploiter automatiquement.

Réponse structurée :

```json
{
  "poste": "Ingénieur Réseau Radio",
  "entreprise": "Ooredoo Algérie",
  "ville": "Alger",
  "competences": ["LTE", "Python", "SQL"]
}
```

Cette deuxième réponse est plus facile à traiter par un programme.

## 2. Qu'est-ce que le JSON ?

JSON (_JavaScript Object Notation_) est un format standard permettant de représenter et d'échanger des données.

Il est composé de paires clé-valeur.

Exemple :

```json
{
  "nom": "Amine",
  "age": 25,
  "ville": "Oran",
  "competences": ["Python", "JavaScript"],
  "disponible": true
}
```

Les principaux types de données JSON sont :

| Type    | Exemple                    |
| ------- | -------------------------- |
| String  | `"Amine"`                  |
| Number  | `25`                       |
| Boolean | `true` ou `false`          |
| Array   | `["Python", "JavaScript"]` |
| Object  | `{"nom": "Amine"}`         |
| Null    | `null`                     |

**Attention :** `null`, `false` et `"null"` sont trois valeurs différentes.

## 3. Pourquoi imposer un schéma ?

Un schéma définit la structure exacte que la réponse doit respecter.

Exemple de schéma :

```json
{
  "nom": "string",
  "age": "number",
  "competences": "string[]",
  "disponible": "boolean"
}
```

Cela permet de préciser :

- Les noms exacts des champs.
- Le type de chaque valeur.
- Les informations obligatoires.
- La manière de représenter les informations absentes.

Sans schéma, le modèle peut choisir librement les noms des propriétés et les types de données.

## 4. Gérer les informations absentes

Une IA peut être tentée de compléter une information qui n'est pas présente dans le document.

Pour éviter cela, il faut lui donner une règle explicite.

Exemple :

> Si une information est absente du document, utilise `null`. N'invente aucune information.

Donnée source :

> Amine travaille comme développeur chez TechNova à Oran.

Résultat attendu :

```json
{
  "nom": "Amine",
  "poste": "Développeur",
  "entreprise": "TechNova",
  "ville": "Oran",
  "salaire": null
}
```

Le salaire n'est pas mentionné. Il ne doit donc pas être inventé.

## 5. Les règles pour obtenir un JSON strict

Pour obtenir une réponse exploitable par un programme, il est conseillé d'utiliser les règles suivantes dans son prompt :

1. Demander explicitement un JSON valide.
2. Définir les champs et leurs types.
3. Interdire le texte avant et après le JSON.
4. Préciser comment gérer les informations absentes.
5. Interdire toute invention ou déduction non autorisée.
6. Fournir les données sources clairement.

**Exemple de prompt amélioré :**

```text
Analyse le document fourni et extrais les informations demandées.

Réponds UNIQUEMENT avec un JSON valide.
N'ajoute aucun texte avant ou après le JSON.
Respecte exactement le schéma fourni.
Si une information est absente, utilise null.
N'invente aucune information.

Schéma :
{
  "nom": "string",
  "age": "number|null",
  "ville": "string|null"
}

Document :
[Insérer le document ici]
```

---

# 6. Exercices pratiques

**Consigne générale :** Pour chaque exercice, rédige un prompt permettant d'obtenir un JSON strict. Définis le schéma, les types de données et les règles à respecter. Les résultats devront être testés avec un modèle d'IA.

## Exercice 4.1 – Extraction d'une offre d'emploi en JSON strict

**1. Objectif**

Obtenir un JSON strict, valide et sans invention à partir d'une offre d'emploi.

**2. Données utilisées**

Offre d'emploi fictive :

Ooredoo Algérie recrute un(e) Ingénieur(e) Réseau Radio à Alger (CDI).

Missions : optimisation du réseau 4G, analyse des KPI radio, drive tests, traitement des réclamations de couverture.

Compétences : LTE, outils de planification radio, Python, SQL, notions de 5G.

Poste sur site, sans télétravail, avec déplacements dans les wilayas. Démarrage dès que possible.

**3. Travail demandé**

Extraire les informations suivantes :

- `poste`
- `entreprise`
- `ville`
- `salaire`
- `competences`
- `teletravail`

Contraintes :

- `competences` doit être un tableau de chaînes de caractères.
- `teletravail` doit être un booléen.
- `salaire` doit être `null` si absent.
- Aucun texte ne doit accompagner le JSON.

## Exercice 4.2 – Extraction des informations d'une facture

**1. Objectif**

Extraire les informations importantes d'une facture et les représenter dans un JSON structuré.

**2. Données utilisées**

Facture n° F-2026-014.

Date : 12/11/2026.

Fournisseur : Atlas Informatique.

Client : SARL El Amel.

Détails :

- 3 claviers à 2 500 DZD l'unité : 7 500 DZD.
- 2 souris à 1 200 DZD l'unité : 2 400 DZD.

Montant HT : 9 900 DZD.

TVA : 19 %, soit 1 881 DZD.

Montant TTC : 11 781 DZD.

**3. Travail demandé**

Extraire les informations suivantes :

- `numero_facture`
- `date`
- `fournisseur`
- `client`
- `lignes` : tableau contenant la description, la quantité, le prix unitaire et le total.
- `montant_ht`
- `tva`
- `montant_ttc`
- `devise`

Contraintes :

- Les montants doivent être des nombres.
- La quantité doit être un nombre entier.
- Les lignes de facture doivent être représentées dans un tableau d'objets.
- Ne pas inventer d'informations.

## Exercice 4.3 – Extraction des informations d'un CV

**1. Objectif**

Transformer le contenu d'un CV en données structurées afin de faciliter son traitement par une application de recrutement.

**2. Données utilisées**

CV fictif :

Nadia Benali, domiciliée à Oran.

Email : nadia.benali@example.com.

Développeuse backend chez TechNova de 2022 à 2025.

Compétences : Python, Django, PostgreSQL, Docker, Git et REST API.

Formation : Master en informatique, obtenu à l'Université d'Oran en 2021.

Langues : français courant et anglais intermédiaire.

**3. Travail demandé**

Extraire les informations suivantes :

- `nom`
- `email`
- `ville`
- `experience_annees`
- `competences`
- `diplomes`
- `langues`

Contraintes :

- `experience_annees` doit être un nombre.
- `competences` et `diplomes` doivent être des tableaux.
- `langues` doit être un tableau d'objets contenant le nom de la langue et le niveau.
- Ne pas ajouter de compétences qui ne figurent pas dans le CV.

## Exercice 4.4 – Classification d'un ticket de support client

**1. Objectif**

Utiliser l'IA pour analyser et catégoriser automatiquement les demandes reçues par un service client.

**2. Données utilisées**

Ticket reçu :

« Bonjour, depuis ce matin je n'arrive plus à me connecter à mon compte, même après avoir réinitialisé mon mot de passe. J'ai une présentation importante dans 30 minutes et j'ai besoin d'accéder à mes documents rapidement. Merci de m'aider. »

**3. Travail demandé**

Analyser le ticket et produire les informations suivantes :

- `categorie` : technique, facturation, compte ou autre.
- `priorite` : faible, moyenne ou élevée.
- `sentiment` : positif, neutre ou négatif.
- `resume`
- `action_recommandee`

Contraintes :

- Les catégories doivent respecter les valeurs autorisées.
- La priorité doit être définie selon l'urgence exprimée.
- Le résumé doit rester fidèle au message.
- Ne pas inventer de détails concernant le problème.

## Exercice 4.5 – Extraction des décisions d'une réunion

**1. Objectif**

Transformer le compte rendu d'une réunion en données structurées afin de faciliter le suivi des décisions et des tâches.

**2. Données utilisées**

Compte rendu de réunion :

Réunion du 14 novembre 2026 concernant le projet « Portail Client ».

Participants : Sarah, Yacine et Amine.

Décisions prises :

- Le lancement du portail est reporté au 25 novembre 2026.
- Le design doit être finalisé avant le lancement.
- Les tests de performance doivent être réalisés avant la mise en production.

Actions :

- Sarah doit finaliser le design pour le 18 novembre 2026.
- Yacine doit terminer le développement de l'API pour le 20 novembre 2026.
- Amine doit réaliser les tests de performance. Aucune échéance précise n'a été mentionnée.

**3. Travail demandé**

Extraire les informations suivantes :

- `titre_reunion`
- `date`
- `participants`
- `decisions`
- `actions` : tableau d'objets contenant la tâche, le responsable et l'échéance.

Contraintes :

- Les participants et les décisions doivent être des tableaux.
- Chaque action doit être un objet.
- Le responsable doit être `null` si non précisé.
- L'échéance doit être `null` si aucune date n'est mentionnée.
- Ne pas inventer de décisions ou de tâches.

---
