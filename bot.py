import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
import json
from datetime import datetime
import asyncio

# Charger les variables d'environnement
load_dotenv()

# Configurer les intents nécessaires
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Configurer le bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Charger les rappels depuis un fichier JSON
try:
    with open("rappels.json", "r") as file:
        rappels_data = json.load(file)
except FileNotFoundError:
    rappels_data = {}

# Déclarer une commande slash
@bot.event
async def on_ready():
    print(f'{bot.user} is connected to Discord!')
    # Sync des commandes slash
    await bot.tree.sync()

# Commande slash pour ajouter une tâche
@bot.tree.command(name="ajouter_tache", description="Ajouter une nouvelle tâche.")
@app_commands.describe(description="La description de la tâche")

async def ajouter_tache(interaction: discord.Interaction, description: str):
    # Demander si l'utilisateur veut ajouter une heure
    await interaction.response.send_message("⏰ Voulez-vous ajouter une heure à cette tâche ? (oui/non)")

    def check(msg):
        return msg.author == interaction.user and msg.channel == interaction.channel

    try:
        hour_response = await bot.wait_for('message', check=check, timeout=60)
        hour_response = hour_response.content.strip().lower()
        
        if hour_response == 'oui':
            await interaction.followup.send("Veuillez entrer la date et l'heure au format `DD-MM-YYYY HH:MM`.")
            date_msg = await bot.wait_for('message', check=check, timeout=60)
            try:
                rappel_time = datetime.strptime(date_msg.content.strip(), "%d-%m-%Y %H:%M")
            except ValueError:
                await interaction.followup.send("❌ Format de date invalide. Utilisez : `DD-MM-YYYY HH:MM`.")
                return
        else:
            rappel_time = None
    except asyncio.TimeoutError:
        await interaction.followup.send("❌ Temps écoulé, aucune réponse reçue.")
        return

    # Ajouter la tâche dans les données
    user_id = str(interaction.user.id)
    if user_id not in rappels_data:
        rappels_data[user_id] = []

    task_id = len(rappels_data[user_id]) + 1
    task_data = {
        "id": task_id,
        "description": description,
        "status": "en attente"
    }
    if rappel_time:
        task_data["rappel_time"] = rappel_time.strftime("%Y-%m-%d %H:%M")

    rappels_data[user_id].append(task_data)

    # Sauvegarder les données
    with open("rappels.json", "w") as file:
        json.dump(rappels_data, file, indent=4)

    # Confirmation de la tâche ajoutée
    if rappel_time:
        await interaction.followup.send(f"✅ Tâche ajoutée : `{description}` pour le {rappel_time.strftime('%d-%m-%Y %H:%M')}.")
    else:
        await interaction.followup.send(f"✅ Tâche ajoutée : `{description}` sans heure définie.")

    # Envoi d'un message privé de confirmation
    try:
        # Envoie un message privé de confirmation
        await interaction.user.send(f"✅ Tâche ajoutée avec succès : `{description}`. {f'Rappel fixé pour {rappel_time.strftime('%d-%m-%Y %H:%M')}' if rappel_time else 'Pas de rappel défini.'}")
    except discord.Forbidden:
        # Si l'utilisateur a désactivé les DMs, informer dans le chat public
        await interaction.response.send_message("❌ Je ne peux pas envoyer de message privé à cet utilisateur.")

# Commande slash pour voir les rappels
@bot.tree.command(name="voir_rappels", description="Voir les rappels en attente.")
async def voir_rappels(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    if user_id in rappels_data and rappels_data[user_id]:
        rappels_list = rappels_data[user_id]
        message = "📅 Vos rappels :\n"
        for rappel in rappels_list:
            message += f"ID: {rappel['id']} | Description: {rappel['description']} | Statut: {rappel['status']}\n"
            if 'rappel_time' in rappel:
                message += f"   Heure : {rappel['rappel_time']}\n"
        await interaction.response.send_message(message)
    else:
        await interaction.response.send_message("❌ Vous n'avez aucun rappel enregistré.")

# Commande slash pour supprimer une tâche
@bot.tree.command(name="supprimer_tache", description="Supprimer une tâche spécifique.")
@app_commands.describe(task_id="L'ID de la tâche à supprimer")

async def supprimer_tache(interaction: discord.Interaction, task_id: int):
    user_id = str(interaction.user.id)
    if user_id in rappels_data and rappels_data[user_id]:
        task_to_delete = next((task for task in rappels_data[user_id] if task["id"] == task_id), None)
        if task_to_delete:
            rappels_data[user_id].remove(task_to_delete)
            # Sauvegarder après suppression
            with open("rappels.json", "w") as file:
                json.dump(rappels_data, file, indent=4)
            await interaction.response.send_message(f"Tâche {task_id} supprimée avec succès.")
        else:
            await interaction.response.send_message(f"❌ Aucune tâche trouvée avec l'ID {task_id}.")
    else:
        await interaction.response.send_message("❌ Vous n'avez aucun rappel enregistré.")

# Lancer le bot
bot.run(os.getenv("TOKEN"))
