**Technique utilisée :** Sortie structurée (JSON + schéma) et règle « null si absent, n'invente rien ».

**Prompt amélioré :**

```text
Extrais les informations de l'offre ci-dessous.

Réponds UNIQUEMENT avec un JSON valide, sans texte autour.
Respecte exactement le schéma fourni.
Si une information est absente, mets null.
N'invente rien.

Schéma :
{
  "poste": "string",
  "entreprise": "string",
  "ville": "string",
  "salaire": "string|null",
  "competences": "string[]",
  "teletravail": "boolean"
}

Offre :
Ooredoo Algérie recrute un(e) Ingénieur(e) Réseau Radio à Alger (CDI).

Missions : optimisation du réseau 4G, analyse des KPI radio,
drive tests, traitement des réclamations de couverture.

Compétences : LTE, outils de planification radio,
Python, SQL, notions de 5G.

Poste sur site, sans télétravail, avec déplacements dans les wilayas.
Démarrage dès que possible.
```

**Résultat attendu :**

```json
{
  "poste": "Ingénieur(e) Réseau Radio",
  "entreprise": "Ooredoo Algérie",
  "ville": "Alger",
  "salaire": null,
  "competences": [
    "LTE",
    "outils de planification radio",
    "Python",
    "SQL",
    "5G"
  ],
  "teletravail": false
}
```

**Analyse :**

Le salaire est absent de l'offre, donc sa valeur est `null`. Le poste étant explicitement indiqué comme étant sur site, le télétravail est représenté par `false`.

## Solution 4.2 – Extraction d'une facture

**Technique utilisée :** Extraction structurée avec types de données précis et tableau d'objets.

**Prompt amélioré :**

```text
Extrais les informations de cette facture.

Réponds UNIQUEMENT avec un JSON valide.
N'ajoute aucun texte autour.
Respecte exactement le schéma.
N'invente aucune information.

Schéma :
{
  "numero_facture": "string",
  "date": "string",
  "fournisseur": "string",
  "client": "string",
  "lignes": [
    {
      "description": "string",
      "quantite": "number",
      "prix_unitaire": "number",
      "total": "number"
    }
  ],
  "montant_ht": "number",
  "tva": "number",
  "montant_ttc": "number",
  "devise": "string"
}

Facture :
F-2026-014, datée du 12/11/2026.
Fournisseur : Atlas Informatique.
Client : SARL El Amel.

3 claviers à 2 500 DZD l'unité : 7 500 DZD.
2 souris à 1 200 DZD l'unité : 2 400 DZD.

Montant HT : 9 900 DZD.
TVA : 19 %, soit 1 881 DZD.
Montant TTC : 11 781 DZD.
```

**Résultat attendu :**

```json
{
  "numero_facture": "F-2026-014",
  "date": "12/11/2026",
  "fournisseur": "Atlas Informatique",
  "client": "SARL El Amel",
  "lignes": [
    {
      "description": "Claviers",
      "quantite": 3,
      "prix_unitaire": 2500,
      "total": 7500
    },
    {
      "description": "Souris",
      "quantite": 2,
      "prix_unitaire": 1200,
      "total": 2400
    }
  ],
  "montant_ht": 9900,
  "tva": 1881,
  "montant_ttc": 11781,
  "devise": "DZD"
}
```

**Analyse :**

Les informations de la facture sont représentées avec des types cohérents. Les lignes sont placées dans un tableau d'objets, ce qui facilite leur traitement dans une application de gestion.

## Solution 4.3 – Extraction d'un CV

**Technique utilisée :** Extraction d'informations avec séparation des tableaux et normalisation des données.

**Prompt amélioré :**

```text
Analyse le CV ci-dessous et extrais les informations demandées.

Réponds UNIQUEMENT avec un JSON valide.
Respecte exactement le schéma.
N'invente aucune compétence ni information.
Utilise null pour toute information absente.

Schéma :
{
  "nom": "string",
  "email": "string",
  "ville": "string",
  "experience_annees": "number|null",
  "competences": "string[]",
  "diplomes": "string[]",
  "langues": [
    {
      "langue": "string",
      "niveau": "string"
    }
  ]
}

CV :
Nadia Benali, domiciliée à Oran.
Email : nadia.benali@example.com.
Développeuse backend chez TechNova de 2022 à 2025.
Compétences : Python, Django, PostgreSQL, Docker, Git et REST API.
Formation : Master en informatique, obtenu à l'Université d'Oran en 2021.
Langues : français courant et anglais intermédiaire.
```

**Résultat attendu :**

```json
{
  "nom": "Nadia Benali",
  "email": "nadia.benali@example.com",
  "ville": "Oran",
  "experience_annees": 3,
  "competences": [
    "Python",
    "Django",
    "PostgreSQL",
    "Docker",
    "Git",
    "REST API"
  ],
  "diplomes": ["Master en informatique - Université d'Oran (2021)"],
  "langues": [
    {
      "langue": "Français",
      "niveau": "Courant"
    },
    {
      "langue": "Anglais",
      "niveau": "Intermédiaire"
    }
  ]
}
```

