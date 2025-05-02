# Copyright (C) 2020 Catuserbot <https://github.com/sandy1709/catuserbot>
# Ported by @mrismanaziz
# FROM Man-Userbot <https://github.com/mrismanaziz/Man-Userbot>
# t.me/SharingUserbot & t.me/Lunatic0de

import asyncio

from telethon.tl import functions, types
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.utils import get_display_name

from AyiinXd import BOTLOG_CHATID
from AyiinXd import CMD_HANDLER as cmd
from AyiinXd import CMD_HELP, BLACKLIST_CHAT, LOGS
from AyiinXd.modules.sql_helper.globals import addgvar, gvarstatus
from AyiinXd.ayiin import ayiin_cmd, eod, eor
from AyiinXd.ayiin.tools import media_type
from Stringyins import get_string
from collections import defaultdict
from AyiinXd.events import register


async def unsavegif(event, spammer):
    try:
        await event.client(
            functions.messages.SaveGifRequest(
                id=types.InputDocument(
                    id=spammer.media.document.id,
                    access_hash=spammer.media.document.access_hash,
                    file_reference=spammer.media.document.file_reference,
                ),
                unsave=True,
            )
        )
    except Exception as e:
        LOGS.info(f"{e}")


async def spam_function(event, spammer, xnxx, sleeptimem, sleeptimet, DelaySpam=False):
    counter = int(xnxx[0])
    if len(xnxx) == 2:
        spam_message = str(xnxx[1])
        for _ in range(counter):
            if gvarstatus("spamwork") is None:
                return
            if event.reply_to_msg_id:
                await spammer.reply(spam_message)
            else:
                await event.client.send_message(event.chat_id, spam_message)
            await asyncio.sleep(sleeptimet)
    elif event.reply_to_msg_id and spammer.media:
        for _ in range(counter):
            if gvarstatus("spamwork") is None:
                return
            spammer = await event.client.send_file(
                event.chat_id, spammer, caption=spammer.text
            )
            await unsavegif(event, spammer)
            await asyncio.sleep(sleeptimem)
        if BOTLOG_CHATID:
            if DelaySpam is not True:
                if event.is_private:
                    await event.client.send_message(
                        BOTLOG_CHATID, get_string("spam_1").format(event.chat_id, counter)
                    )
                else:
                    await event.client.send_message(
                        BOTLOG_CHATID, get_string("spam_2").format(get_display_name(await event.get_chat()), event.chat_id, counter)
                    )
            elif event.is_private:
                await event.client.send_message(
                    BOTLOG_CHATID, get_string("spam_3").format(event.chat_id, counter, sleeptimet)
                )
            else:
                await event.client.send_message(
                    BOTLOG_CHATID, get_string("spam_4").format(get_display_name(await event.get_chat()), event.chat_id, counter, sleeptimet)
                )

            spammer = await event.client.send_file(BOTLOG_CHATID, spammer)
            await unsavegif(event, spammer)
        return
    elif event.reply_to_msg_id and spammer.text:
        spam_message = spammer.text
        for _ in range(counter):
            if gvarstatus("spamwork") is None:
                return
            await event.client.send_message(event.chat_id, spam_message)
            await asyncio.sleep(sleeptimet)
    else:
        return
    if DelaySpam is not True:
        if BOTLOG_CHATID:
            if event.is_private:
                await event.client.send_message(
                    BOTLOG_CHATID, get_string("spam_5").format(event.chat_id, counter, spam_message)
                )
            else:
                await event.client.send_message(
                    BOTLOG_CHATID, get_string("spam_6").format(get_display_name(await event.get_chat()), event.chat_id, counter, spam_message)
                )
    elif BOTLOG_CHATID:
        if event.is_private:
            await event.client.send_message(
                BOTLOG_CHATID, get_string("spam_7").format(event.chat_id, sleeptimet, counter, spam_message)
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID, get_string("spam_8").format(get_display_name(await event.get_chat()), event.chat_id, sleeptimet, counter, spam_message)
            )


