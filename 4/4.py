from dotenv import load_dotenv
from telethon.sync import TelegramClient, events
import os
import json
import asyncio

# async def getListOfGroups(client):
#     try:
#         dialogs = await client.get_dialogs()
#         groups_info = []
#         for dialog in dialogs:
#             if dialog.is_group or dialog.is_channel:  # Filtra los grupos y canales
#                 group_info = {'group_id': dialog.id, 'group_name': dialog.title}
#                 groups_info.append(group_info)
#                 # Imprimir el nombre y el ID del grupo
#                 print(f"Grupo: {dialog.title}, ID: {dialog.id}")
#         return groups_info
#     except Exception as e:
#         print(f"Error: {e}")
#         return []

async def getListOfGroups(client):
    try:
        dialogs = await client.get_dialogs()
        groups_info = []
        for dialog in dialogs:
            if dialog.is_group or dialog.is_channel:
                entity = await client.get_entity(dialog.id)
                can_send_messages = entity.default_banned_rights is None or not entity.default_banned_rights.send_messages
                if can_send_messages:
                    group_info = {'group_id': dialog.id, 'group_name': dialog.title}
                    groups_info.append(group_info)

        return groups_info
    except Exception as e:
        print(e)
        return []

async def getMessagesFromGroup(client, group_id):
    try:
        all_messages = []
        async for message in client.iter_messages(group_id):
            try:
                all_messages.append(message)
            except:
                pass
        return all_messages
    except Exception as e:
        print(e)
        return []

