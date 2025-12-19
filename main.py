from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("TOKEN no configurado")

# ---------- MENU ----------
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
    await chat.send_message(
        "¿Qué trámite deseas realizar en el SRI?",
        reply_markup=reply_markup
    )

# ---------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await mostrar_menu(update.message.chat, context)

# ---------- CALLBACKS ----------
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    opciones = {
        "ruc": (
            "📄 Trámites del RUC\n\n"
            "Inscripción, actualización o suspensión.\n\n"
            "🔗 https://srienlinea.sri.gob.ec/sri-en-linea/consulta/1"
        ),
        "declaraciones": (
            "🧾 Declaraciones\n\n"
            "IVA, Renta y anexos.\n\n"
            "🔗 https://srienlinea.sri.gob.ec/sri-en-linea/consulta/72"
        ),
        "facturacion": (
            "💻 Facturación Electrónica\n\n"
            "🔗 https://srienlinea.sri.gob.ec/sri-en-linea/consulta/55"
        ),
        "facturacion_fisica": (
            "🧾 Facturación Física\n\n"
            "🔗 http://srienlinea.sri.gob.ec/sri-en-linea/consulta/36"
        ),
        "clave": (
            "🔐 Clave SRI\n\n"
            "🔗 https://srienlinea.sri.gob.ec/sri-en-linea/consulta/19"
        )
    }

    texto = opciones.get(query.data, "Opción no válida")

    await query.message.delete()
    await context.bot.send_message(
        chat_id=query.message.chat.id,
        text=texto,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("⬅ Volver", callback_data="volver")]]
        )
    )

async def volver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.delete()
    await mostrar_menu(query.message.chat, context)

# ---------- MAIN ----------
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(volver, pattern="volver"))
    app.add_handler(CallbackQueryHandler(menu))
    print("Bot del SRI activo...")
    app.run_polling()

if __name__ == "__main__":
    main()