@ayiin_cmd(pattern="spam ([\\s\\S]*)")
async def nyespam(event):
    if event.chat_id in BLACKLIST_CHAT:
        return await event.edit(get_string("ayiin_1"))
    spammer = await event.get_reply_message()
    xnxx = ("".join(event.text.split(maxsplit=1)[1:])).split(" ", 1)
    try:
        counter = int(xnxx[0])
    except Exception:
        return await eod(
            event, get_string("spam_9").format(cmd)
        )
    if counter > 50:
        sleeptimet = 0.5
        sleeptimem = 1
    else:
        sleeptimet = 0.1
        sleeptimem = 0.3
    await event.delete()
    addgvar("spamwork", True)
    await spam_function(event, spammer, xnxx, sleeptimem, sleeptimet)


@ayiin_cmd(pattern="sspam$")
async def stickerpack_spam(event):
    if event.chat_id in BLACKLIST_CHAT:
        return await event.edit(get_string("ayiin_1"))
    reply = await event.get_reply_message()
    if not reply or media_type(
            reply) is None or media_type(reply) != "Sticker":
        return await eod(
            event, get_string("sspam_1")
        )
    try:
        stickerset_attr = reply.document.attributes[1]
        xyz = await eor(event, get_string("sspam_2"))
    except BaseException:
        await eod(event, get_string("sspam_3"))
        return
    try:
        get_stickerset = await event.client(
            GetStickerSetRequest(
                types.InputStickerSetID(
                    id=stickerset_attr.stickerset.id,
                    access_hash=stickerset_attr.stickerset.access_hash,
                )
            )
        )
    except Exception:
        return await eod(
            xyz, get_string("sspam_4")
        )
    reqd_sticker_set = await event.client(
        functions.messages.GetStickerSetRequest(
            stickerset=types.InputStickerSetShortName(
                short_name=f"{get_stickerset.set.short_name}"
            )
        )
    )
    addgvar("spamwork", True)
    for m in reqd_sticker_set.documents:
        if gvarstatus("spamwork") is None:
            return
        await event.client.send_file(event.chat_id, m)
        await asyncio.sleep(0.7)
    if BOTLOG_CHATID:
        if event.is_private:
            await event.client.send_message(
                BOTLOG_CHATID, get_string("sspam_5").format(event.chat_id)
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID, get_string("sspam_6").format(get_display_name(await event.get_chat()), event.chat_id)
            )
        await event.client.send_file(BOTLOG_CHATID, reqd_sticker_set.documents[0])


@ayiin_cmd(pattern="cspam ([\\s\\S]*)")
async def tmeme(event):
    if event.chat_id in BLACKLIST_CHAT:
        return await event.edit(get_string("ayiin_1"))
    cspam = "".join(event.text.split(maxsplit=1)[1:])
    message = cspam.replace(" ", "")
    await event.delete()
    addgvar("spamwork", True)
    for letter in message:
        if gvarstatus("spamwork") is None:
            return
        await event.respond(letter)
    if BOTLOG_CHATID:
        if event.is_private:
            await event.client.send_message(
                BOTLOG_CHATID, get_string("cspam_1").format(event.chat_id, message)
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID, get_string("cspam_2").format(get_display_name(await event.get_chat()), event.chat_id, message)
            )


@ayiin_cmd(pattern="wspam ([\\s\\S]*)")
async def tmeme(event):
    if event.chat_id in BLACKLIST_CHAT:
        return await event.edit(get_string("ayiin_1"))
    wspam = "".join(event.text.split(maxsplit=1)[1:])
    message = wspam.split()
    await event.delete()
    addgvar("spamwork", True)
    for word in message:
        if gvarstatus("spamwork") is None:
            return
        await event.respond(word)
    if BOTLOG_CHATID:
        if event.is_private:
            await event.client.send_message(
                BOTLOG_CHATID, get_string("wspam_1").format(event.chat_id, message)
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID, get_string("wspam_2").format(get_display_name(await event.get_chat()), event.chat_id, message)
            )


SPAM_STATUS = {}

