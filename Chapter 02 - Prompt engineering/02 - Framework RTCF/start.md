# Atelier de Prompt Engineering — Framework RTCF

**Public :** débutants en intelligence artificielle  
**Contexte métier :** nouveaux conseillers du service client d'un opérateur télécom algérien  
**Objectif :** apprendre à structurer un prompt en utilisant le framework RTCF (Rôle, Tâche, Contexte, Format).

---

# Partie 1 — Exercices à résoudre

## Introduction — Le framework RTCF

Le framework RTCF est une méthode permettant de structurer un prompt en quatre éléments :

| Élément      | Signification                                           | Question à se poser             |
| ------------ | ------------------------------------------------------- | ------------------------------- |
| R — Rôle     | Définir le rôle ou l'expertise de l'IA.                 | Qui doit être l'IA ?            |
| T — Tâche    | Décrire précisément le travail demandé.                 | Que doit-elle faire ?           |
| C — Contexte | Fournir les informations sur la situation et le public. | Dans quelle situation ?         |
| F — Format   | Définir la structure de la réponse attendue.            | Comment présenter le résultat ? |

**Exemple simple :**

Prompt vague :

> Explique-moi comment fonctionne Internet.

Prompt structuré :

> **Rôle :** Tu es un formateur spécialisé dans les télécommunications.
>
> **Tâche :** Explique le fonctionnement d'Internet.
>
> **Contexte :** La réponse s'adresse à des personnes débutantes qui suivent une formation dans un centre d'appels d'un opérateur téléphonique en Algérie.
>
> **Format :** Présente une explication en trois parties, avec des exemples simples et une analogie facile à comprendre.

## Consignes générales

Pour chaque exercice :

1. Testez le prompt initial dans le modèle IA de votre choix.
2. Observez les limites de la réponse obtenue.
3. Réécrivez le prompt en utilisant le framework RTCF.
4. Testez votre nouvelle version.
5. Comparez les deux résultats.

**Important :** il n'existe pas une seule bonne formulation. Votre prompt doit simplement répondre clairement au besoin.

---

## Exercice 1 — Traiter une réclamation réseau

**Objectif :** apprendre à préciser le rôle, le public et la tâche.

**Situation :** un client appelle le centre de contact pour signaler qu'il n'a plus de réseau mobile.

**Prompt initial :**

> Comment résoudre un problème de réseau ?

**Votre travail :** améliorez ce prompt pour obtenir un guide destiné à un nouveau conseiller. La réponse doit lui permettre de comprendre comment accueillir la réclamation, poser les bonnes questions et accompagner le client sans avoir de connaissances techniques avancées.

---

## Exercice 2 — Expliquer une technologie

**Objectif :** adapter une explication technique au niveau du destinataire.

**Situation :** un nouveau conseiller doit comprendre la différence entre la 3G et la 4G afin de répondre aux questions des clients.

**Prompt initial :**

> Explique-moi la 3G et la 4G.

**Votre travail :** rédigez un prompt demandant une explication simple de ces deux technologies, adaptée à un conseiller débutant. Précisez les notions à expliquer et demandez des exemples concrets.

---

## Exercice 3 — Préparer un script téléphonique

**Objectif :** imposer une structure précise à la réponse.

**Situation :** un client appelle pour signaler une connexion Internet très lente. Le conseiller doit savoir comment conduire la conversation.

**Prompt initial :**

> Écris un script pour parler avec un client.

**Votre travail :** améliorez ce prompt pour obtenir un script téléphonique structuré en plusieurs étapes : accueil, identification du problème, questions de diagnostic, proposition d'assistance et conclusion.

---

## Exercice 4 — Gérer un client mécontent

**Objectif :** définir un rôle professionnel et un contexte précis.

**Situation :** un client est mécontent parce que sa connexion Internet ne fonctionne plus depuis plusieurs heures.

**Prompt initial :**

> Comment gérer un client énervé ?

**Votre travail :** construisez un prompt qui demande à l'IA d'adopter le rôle d'un formateur spécialisé en relation client. Demandez des techniques de communication et des exemples de phrases adaptées à un conseiller débutant.

---

## Exercice 5 — Créer une fiche de formation

**Objectif :** combiner les quatre éléments RTCF pour obtenir un support pédagogique complet.

**Situation :** vous êtes responsable de la formation des nouveaux conseillers du centre d'appels d'Oran. Vous devez préparer une fiche de formation sur le traitement des réclamations « pas de réseau / Internet lent ».

**Prompt initial :**

> Fais une fiche de formation pour le service client.

**Votre travail :** construisez un prompt complet en utilisant RTCF. La fiche doit être adaptée aux débutants et contenir des étapes de traitement, des définitions simples et des mises en situation.

---
