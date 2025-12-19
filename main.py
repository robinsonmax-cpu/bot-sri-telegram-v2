from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("La variable de entorno TOKEN no está configurada")

# ---------------- START ----------------
async def mostrar_menu(chat, context):
    keyboard = [
        [InlineKeyboardButton("📄 RUC", callback_data="ruc")],
        [InlineKeyboardButton("🧾 Declaraciones", callback_data="declaraciones")],
        [
            InlineKeyboardButton("💻 Facturación Electrónica", callback_data="facturacion"),
            InlineKeyboardButton("🧾 Facturación Física", callback_data="facturacion_fisica")
        ],
        [InlineKeyboardButton("🔐 Clave SRI", callback_data="clave")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=chat.id,
        text="¿Qué trámite deseas realizar en el SRI?",
        reply_markup=reply_markup
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await mostrar_menu(update.message.chat, context)


# ---------------- MENU ----------------
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "ruc":
        texto = (
            "📄 Trámites del RUC\n\n"
            "Inscripción, actualización o suspensión del RUC.\n\n"
            "🔗 https://srienlinea.sri.gob.ec/sri-en-linea/consulta/1"
        )
    elif query.data == "declaraciones":
        texto = (
            "🧾 Declaraciones de Impuestos\n\n"
            "IVA, Renta y anexos.\n\n"
            "🔗 https://srienlinea.sri.gob.ec/sri-en-linea/consulta/72"
        )
    elif query.data == "facturacion":
        texto = (
            "💻 Facturación Electrónica\n\n"
            "Información para emitir comprobantes electrónicos.\n\n"
            "🔗 https://srienlinea.sri.gob.ec/sri-en-linea/consulta/55"
        )
    elif query.data == "facturacion_fisica":
        texto = (
            "🧾 Facturación Física\n\n"
            "Autorización y gestión de comprobantes físicos.\n\n"
            "🔗 http://srienlinea.sri.gob.ec/sri-en-linea/consulta/36"
        )
    elif query.data == "clave":
        texto = (
            "🔐 Clave SRI\n\n"
            "Recuperación o creación de clave.\n\n"
            "🔗 https://srienlinea.sri.gob.ec/sri-en-linea/consulta/19"
        )
    else:
        texto = "Opción no válida."

    keyboard = [[InlineKeyboardButton("⬅ Volver al menú", callback_data="volver")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # eliminar mensaje anterior
    try:
        await query.message.delete()
    except:
        pass

    # enviar mensaje nuevo
    await context.bot.send_message(
        chat_id=query.message.chat.id,
        text=texto,
        reply_markup=reply_markup
    )



# ---------------- VOLVER ----------------
async def volver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        await query.message.delete()
    except:
        pass

    await mostrar_menu(query.message.chat, context)


# ---------------- MAIN ----------------
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(volver, pattern="volver"))
    app.add_handler(CallbackQueryHandler(menu))

    print("Bot del SRI activo...")
    app.run_polling()


if __name__ == "__main__":
    main()