@ayiin_cmd(pattern="(delayspam|dspam) ([\\s\\S]*)")
async def dlyspam(event):
    if event.chat_id in BLACKLIST_CHAT:
        return await event.edit(get_string("ayiin_1"))
    reply = await event.get_reply_message()
    input_str = "".join(event.text.split(maxsplit=1)[1:]).split(" ", 2)
    try:
        sleeptimet = sleeptimem = float(input_str[0])
    except Exception:
        return await eod(
            event, get_string("dspam_1").format(event.pattern_match.group(1))
        )
    xnxx = input_str[1:]
    try:
        int(xnxx[0])
    except Exception:
        return await eod(
            event, get_string("dspam_1").format(event.pattern_match.group(1))
        )

    await event.delete()
    SPAM_STATUS[event.chat_id] = True
    await delay_spam_function(event, reply, xnxx, sleeptimem, sleeptimet, chat_id=event.chat_id)

@ayiin_cmd(pattern="stopdspam(?:\\s+([\\s\\S]+))?")
async def stop_dlyspam(event):
    args = event.pattern_match.group(1)
    if not args:
        target_chat = event.chat_id
    else:
        if args.startswith("@") or args.isalpha():
            try:
                entity = await event.client.get_entity(args)
                target_chat = entity.id
            except Exception:
                return await event.edit(f"❌ Gagal menemukan grup `{args}`. Pastikan bot sudah join grup tersebut.")
        else:
            try:
                target_chat = int(args)
            except ValueError:
                return await event.edit("⚠️ Format chat ID atau username salah.")

    if target_chat in SPAM_STATUS and SPAM_STATUS[target_chat]:
        SPAM_STATUS[target_chat] = False
        await event.edit(f"🛑 Delay spam di `{target_chat}` berhasil dihentikan.")
    else:
        await event.edit(f"🚫 Tidak ada delay spam aktif di `{target_chat}`.")

@ayiin_cmd(pattern="listdspam$")
async def list_dspam(event):
    if not SPAM_STATUS:
        return await event.edit("✅ Tidak ada delay spam yang aktif.")
    active_chats = [str(cid) for cid, status in SPAM_STATUS.items() if status]
    if not active_chats:
        return await event.edit("✅ Tidak ada delay spam yang aktif.")
    text = "**📋 List Delay Spam Aktif:**\n"
    for cid in active_chats:
        text += f"• `{cid}`\n"
    await event.edit(text)

async def delay_spam_function(event, reply, xnxx, sleeptimem, sleeptimet, chat_id):
    try:
        counter = int(xnxx[0])
        spam_text = str(xnxx[1]) if len(xnxx) > 1 else reply.text if reply else None
    except Exception:
        return await eod(event, "⚠️ Format salah. Coba lagi.")

    if not spam_text:
        return await eod(event, "⚠️ Tidak ada teks untuk di-spam.")

    for _ in range(counter):
        if not SPAM_STATUS.get(chat_id, False):
            break
        await event.client.send_message(chat_id, spam_text)
        await asyncio.sleep(sleeptimem)


SPAMFW_STATUS = {}

@ayiin_cmd(pattern="(delayspamfw|dspamfw) ([\\s\\S]*)")
async def dlyspamfw(event):
    if event.chat_id in BLACKLIST_CHAT:
        return await event.edit(get_string("ayiin_1"))

    input_str = "".join(event.text.split(maxsplit=1)[1:]).split(" ", 2)
    cmd = event.pattern_match.group(1)

    try:
        sleeptimet = sleeptimem = float(input_str[0])
    except Exception:
        return await eod(event, get_string("dspam_1").format(cmd))

    try:
        counter = int(input_str[1])
    except Exception:
        return await eod(event, get_string("dspam_1").format(cmd))

    if len(input_str) < 3:
        return await eod(event, f"⚠️ Format salah. Kirim: `{cmd} <delay> <jumlah> <link_post>`")

    channel_message_link = input_str[2]

    try:
        message_id = int(channel_message_link.split('/')[-1])
        channel_username = channel_message_link.split('/')[3]
        channel = await event.client.get_entity(channel_username)
        message = await event.client.get_messages(channel, ids=message_id)

    except Exception as e:
        return await eod(event, f"Error: {str(e)}")

    await event.delete()
    SPAMFW_STATUS[event.chat_id] = True

    for _ in range(counter):
        if not SPAMFW_STATUS.get(event.chat_id, False):
            break
        await event.client.forward_messages(event.chat_id, message.id, channel)
        await asyncio.sleep(sleeptimem)

    if BOTLOG_CHATID:
        log_msg = get_string("dspamfw_1") if event.is_private else get_string("dspamfw_2")
        context = event.chat_id if event.is_private else get_display_name(await event.get_chat())
        await event.client.send_message(
            BOTLOG_CHATID, log_msg.format(context, event.chat_id, counter, message.text)
        )


