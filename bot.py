import discord
from discord.ext import commands
import database
import image_generator
import os

from dotenv import load_dotenv

# .env'den token'i al
load_dotenv(override=True)
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN bulunamadi! .env dosyasina ekle.")

# bot ayarlari
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


def get_task_by_sira(sira):
    """kullanicinin girdigi sira numarasindan db'deki task'i bul.
    mesela 3 gorev varsa kullanici 1-2-3 yazar, ben db id'sine ceviriyorum"""
    tasks = database.get_tasks()
    if sira < 1 or sira > len(tasks):
        return None
    return tasks[sira - 1]


@bot.event
async def on_ready():
    database.init_db()
    print(f"Bot hazir: {bot.user}")


@bot.command()
async def add_task(ctx, *, description: str):
    """yeni gorev ekle"""
    database.add_task(description)
    total = len(database.get_tasks())
    await ctx.send(f"Görev eklendi (toplam {total}). !show_tasks ile gorebilirsin.")


@bot.command()
async def show_tasks(ctx):
    """tum gorevleri listele"""
    tasks = database.get_tasks()
    if not tasks:
        await ctx.send("Henüz görev yok.")
        return

    msg = "**Görev Listesi:**\n"
    for i, t in enumerate(tasks, start=1):
        status = "✅" if t["completed"] else "⬜"
        msg += f"`{i}` - {t['description']} {status}\n"

    await ctx.send(msg)


@bot.command()
async def delete_task(ctx, task_id: int):
    """gorev sil"""
    task = get_task_by_sira(task_id)
    if task is None:
        await ctx.send(f"#{task_id} diye bir görev bulamadım.")
        return

    database.delete_task(task["id"])
    await ctx.send(f"#{task_id} silindi.")


@bot.command()
async def complete_task(ctx, task_id: int):
    """gorevi tamamlandi olarak isaretle"""
    task = get_task_by_sira(task_id)
    if task is None:
        await ctx.send(f"#{task_id} bulunamadı, id'yi kontrol et.")
        return

    database.complete_task(task["id"])
    await ctx.send(f"#{task_id} tamamlandı olarak işaretlendi 🎉")


@bot.command()
async def celebrate(ctx, task_id: int):
    """tamamlanan gorev icin kutlama gorseli olustur.
    pollinations.ai api kullaniyorum (reve api alternatifi)"""
    task = get_task_by_sira(task_id)

    if task is None:
        await ctx.send("Böyle bir görev yok.")
        return

    if not task["completed"]:
        await ctx.send("Bu görev henüz tamamlanmadı, önce !complete_task ile tamamla.")
        return

    await ctx.send(f"'{task['description']}' için kutlama görseli oluşturuluyor...")

    try:
        # api'den gorsel al ve gonder
        filepath = image_generator.generate_celebration_image(
            task["description"], task_id=task["id"]
        )

        file = discord.File(filepath, filename="celebration.png")
        await ctx.send("İşte kutlama posterin! 🥳", file=file)

    except Exception as err:
        print(f"celebrate hatasi: {err}")
        await ctx.send("Görsel oluşturulurken hata oldu, tekrar dene.")


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)