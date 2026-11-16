# Atelier de Prompt Engineering — Exercices

**Public :** débutants en intelligence artificielle  
**Contexte métier :** ingénieur NOC junior chez un opérateur télécom algérien  
**Objectif :** apprendre à améliorer un prompt en précisant le rôle, le contexte, la tâche, le format et les contraintes.

## Consignes générales

Pour chaque exercice :

1. Testez le prompt initial dans le modèle IA de votre choix.
2. Observez les limites de la réponse obtenue.
3. Réécrivez le prompt pour obtenir une réponse plus utile.
4. Testez votre nouvelle version.
5. Comparez les deux résultats.

**Important :** il n'existe pas une seule bonne formulation. Votre prompt doit simplement répondre clairement au besoin.

---

## Exercice 1 — Comprendre une technologie

**Objectif :** transformer une demande générale en demande adaptée à un public précis.

**Situation :** vous êtes un nouvel ingénieur NOC et vous devez comprendre la technologie 4G.

**Prompt initial :**

> Parle-moi de la 4G.

**Votre travail :** améliorez ce prompt pour obtenir une explication adaptée à un ingénieur NOC débutant. Précisez les notions à expliquer et la manière de présenter la réponse.

---

## Exercice 2 — Diagnostiquer un problème réseau

**Objectif :** ajouter du contexte et demander une méthode de diagnostic.

**Situation :** plusieurs utilisateurs signalent une perte de connexion Internet sur le réseau 4G depuis quelques minutes.

**Prompt initial :**

> Pourquoi Internet ne fonctionne pas ?

**Votre travail :** transformez cette demande en une consigne qui aide un ingénieur junior à organiser ses vérifications sans supposer immédiatement la cause de la panne.

---

## Exercice 3 — Obtenir une réponse dans un format précis

**Objectif :** apprendre à imposer une structure de sortie.

**Situation :** vous devez préparer une fiche de référence sur les alarmes rencontrées dans un centre de supervision réseau.

**Prompt initial :**

> Explique-moi les alarmes réseau.

**Votre travail :** demandez une réponse sous forme de tableau. Définissez les colonnes nécessaires pour qu'un débutant puisse comprendre une alarme et savoir quelle première vérification effectuer.

---

## Exercice 4 — Définir un rôle

**Objectif :** utiliser un rôle pour orienter le point de vue et le niveau d'explication du modèle.

**Situation :** vous devez comprendre le rôle d'une station de base 4G (eNodeB) dans le réseau mobile.

**Prompt initial :**

> Explique-moi une antenne 4G.

**Votre travail :** donnez au modèle un rôle professionnel adapté et demandez une explication destinée à un ingénieur NOC junior.

---

## Exercice 5 — Ajouter des contraintes

**Objectif :** contrôler la longueur, le niveau de langage et le contenu d'une réponse.

**Situation :** vous devez expliquer le DNS à un collègue qui débute.

**Prompt initial :**

> Explique-moi le DNS.

**Votre travail :** imposez une limite de mots, un langage simple et un exemple concret. La réponse doit être courte et facile à retenir.

---

## Exercice 6 — Apprendre à partir d'exemples (Few-Shot)

**Objectif :** fournir des exemples pour montrer au modèle le format et les critères attendus.

**Situation :** vous devez classer des incidents selon leur priorité. Votre équipe utilise trois niveaux : critique, moyenne et faible.

**Prompt initial :**

> Classe ces incidents par priorité.

**Votre travail :** écrivez un prompt contenant au moins trois exemples d'incidents déjà classés, puis demandez au modèle de classer un nouvel incident en suivant les mêmes critères.

**Nouvel incident à classer :**

> Plusieurs stations de base d'une même région sont indisponibles.

---

## Exercice 7 — Décomposer une tâche complexe

**Objectif :** diviser une demande complexe en étapes simples.

**Situation :** une panne électrique a provoqué l'indisponibilité d'une station de base 4G pendant 30 minutes. Vous devez préparer un rapport d'incident.