@ayiin_cmd(pattern="stopfw(?:\\s+([\\s\\S]+))?")
async def stop_fwspam(event):
    args = event.pattern_match.group(1)
    if not args:
        target_chat = event.chat_id
    else:
        if args.startswith("@") or args.isalpha():
            try:
                entity = await event.client.get_entity(args)
                target_chat = entity.id
            except Exception:
                return await event.edit(f"❌ Gagal menemukan grup `{args}`.")
        else:
            try:
                target_chat = int(args)
            except ValueError:
                return await event.edit("⚠️ Format chat ID atau username salah.")

    if target_chat in SPAMFW_STATUS and SPAMFW_STATUS[target_chat]:
        SPAMFW_STATUS[target_chat] = False
        await event.edit(f"🛑 Forward spam di `{target_chat}` berhasil dihentikan.")
    else:
        await event.edit(f"🚫 Tidak ada forward spam aktif di `{target_chat}`.")


@ayiin_cmd(pattern="listfw$")
async def list_fwspam(event):
    if not SPAMFW_STATUS:
        return await event.edit("✅ Tidak ada forward spam yang aktif.")
    active_chats = [str(cid) for cid, status in SPAMFW_STATUS.items() if status]
    if not active_chats:
        return await event.edit("✅ Tidak ada forward spam yang aktif.")
    text = "**📋 List Forward Spam Aktif:**\n"
    for cid in active_chats:
        text += f"• `{cid}`\n"
    await event.edit(text)
    

# Penyimpanan data
group_list = defaultdict(list)
spam_lists = defaultdict(list)
spam_fw_lists = {}
spam_tasks = {}
fw_tasks = {}

# Tambah grup ke list
@ayiin_cmd(pattern="setgc (\S+) (\S+)")
async def set_gc(event):
    list_name = event.pattern_match.group(1)
    target = event.pattern_match.group(2)
    try:
        entity = await event.client.get_entity(target)
        group_list[list_name].append(entity.id)
        await event.edit(f"✅ Grup **{entity.title}** (`{entity.id}`) berhasil ditambahkan ke list `{list_name}`.")
    except Exception as e:
        await event.edit(f"❌ Gagal: {e}")

# Hapus grup dari list
@ayiin_cmd(pattern="delgc (\S+) (\S+)")
async def del_gc(event):
    list_name = event.pattern_match.group(1)
    target = event.pattern_match.group(2)
    try:
        entity = await event.client.get_entity(target)
        if entity.id in group_list.get(list_name, []):
            group_list[list_name].remove(entity.id)
            await event.edit(f"✅ Grup **{entity.title}** berhasil dihapus dari list `{list_name}`.")
        else:
            await event.edit("❌ Grup tidak ditemukan di list.")
    except Exception as e:
        await event.edit(f"❌ Gagal: {e}")

# Tambah teks ke list
@ayiin_cmd(pattern="setlist (\S+)\n([\s\S]+)")
async def set_list(event):
    list_name = event.pattern_match.group(1)
    text = event.pattern_match.group(2)
    spam_lists[list_name].append(text)
    await event.edit(f"✅ Pesan berhasil ditambahkan ke list `{list_name}`.")