**Analyse :**

Les compétences, les diplômes et les langues sont séparés dans des tableaux. L'expérience est exprimée en nombre d'années à partir de la période de travail indiquée, soit trois ans entre 2022 et 2025.

## Solution 4.4 – Classification d'un ticket de support

**Technique utilisée :** Classification avec valeurs autorisées (énumération) et sortie structurée.

**Prompt amélioré :**

```text
Analyse le ticket de support suivant.

Réponds UNIQUEMENT avec un JSON valide.
N'ajoute aucun texte autour.
N'invente aucune information.

Utilise uniquement les valeurs suivantes :
categorie : technique, facturation, compte, autre.
priorite : faible, moyenne, élevée.
sentiment : positif, neutre, négatif.

Schéma :
{
  "categorie": "string",
  "priorite": "string",
  "sentiment": "string",
  "resume": "string",
  "action_recommandee": "string"
}

Ticket :
Bonjour, depuis ce matin je n'arrive plus à me connecter
à mon compte, même après avoir réinitialisé mon mot de passe.
J'ai une présentation importante dans 30 minutes et j'ai besoin
d'accéder à mes documents rapidement. Merci de m'aider.
```

**Résultat attendu :**

```json
{
  "categorie": "compte",
  "priorite": "élevée",
  "sentiment": "négatif",
  "resume": "Le client ne parvient pas à accéder à son compte malgré la réinitialisation de son mot de passe. Il a besoin d'un accès rapide à ses documents.",
  "action_recommandee": "Vérifier le problème de connexion et orienter le client vers le support technique pour rétablir rapidement l'accès à son compte."
}
```

**Analyse :**

Le modèle doit classer le ticket dans une catégorie autorisée. La priorité est élevée car le client mentionne une présentation dans 30 minutes.

## Solution 4.5 – Extraction des décisions d'une réunion

**Technique utilisée :** Extraction structurée, tableaux d'objets et gestion des informations absentes.

**Prompt amélioré :**

```text
Analyse le compte rendu de réunion suivant.

Extrais les informations demandées.
Réponds UNIQUEMENT avec un JSON valide.
Respecte exactement le schéma.
N'invente aucune décision, tâche ou échéance.
Utilise null lorsqu'une information est absente.

Schéma :
{
  "titre_reunion": "string",
  "date": "string",
  "participants": "string[]",
  "decisions": "string[]",
  "actions": [
    {
      "tache": "string",
      "responsable": "string|null",
      "echeance": "string|null"
    }
  ]
}

Compte rendu :
Réunion du 14 novembre 2026 concernant le projet « Portail Client ».

Participants : Sarah, Yacine et Amine.

Décisions :
- Le lancement du portail est reporté au 25 novembre 2026.
- Le design doit être finalisé avant le lancement.
- Les tests de performance doivent être réalisés avant la mise en production.

Actions :
- Sarah doit finaliser le design pour le 18 novembre 2026.
- Yacine doit terminer le développement de l'API pour le 20 novembre 2026.
- Amine doit réaliser les tests de performance. Aucune échéance précise n'a été mentionnée.
```

**Résultat attendu :**

```json
{
  "titre_reunion": "Projet Portail Client",
  "date": "14/11/2026",
  "participants": ["Sarah", "Yacine", "Amine"],
  "decisions": [
    "Le lancement du portail est reporté au 25 novembre 2026.",
    "Le design doit être finalisé avant le lancement.",
    "Les tests de performance doivent être réalisés avant la mise en production."
  ],
  "actions": [
    {
      "tache": "Finaliser le design",
      "responsable": "Sarah",
      "echeance": "18/11/2026"
    },
    {
      "tache": "Terminer le développement de l'API",
      "responsable": "Yacine",
      "echeance": "20/11/2026"
    },
    {
      "tache": "Réaliser les tests de performance",
      "responsable": "Amine",
      "echeance": null
    }
  ]
}
```

**Analyse :**

Les décisions et les actions sont séparées pour faciliter leur exploitation. L'échéance d'Amine est `null`, car aucune date précise n'a été indiquée.

---

## Conclusion générale du module

Les sorties structurées permettent de transformer les réponses d'une IA en données directement exploitables par des applications.

Les points essentiels à retenir :

1. Toujours définir le format de sortie attendu.
2. Imposer un schéma précis et des types de données.
3. Demander un JSON valide, sans texte supplémentaire.
4. Utiliser `null` pour les informations absentes.
5. Interdire explicitement les inventions.
6. Tester et vérifier les résultats produits par le modèle.

**À retenir :** Un bon prompt ne sert pas uniquement à obtenir une réponse pertinente. Il sert également à obtenir une réponse dans le format exact dont on a besoin.
