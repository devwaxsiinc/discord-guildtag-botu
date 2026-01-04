import discord
import json
from discord.ext import commands

# Ayarları yükle
with open('ayarlar.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

intents = discord.Intents.default()
intents.members = True  # Üyeleri takip etmek için
intents.presences = True # Etiket değişimlerini yakalamak için bazen gerekebilir

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} aktif! Klan etiketi kontrol ediliyor: {config["tag_adi"]}')

@bot.event
async def on_member_update(before, after):
    # Ayarları değişkene al
    hedef_tag = config["tag_adi"]
    rol_id = int(config["rol_id"])
    guild = after.guild
    
    # Sunucu kontrolü (Sadece belirtilen sunucuda çalışsın)
    if str(guild.id) != config["sunucu_id"]:
        return

    rol = guild.get_role(rol_id)
    if not rol:
        return

    # KULLANICININ KLAN ETİKETİNİ KONTROL ET
    # Discord API'sinde clan bilgisi 'clan' özniteliği altında tutulur
    user_clan_tag = None
    if hasattr(after, 'clan') and after.clan:
        user_clan_tag = after.clan.tag

    # Rol verme/alma mantığı
    if user_clan_tag == hedef_tag:
        if rol not in after.roles:
            await after.add_roles(rol)
            print(f"[+] {after.name} klan etiketini taktığı için rol verildi.")
    else:
        if rol in after.roles:
            await after.remove_roles(rol)
            print(f"[-] {after.name} klan etiketini çıkardığı için rol alındı.")

bot.run(config["token"])