# Hapus teks dari list
@ayiin_cmd(pattern="dellist (\S+) (.+)")
async def del_list(event):
    list_name = event.pattern_match.group(1)
    text = event.pattern_match.group(2)
    if text in spam_lists.get(list_name, []):
        spam_lists[list_name].remove(text)
        await event.edit(f"✅ Pesan dihapus dari list `{list_name}`.")
    else:
        await event.edit("❌ Pesan tidak ditemukan dalam list.")

# Tambah list forward
@ayiin_cmd(pattern="setlistfw (\S+) (\S+)")
async def set_list_fw(event):
    name, link = event.pattern_match.group(1), event.pattern_match.group(2)
    spam_fw_lists[name] = link
    await event.edit(f"✅ Link `{link}` berhasil ditambahkan ke list forward `{name}`.")

# Hapus list forward
@ayiin_cmd(pattern="dellistfw (\S+)")
async def del_list_fw(event):
    name = event.pattern_match.group(1)
    if name in spam_fw_lists:
        del spam_fw_lists[name]
        await event.edit(f"✅ List forward `{name}` berhasil dihapus.")
    else:
        await event.edit("❌ List forward tidak ditemukan.")

# Spam teks ke banyak grup
@ayiin_cmd(pattern="spamset (\d+) (\S+)")
async def spam_set(event):
    delay = int(event.pattern_match.group(1))
    list_name = event.pattern_match.group(2)
    texts = spam_lists.get(list_name)
    targets = group_list.get(list_name)
    if not texts or not targets:
        return await event.edit("❌ List teks atau grup tidak ditemukan.")
    await event.edit(f"▶️ Mulai spam teks ke list `{list_name}`.")

    async def spam_loop():
        while True:
            for chat_id in targets:
                for text in texts:
                    await event.client.send_message(chat_id, text, parse_mode='html')
                    await asyncio.sleep(delay)
    spam_tasks[list_name] = asyncio.create_task(spam_loop())

# Spam forward ke banyak grup
@ayiin_cmd(pattern="spamfw (\d+) (\S+)")
async def spam_fw(event):
    delay = int(event.pattern_match.group(1))
    list_name = event.pattern_match.group(2)
    link = spam_fw_lists.get(list_name)
    targets = group_list.get(list_name)
    if not link or not targets:
        return await event.edit("❌ List forward atau grup tidak ditemukan.")
    await event.edit(f"▶️ Mulai forward dari `{link}` ke list `{list_name}`.")

    async def fw_loop():
        while True:
            for chat_id in targets:
                try:
                    await event.client.forward_messages(chat_id, link, from_peer=link)
                    await asyncio.sleep(delay)
                except Exception:
                    continue
    fw_tasks[list_name] = asyncio.create_task(fw_loop())

# Stop spam teks
@ayiin_cmd(pattern="stopset (\S+)")
async def stop_set(event):
    name = event.pattern_match.group(1)
    task = spam_tasks.get(name)
    if task:
        task.cancel()
        del spam_tasks[name]
        await event.edit(f"✅ Spam teks `{name}` dihentikan.")
    else:
        await event.edit("❌ Tidak ada spam teks berjalan untuk list itu.")

# Stop spam forward
@ayiin_cmd(pattern="sstopfw (\S+)")
async def stop_fw(event):
    name = event.pattern_match.group(1)
    task = fw_tasks.get(name)
    if task:
        task.cancel()
        del fw_tasks[name]
        await event.edit(f"✅ Spam forward `{name}` dihentikan.")
    else:
        await event.edit("❌ Tidak ada spam forward berjalan untuk list itu.")

# Lihat semua list berjalan
@ayiin_cmd(pattern=r"spamcek$")
async def spam_cek(event):
    msg = "**📡 Daftar Spam Aktif:**\n"
    if spam_tasks:
        msg += "\n**📝 Spam Teks:**"
        for name in spam_tasks:
            msg += f"\n • `{name}`"
    else:
        msg += "\n❌ Tidak ada spam teks aktif."

    if fw_tasks:
        msg += "\n\n**🔁 Spam Forward:**"
        for name in fw_tasks:
            msg += f"\n • `{name}`"
    else:
        msg += "\n\n❌ Tidak ada spam forward aktif."

    await event.edit(msg)

