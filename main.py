from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
TOKEN = "8514555312:AAH5BNs0naq3BeFq2-n8UXt_2U9NOdNgiXk"
# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📄 RUC", callback_data="ruc")],
        [InlineKeyboardButton("🧾 Declaraciones", callback_data="declaraciones")],
        [InlineKeyboardButton("💻 Facturación Electrónica", callback_data="facturacion"),
        InlineKeyboardButton("🧾 Facturación Física", callback_data="facturacion_fisica")],
        [InlineKeyboardButton("🔐 Clave SRI", callback_data="clave")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "¿Qué trámite deseas realizar en el SRI?",
        reply_markup=reply_markup
    )

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

    keyboard = [
        [InlineKeyboardButton("⬅ Volver al menú", callback_data="volver")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=texto, reply_markup=reply_markup)

# ---------------- VOLVER ----------------
async def volver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await start(query, context)

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
