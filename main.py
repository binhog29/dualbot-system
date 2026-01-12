import discord
from discord.ext import commands
import google.generativeai as genai
import os

# Busca as senhas nas Variaveis de Ambiente (Seguranca)
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


# --- PERSONALIDADE CORPORATIVA ---
instrucoes_sistema = """
Você é o DualBot, a Inteligência Artificial oficial e exclusiva da empresa DualCore Solutions.
Seus criadores e diretores são Fabio Borges e Bruno Borges.
Você age como um funcionário sênior da empresa: é extremamente educado, técnico, direto e profissional.
Nunca diga que foi criado pelo Google. Se perguntarem, diga que é o sistema proprietário da DualCore.
"""

# 1. Configuração do Cérebro (Gemini 2.0 Flash)
# Este modelo foi validado na sua conta e é o mais rápido disponível.
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash', system_instruction=instrucoes_sistema)

# 2. Configuração do Bot Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ SISTEMA ONLINE: {bot.user} carregado com sucesso!')
    await bot.change_presence(activity=discord.Game(name="DualCore AI | Online"))

@bot.command()
async def dual(ctx, *, pergunta):
    async with ctx.typing():
        try:
            # Filtros de segurança no mínimo para evitar bloqueios bobos
            safe = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]
            
            # Gera a resposta
            response = model.generate_content(pergunta, safety_settings=safe)
            
            if response.text:
                texto = response.text
                # O Discord tem limite de 2000 letras, cortamos se passar
                if len(texto) > 2000: texto = texto[:1990] + "..."
                
                await ctx.reply(f"🤖 **DualBot:**\n{texto}")
            else:
                await ctx.reply("🤖 **DualBot:** [Erro] Resposta vazia.")
                
        except Exception as e:
            await ctx.reply(f"❌ Erro de processamento: {e}")

# Iniciar Execução
bot.run(DISCORD_TOKEN)