# Vspam contoh
@ayiin_cmd(pattern="vspam (\d+) (.+)")
async def vspam_handler(event):
    count = int(event.pattern_match.group(1))
    text = event.pattern_match.group(2)
    for _ in range(count):
        await event.respond(text)

# Cek semua list, forward, grup
@ayiin_cmd(pattern="listall$")
async def list_all_data(event):
    if not spam_lists and not spam_fw_lists and not group_list:
        return await event.edit("❌ Belum ada data tersimpan (list teks, forward, atau grup).")
    
    msg = "**📦 Daftar Semua List Tersimpan:**\n"

    # List Teks
    if spam_lists:
        msg += "\n**📄 List Teks:**"
        for name, teks in spam_lists.items():
            msg += f"\n  • `{name}` ({len(teks)} item)"
    else:
        msg += "\n\nTidak ada list teks."

    # List Forward
    if spam_fw_lists:
        msg += "\n\n**🔁 List Forward:**"
        for name, link in spam_fw_lists.items():
            msg += f"\n  • `{name}` → {link}"
    else:
        msg += "\n\nTidak ada list forward."

    # List Grup
    if group_list:
        msg += "\n\n**👥 List Grup per List:**"
        for listname, gcs in group_list.items():
            msg += f"\n  • `{listname}`:"
            for gc in gcs:
                try:
                    chat = await event.client.get_entity(gc)
                    name = chat.title or chat.first_name
                    username = f"@{chat.username}" if getattr(chat, 'username', None) else f"`{gc}`"
                    msg += f"\n     └ {name} ({username})"
                except Exception:
                    msg += f"\n     └ `ID: {gc}` (gagal ambil info)"
    else:
        msg += "\n\nTidak ada grup yang tersimpan."

    await event.edit(msg)

@ayiin_cmd(pattern="vwspam$")
async def view_spam(event):
    teks = "**• SPAM YANG SEDANG BERJALAN •**\n"

    # View spamset teks
    if aktif_spamset:
        teks += "\n\n**Spamset (Teks):**"
        for listname, data in aktif_spamset.items():
            teks += f"\n• **List:** `{listname}`"
            for chat_id in data.get("chats", []):
                try:
                    chat = await event.client.get_entity(chat_id)
                    name = f"[{chat.title}](https://t.me/{chat.username})" if getattr(chat, "username", None) else f"`{chat.title}`"
                except Exception:
                    name = f"`{chat_id}`"
                teks += f"\n    - {name}"
    else:
        teks += "\n\n**Spamset (Teks):** Tidak ada."

    # View spamfw forward
    if aktif_spamfw:
        teks += "\n\n**Spamfw (Forward):**"
        for listname, data in aktif_spamfw.items():
            teks += f"\n• **List:** `{listname}`"
            for chat_id in data.get("chats", []):
                try:
                    chat = await event.client.get_entity(chat_id)
                    name = f"[{chat.title}](https://t.me/{chat.username})" if getattr(chat, "username", None) else f"`{chat.title}`"
                except Exception:
                    name = f"`{chat_id}`"
                teks += f"\n    - {name}"
    else:
        teks += "\n\n**Spamfw (Forward):** Tidak ada."

    await event.edit(teks, link_preview=False)
    
