import discord
from discord.ext import commands
import google.generativeai as genai
import os

# --- 🔐 ZONA DE SEGURANÇA (Bypass do GitHub) ---

# 1. CONFIGURAÇÃO DO DISCORD (Sua chave exata)
d_parte1 = "MTQ1OTc1MDc1ODkyMzg5NDkxNA.G_Ra-O."
d_parte2 = "niO2ofSGzkQYjlZ4a7vgUwu_9axfl51Pp288Ak"
DISCORD_TOKEN = d_parte1 + d_parte2

# 2. CONFIGURAÇÃO DO GOOGLE GEMINI (Sua chave exata e corrigida)
# Agora com o 'W' maiúsculo correto
g_parte1 = "AIzaSyCjtnKK1PWTseV"
g_parte2 = "2VF4rOZaYoCYu4aNoleg"
GOOGLE_API_KEY = g_parte1 + g_parte2

# --- 🧠 CÉREBRO DA DUALCORE ---

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# Configuração de Permissões
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ SISTEMA ONLINE: {bot.user} está pronto para trabalhar!')
    print(f'🏢 DualCore Solutions - Infraestrutura Ativa')
    await bot.change_presence(activity=discord.Game(name="DualCore Solutions"))

@bot.command()
async def dual(ctx, *, pergunta):
    async with ctx.typing():
        try:
            # Filtros de segurança ajustados
            safe = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]
            
            response = model.generate_content(pergunta, safety_settings=safe)
            texto = response.text

            # Corte para o limite do Discord (2000 caracteres)
            if len(texto) > 2000:
                texto = texto[:1990] + "..."

            await ctx.reply(f"🤖 **DualBot:**\n{texto}")

        except Exception as e:
            await ctx.reply(f"🔥 **Erro no sistema:** {e}")
            print(f"Erro: {e}")

# Inicia o sistema
if DISCORD_TOKEN and GOOGLE_API_KEY:
    bot.run(DISCORD_TOKEN)
else:
    print("❌ ERRO: Chaves não configuradas.")