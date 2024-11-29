# Discord Task Reminder Bot

## Description
Ce bot Discord permet aux utilisateurs de créer, consulter et supprimer des rappels/tâches dans Discord via des commandes slash. Il prend en charge l'ajout de tâches avec ou sans heure définie et vous rappelle ces tâches en fonction de l'heure. Les utilisateurs peuvent également supprimer des tâches existantes.

## Fonctionnalités
- **Ajouter une tâche** : Permet à l'utilisateur d'ajouter une tâche avec une description et, si souhaité, une heure spécifique.
- **Voir les rappels** : Affiche la liste des rappels/tâches enregistrées pour l'utilisateur.
- **Supprimer une tâche** : Permet à l'utilisateur de supprimer une tâche en utilisant son ID.

## Prérequis
- Python 3.8 ou supérieur
- Un bot Discord configuré et invité sur ton serveur
- Une clé d'API Discord (TOKEN)
- La bibliothèque `discord.py` (version 2.x)
- La bibliothèque `dotenv` pour la gestion des variables d'environnement

## Installation

### 1. Clonez ce dépôt :
```bash
git clone https://github.com/votre-utilisateur/discord-task-reminder-bot.git

cd discord-task-reminder-bot
pip install -r requirements.txt

TOKEN=VOTRE_TOKEN_DISCORD