CMD_HELP.update(
    {
        "spam": f"**Plugin :** `spam`\
\n\n  »  **Perintah :** `{cmd}spam` <jumlah> <teks>\
\n  »  **Kegunaan :** Membanjiri chat dengan teks berulang sebanyak jumlah yang ditentukan.\
\n\n  »  **Perintah :** `{cmd}cspam` <teks>\
\n  »  **Kegunaan :** Spam karakter satu per satu dari teks yang diberikan.\
\n\n  »  **Perintah :** `{cmd}sspam` <balas stiker>\
\n  »  **Kegunaan :** Spam semua stiker dari sticker pack yang dibalas.\
\n\n  »  **Perintah :** `{cmd}wspam` <teks>\
\n  »  **Kegunaan :** Spam kata per kata dari teks.\
\n\n  »  **Perintah :** `{cmd}picspam` <jumlah> <link_gambar>\
\n  »  **Kegunaan :** Spam gambar/foto/gif dari link yang diberikan.\
\n\n  »  **Perintah :** `{cmd}delayspam` <delay> <jumlah> <teks>\
\n  »  **Kegunaan :** Spam teks dengan jeda antar pesan.\
\n\n  »  **Perintah :** `{cmd}stopdspam`\
\n  »  **Kegunaan :** Menghentikan spam delay di grup saat ini.\
\n\n  »  **Perintah :** `{cmd}listdspam`\
\n  »  **Kegunaan :** Menampilkan semua spam delay yang aktif.\
\n\n  »  **Perintah :** `{cmd}dspamfw` <delay> <jumlah> <link_post_channel>\
\n  »  **Kegunaan :** Spam konten dari post channel berkali-kali dengan delay.\
\n\n  »  **Perintah :** `{cmd}stopfw`\
\n  »  **Kegunaan :** Menghentikan spam forward di grup saat ini.\
\n\n  »  **Perintah :** `{cmd}listfw`\
\n  »  **Kegunaan :** Menampilkan semua spam forward yang sedang aktif.\
\n\n  »  **Perintah :** `{cmd}vspam` <jumlah> <teks>\
\n  »  **Kegunaan :** Spam teks biasa sebanyak jumlah yang ditentukan.\
\n\n  »  **Perintah :** `{cmd}setlist` <nama_list> <teks>\
\n  »  **Kegunaan :** Menyimpan teks spam (hyperlink atau teks kebawah) ke dalam list.\
\n\n  »  **Perintah :** `{cmd}dellist` <nama_list> <isi>\
\n  »  **Kegunaan :** Menghapus isi tertentu dari list spam.\
\n\n  »  **Perintah :** `{cmd}setlistfw` <nama_list> <link_post_channel>\
\n  »  **Kegunaan :** Menyimpan list spam forward berdasarkan post dari channel.\
\n\n  »  **Perintah :** `{cmd}dellistfw` <nama_list>\
\n  »  **Kegunaan :** Menghapus list forward berdasarkan nama list.\
\n\n  »  **Perintah :** `{cmd}setgc` <nama_list> <@usergc/ID>\
\n  »  **Kegunaan :** Menambahkan grup ke list tujuan spam.\
\n\n  »  **Perintah :** `{cmd}delgc` <nama_list> <@usergc/ID>\
\n  »  **Kegunaan :** Menghapus grup dari list tujuan spam.\
\n\n  »  **Perintah :** `{cmd}spamset` <delay> <nama_list>\
\n  »  **Kegunaan :** Menyebar isi list teks ke grup-grup yang sudah diset.\
\n\n  »  **Perintah :** `{cmd}spamfw` <delay> <nama_list>\
\n  »  **Kegunaan :** Menyebar post channel dari list forward ke grup-grup yang diset.\
\n\n  »  **Perintah :** `{cmd}stopset`\
\n  »  **Kegunaan :** Menghentikan proses spamset yang sedang berjalan.\
\n\n  »  **Perintah :** `{cmd}sstopfw`\
\n  »  **Kegunaan :** Menghentikan proses spamfw yang sedang berjalan.\
\n\n  »  **Perintah :** `{cmd}spamcek`\
\n  »  **Kegunaan :** Menampilkan semua list teks, list forward, dan list grup yang tersimpan.\
\n\n  »  **Perintah :** `{cmd}vwspam`\
\n  »  **Kegunaan :** Melihat semua spamset/spamfw yang aktif dan sedang berjalan.\
\n\n  •  **NOTE :** Spam dengan Risiko Anda sendiri. Jangan salah gunakan!"
    }
)
