# repack by blue. #
""" Userbot start point """

import sys
import time
import os
import asyncpg
from importlib import import_module
from platform import python_version

from pytgcalls import __version__ as pytgcalls
from telethon import version
from telethon.tl.alltlobjects import LAYER
from AyiinXd.ayiin.events import ajg
from AyiinXd import BOT_TOKEN, bot
from AyiinXd import BOT_VER as ubotversion
from AyiinXd import BOTLOG_CHATID, LOGS, LOOP, bot
from AyiinXd.clients import ayiin_userbot_on, multiayiin
from AyiinXd.core.git import git
from AyiinXd.modules import ALL_MODULES
from AyiinXd.ayiin import AyiinDB, HOSTED_ON, autobot, autopilot, ayiin_version

# ⏱️ Fungsi untuk inisialisasi durasi pertama kali
async def init_bot_durasi():
    try:
        DATABASE_URL = os.getenv("DATABASE_URL")
        DURASI_UBOT = os.getenv("DURASI_UBOT").lower()
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS bot_info (
                id INTEGER PRIMARY KEY,
                start_time BIGINT,
                jenis TEXT
            );
        """)
        row = await conn.fetchrow("SELECT id FROM bot_info WHERE id=1")
        if not row:
            now = int(time.time())
            await conn.execute("""
                INSERT INTO bot_info (id, start_time, jenis)
                VALUES (1, $1, $2)
            """, now, DURASI_UBOT)
        await conn.close()
    except Exception as e:
        print(f"[ERROR INIT DURASI] {e}")

# ⛔ Matikan userbot jika durasi habis
async def cek_auto_expired():
    try:
        DATABASE_URL = os.getenv("DB_URI")
        conn = await asyncpg.connect(DATABASE_URL)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS bot_info (
                id INTEGER PRIMARY KEY,
                start_time BIGINT,
                jenis TEXT
            );
        """)
        row = await conn.fetchrow("SELECT start_time, jenis FROM bot_info WHERE id=1")
        await conn.close()
        if not row:
            return

        jenis = row["jenis"]
        start_time = row["start_time"]
        now = int(time.time())

        if jenis == "lifetime":
            return

        def konversi_ke_detik(durasi: str) -> int:
            jumlah = ''.join(filter(str.isdigit, durasi))
            satuan = ''.join(filter(str.isalpha, durasi))
            if not jumlah or not satuan:
                return 0
            jumlah = int(jumlah)
            konversi = {
                "menit": 60,
                "jam": 3600,
                "hari": 86400,
                "minggu": 7 * 86400,
                "bulan": 30 * 86400,
                "tahun": 365 * 86400,
            }
            return jumlah * konversi.get(satuan, 0)

        total_durasi = konversi_ke_detik(jenis)
        sisa = total_durasi - (now - start_time)

        if sisa <= 0:
            print("[❌] Durasi userbot telah habis. Mematikan...")
            sys.exit(0)
    except Exception as e:
        print(f"[ERROR CEK DURASI HABIS] {e}")

# 🔁 Load semua modul & start bot
try:
    for module_name in ALL_MODULES:
        import_module(f"AyiinXd.modules.{module_name}")
    adB = AyiinDB()
    client = multiayiin()
    git()
    LOOP.run_until_complete(cek_auto_expired())  # ⛔ auto mati jika expired
    LOOP.run_until_complete(init_bot_durasi())   # ⏱️ inisialisasi durasi
    LOGS.info(f"Python Version - {python_version()}")
    LOGS.info(f"Telethon Version - {version.__version__} [Layer: {LAYER}]")
    LOGS.info(f"PyTgCalls Version - {pytgcalls}")
    LOGS.info(f"Userbot Version - {ubotversion} •[{adB.name}]•")
    LOGS.info(f"IXALL Version - {ayiin_version} •[{HOSTED_ON}]•")
    LOGS.info("[🔥 USERBOT BERHASIL DIAKTIFKAN 🔥]")
except (ConnectionError, KeyboardInterrupt, NotImplementedError, SystemExit):
    pass
except BaseException as e:
    LOGS.info(str(e), exc_info=True)
    sys.exit(1)

# 🚀 Start userbot
LOOP.run_until_complete(ayiin_userbot_on())
LOOP.run_until_complete(ajg())
if not BOTLOG_CHATID:
    LOOP.run_until_complete(autopilot())
if not BOT_TOKEN:
    LOOP.run_until_complete(autobot())

if len(sys.argv) not in (1, 3, 4):
    bot.disconnect()
else:
    try:
        bot.run_until_disconnected()
    except ConnectionError:
        pass
