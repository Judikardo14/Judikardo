import os
from threading import Thread
# Correction des importations pour python-telegram-bot
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters
from telegram._update import Update
from telegram._message import Message
import google.generativeai as genai


# Configuration des clés API
TELEGRAM_TOKEN =  "7939560231:AAFLiELtAiCucV6hP0n8uwUsQ6Opdwnvrhk"
GOOGLE_API_KEY = "AIzaSyDzDzivynuJ5vS8fyIYn7MW7mFXhzAVGX8"
 
# Configuration de Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gestionnaire de la commande /start"""
    welcome_message = """
    👋 Bonjour! Je suis un bot alimenté par Gemini et développé par Judikardo.
    Vous pouvez me poser des questions ou discuter avec moi sur n'importe quel sujet.
    Je ferai de mon mieux pour vous aider!
    """
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gestionnaire de la commande /help"""
    help_text = """
    🤖 Voici comment m'utiliser :
    - Envoyez-moi simplement un message et j'y répondrai
    - Utilisez /start pour recommencer
    - Utilisez /help pour voir cette aide
    """
    await update.message.reply_text(help_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gestionnaire pour tous les messages texte"""
    try:
        # Obtenir le message de l'utilisateur
        user_message = update.message.text
        
        # Indiquer que le bot est en train d'écrire
        await update.message.chat.send_action(action="typing")
        
        # Générer la réponse avec Gemini
        response = model.generate_content(user_message)
        
        # Envoyer la réponse
        if response.text:
            # Diviser le message si trop long
            if len(response.text) > 4096:
                chunks = [response.text[i:i+4096] for i in range(0, len(response.text), 4096)]
                for chunk in chunks:
                    await update.message.reply_text(chunk)
            else:
                await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("Désolé, je n'ai pas pu générer une réponse appropriée.")
            
    except Exception as e:
        print(f"Erreur: {str(e)}")
        await update.message.reply_text(
            "Désolé, une erreur s'est produite lors du traitement de votre message. "
            "Veuillez réessayer plus tard."
        )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gestionnaire d'erreurs global"""
    print(f'Erreur: {context.error}')
    await update.message.reply_text(
        "Une erreur s'est produite. Veuillez réessayer plus tard."
    )

def main():
    """Fonction principale"""
    
    
    # Créer l'application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Ajouter les gestionnaires
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Ajouter le gestionnaire d'erreurs
    application.add_error_handler(error_handler)
    
    # Démarrer le bot
    print("Bot démarré...")
    application.run_polling()

if __name__ == '__main__':
    main()