async def logUserBot():
    load_dotenv()
    api_id = int(29245178)
    api_hash = "0be88ee59a26a56a28c955d001a64b64"
    phone_number = "51981885592"
    session_name = "bot_spammer"
    client = TelegramClient(session_name, api_id, api_hash)

    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(phone_number)
        await client.sign_in(phone_number, input('Ingrese el código de verificación: '))
    await client.send_message("@spmmorgan7", f'<b>Bot encendido</b>', parse_mode="HTML")
    spammer_group = int("-1002351366917")
    spammer_group2 = int("-1002331326186") # Mensajes Especiales
    spammer_group3 = int("-1002425258747") # Mensajes Bins Peru
    spammer_group4 = int("-1002432211914") # Mensajes Peru Ayuda

    @client.on(events.NewMessage)
    async def my_event_handler(event):
        # Verificar si el mensaje proviene de un chat privado
        if event.is_private:
            sender = await event.get_sender()
            sender_id = sender.id
            message = event.message.message
            # Responder solo en chats privados
            await client.send_message(sender_id, "Hola, esta es una cuenta de spam. Si deseas adquirir algun servicio, escríbele a @XeX_Morgan.")


    # Lista de IDs de grupos/canales a los que no quieres enviar mensajes
    excluded_group_ids = [-1002351366917,-1002331326186,-1002425258747,-1002432211914,-1002407157979,-1002442286122,-1001926519077,-1001580673964,-1001907073788,-1001737351681,-1001733869168,-1001829996546,-1002018025154,-1001859082953,-4553972318,-4553791708,-4559750226,-4586567990]
    special_group_ids = [-1001724620371,-1001760634472,-1002158967551,-1002125807620,-1001617010310,-1001867739320,-1002221235561,-1002074331354,-1001789640951,-1001899823705,-1001890531963,-1001781855275,-1001538693959]
    bins_peru_groups_ids = [-1001724620371,-1001760634472,-1002158967551,-1002125807620]
    peru_ayuda_groups_ids = [-1001617010310,-1001867739320,-1002221235561,-1002074331354,-1001789640951,-1001899823705,-1001890531963]
    other_groups_ids = [-1001781855275,-1001538693959]
    peru_ayuda_id = -1001789640951
    bins_peru_id = -1001724620371

    while True:
        groups_info = await getListOfGroups(client)
        messages_list = await getMessagesFromGroup(client, spammer_group)
        special_messages_list = await getMessagesFromGroup(client, spammer_group2)
        mensajes_bins_peru = await getMessagesFromGroup(client, spammer_group3)
        mensajes_peru_ayuda = await getMessagesFromGroup(client, spammer_group4)
        try:
            await client.send_message("@spmmorgan7", f"<b>CANTIDAD DE MENSAJES CONSEGUIDOS PARA PUBLICAR</b> <code>{len(messages_list)-1}</code>", parse_mode="HTML")
        except:
            pass
            
        try:
            for i in groups_info:
                if i['group_id'] not in excluded_group_ids:

                    if i['group_id'] in special_group_ids:
                        if i['group_id'] == bins_peru_id:
                            lista_mensajes = mensajes_bins_peru
                        elif i['group_id'] == peru_ayuda_id or i['group_id'] in bins_peru_groups_ids:
                            lista_mensajes = mensajes_peru_ayuda
                        else:
                            lista_mensajes = special_messages_list
                        j = 0
                        for message_spam in lista_mensajes:
                            j += 1
                            resultado = True
                            try:
                                if i['group_id'] == bins_peru_id:
                                    await client.send_message(i["group_id"], message_spam)
                                else:
                                    await client.forward_messages(i["group_id"], message_spam)
                            except Exception as error:
                                # Verifica si el error es "CHAT_SEND_PHOTOS_FORBIDDEN"
                                if "CHAT_SEND_PHOTOS_FORBIDDEN" in str(error):
                                    # Intenta enviar solo el texto
                                    try:
                                        await client.send_message(i["group_id"], message_spam.text)
                                        await client.send_message("@spmmorgan7", f'<b>Enviado solo texto a {i["group_id"]}</b> - <code>{i["group_name"]}</code>', parse_mode="HTML")
                                    except Exception as new_error:
                                        await client.send_message("@spmmorgan7", f'<b>Error enviando solo texto a {i["group_id"]}</b> - <code>{i["group_name"]}</code>\nCausa: {new_error}', parse_mode="HTML")
                                elif "banned from sending messages" in str(error) or "A wait of" in str(error):
                                    continue
                                else:
                                    await client.send_message("@spmmorgan7", f'<b>Error enviando mensajes a {i["group_id"]}</b> - <code>{i["group_name"]}</code>\nCausa: {error}', parse_mode="HTML")
                                resultado = False
                            if resultado:
                                await client.send_message("@spmmorgan7", f'<b>Mensaje enviado a {i["group_id"]}</b> - <code>{i["group_name"]}</code>', parse_mode="HTML")  
                            if j == 3: 
                                await asyncio.sleep(10)
                                break
                            else:
                                if i['group_id'] in bins_peru_groups_ids:
                                    await asyncio.sleep(120)
                                elif i['group_id'] in peru_ayuda_groups_ids:
                                    await asyncio.sleep(30)
                                else:
                                    await asyncio.sleep(10)
                    else:
                        j = 0
                        for message_spam in messages_list:
                            j += 1
                            resultado = True
                            try:
                                await client.forward_messages(i["group_id"], message_spam)
                            except Exception as error:
                                # Verifica si el error es "CHAT_SEND_PHOTOS_FORBIDDEN"
                                if "CHAT_SEND_PHOTOS_FORBIDDEN" in str(error):
                                    # Intenta enviar solo el texto
                                    try:
                                        await client.forward_messages(i["group_id"], message_spam.text)
                                        await client.send_message("@spmmorgan7", f'<b>Enviado solo texto a {i["group_id"]}</b> - <code>{i["group_name"]}</code>', parse_mode="HTML")
                                    except Exception as new_error:
                                        await client.send_message("@spmmorgan7", f'<b>Error enviando solo texto a {i["group_id"]}</b> - <code>{i["group_name"]}</code>\nCausa: {new_error}', parse_mode="HTML")
                                elif "banned from sending messages" in str(error) or "A wait of" in str(error):
                                    continue
                                else:
                                    await client.send_message("@spmmorgan7", f'<b>Error enviando mensajes a {i["group_id"]}</b> - <code>{i["group_name"]}</code>\nCausa: {error}', parse_mode="HTML")
                                resultado = False
                            if resultado:
                                await client.send_message("@spmmorgan7", f'<b>Mensaje enviado a {i["group_id"]}</b> - <code>{i["group_name"]}</code>', parse_mode="HTML")  
                            await asyncio.sleep(10)
                            if j == 4: break
            await client.send_message("@spmmorgan7", f'<b>RONDA ACABADA</b>', parse_mode="HTML")
            await asyncio.sleep(100) 
        except:
            pass

if __name__ == "__main__":
    asyncio.run(logUserBot())
