import discord
from discord.ext import commands
import google.generativeai as genai
import os

# --- 🔐 ZONA DE SEGURANÇA ---
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# --- 🧠 CÉREBRO DA DUALCORE ---
genai.configure(api_key=GOOGLE_API_KEY)

# --- 👔 PERSONALIDADE (O SEGREDO) ---
# Aqui definimos a alma do negócio.
system_instruction = """
Você é o DualBot, a Inteligência Artificial oficial e exclusiva da DualCore Solutions.
Seus criadores e diretores são Fabio Borges e Bruno Borges.
Você age como um funcionário sênior da empresa: é extremamente profissional, prestativo e técnico.
Nunca diga que foi criado pelo Google. Se perguntarem, diga que foi desenvolvido internamente pela DualCore.
"""

# Criamos o modelo já com a personalidade embutida
model = genai.GenerativeModel(
    'gemini-2.0-flash',
    system_instruction=system_instruction
)

# Configuração do Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ SISTEMA ONLINE: {bot.user} na escuta!')
    await bot.change_presence(activity=discord.Game(name="DualCore Solutions"))

@bot.command()
async def dual(ctx, *, pergunta):
    async with ctx.typing():
        try:
            safe = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]
            
            response = model.generate_content(pergunta, safety_settings=safe)
            texto = response.text

            if len(texto) > 2000:
                texto = texto[:1990] + "..."

            await ctx.reply(f"🤖 **DualBot:**\n{texto}")

        except Exception as e:
            await ctx.reply(f"🔥 **Erro:** {e}")
            print(f"Erro: {e}")

if DISCORD_TOKEN and GOOGLE_API_KEY:
    bot.run(DISCORD_TOKEN)