**Prompt initial :**

> Fais-moi un rapport sur une panne réseau.

**Votre travail :** décomposez la rédaction du rapport en plusieurs parties. Pensez notamment au résumé, à l'impact, aux actions effectuées et aux recommandations. Demandez au modèle de ne pas inventer les informations manquantes.

---

## Exercice 8 — Demander des précisions avant de répondre

**Objectif :** éviter les réponses basées sur des suppositions lorsque le contexte est incomplet.

**Situation :** un collègue vous signale une dégradation des performances réseau, mais ne fournit aucune autre information.

**Prompt initial :**

> Mon réseau est lent, trouve le problème.

**Votre travail :** demandez au modèle de poser des questions avant de proposer un diagnostic. Déterminez les informations essentielles à collecter.

---

## Exercice 9 — Adapter la réponse à son public

**Objectif :** adapter le vocabulaire et le niveau technique au destinataire.

**Situation :** vous devez expliquer le phénomène de perte de paquets (Packet Loss) à un nouvel arrivant au NOC.

**Prompt initial :**

> C'est quoi le Packet Loss ?

**Votre travail :** améliorez le prompt pour obtenir une explication pédagogique avec une définition, un exemple concret, les conséquences pour les utilisateurs et une méthode de détection.

---

## Exercice 10 — Transformer une information en procédure

**Objectif :** demander au modèle de produire une procédure claire et ordonnée.

**Situation :** un ingénieur junior doit vérifier une alarme de perte de connectivité sur un équipement réseau. Il ne connaît pas encore la procédure de son équipe.

**Prompt initial :**

> Comment vérifier une alarme réseau ?

**Votre travail :** demandez une procédure étape par étape. Faites préciser les contrôles à réaliser, les informations à noter et les conditions dans lesquelles il faut escalader l'incident. Le modèle ne doit pas inventer de commandes propres à un équipement non identifié.

---

## Exercice 11 — Résumer un compte rendu

**Objectif :** extraire les informations importantes d'un texte et les organiser.

**Situation :** vous recevez le compte rendu suivant après un incident :

> À 02 h 10, une alarme a signalé une perte de connectivité sur un équipement de transmission. L'équipe NOC a commencé les vérifications à 02 h 15. À 02 h 25, l'équipe terrain a été contactée. La connectivité a été rétablie à 02 h 50. La cause exacte reste à confirmer.

**Prompt initial :**

> Résume ce texte.

**Votre travail :** demandez un résumé professionnel qui distingue les faits confirmés, la chronologie, les actions réalisées et les informations encore inconnues.

---

## Exercice 12 — Vérifier les limites d'une réponse IA

**Objectif :** apprendre à demander une réponse prudente et à distinguer les faits des hypothèses.

**Situation :** vous observez une augmentation du taux d'échec d'établissement des connexions sur plusieurs cellules 4G. Vous ne disposez pas encore de données supplémentaires.

**Prompt initial :**

> Pourquoi le taux d'échec augmente ?

**Votre travail :** construisez un prompt qui demande des causes possibles, les données nécessaires pour les vérifier et les limites du diagnostic. Le modèle ne doit pas présenter une hypothèse comme une cause confirmée.

---

## Défi final — Construire un prompt complet

**Objectif :** combiner les techniques étudiées.

**Situation :** pendant un quart de nuit, vous recevez un signalement de dégradation de la qualité du réseau 4G dans une zone géographique. Vous devez préparer une première analyse pour votre responsable.

**Prompt initial :**

> Aide-moi avec ce problème 4G.

**Votre travail :** construisez un prompt complet intégrant :

- Un rôle précis.
- Le public cible.
- Le contexte de l'incident.
- Une tâche clairement définie.
- Un format de réponse.
- Des contraintes de longueur et de langage.
- Une demande de clarification si des informations manquent.
- Une distinction entre faits, hypothèses et recommandations.

**Livrable :** votre prompt final et la réponse obtenue après l'avoir testé.
