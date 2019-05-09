#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Vk.py
# (c) Oleg Plaxin 2019
# plaxoleg@gmail.com

# -*- coding: utf-8 -*-
import vk_api

from Utils.ConfigWorker import Config
from Utils.Log import Log
from vk_api.utils import get_random_id

from urlextract import URLExtract


class VK:
    def __init__(self):

        log_tag = 'VK - init'
        self.settings_tag = 'VK'

        self.extractor = URLExtract()
        self.config = Config()
        try:
            self.vk_bot = vk_api.VkApi(token=str(self.config.read(self.settings_tag, 'bot_token')))
            self.api_bot_vk = self.vk_bot.get_api()
            Log().info(log_tag, 'Инициализация токена-бота VK успешна.')
        except Exception as e:
            Log().error(log_tag, e)

        p_name = 'ЛИНКЕР'
        p_channel = 'hackathon'
        p_version = '0.0.1'
        desc = 'Бот, создающий сокращенные vk.cc ссылки прямо в диалоге.'
        self.info = f'{p_name} {p_version} ({p_channel})\n\n{desc}\n\nбеседа %peer_id%'

    def long_poll(self):
        tag = 'VK - Message LongPoll'
        from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

        long_poll_bot = VkBotLongPoll(self.vk_bot, int(self.config.read(self.settings_tag, "community_id")))

        for event in long_poll_bot.listen():
            try:
                if event.type == VkBotEventType.MESSAGE_NEW:
                    Log().info(tag, f'Новое сообщение от \"https://vk.com/id{event.obj.from_id}\".\n'
                                    f'Текст сообщения:\t\n{event.obj.text}\n'
                                    f'Прикрепленные аттачи:\t\n{event.obj.attachments}\n'
                                    f'Пересланные сообщения:\t\n{event.obj.fwd_messages}')
                    self.listener(event)

                elif event.type == VkBotEventType.MESSAGE_REPLY:
                    Log().info(tag, f'Бот ответил в чате {event.obj.peer_id}.')

                else:
                    Log().info(tag, f'Обнаружено новое действие: {event.type} от '
                                    f'\"https://vk.com/id{event.obj.from_id}\"')

            except Exception as e:
                Log().error(tag, e)

    def listener(self, event):
        tag = "VK - Message Listener"
        Log().info(tag, 'Обрабатываю сообщение...')
        from_id = event.obj.from_id
        peer_id = event.obj.peer_id
        msg_text = str(event.obj.text)
        msg_attach = event.obj.attachments
        msg_fwd = event.obj.fwd_messages
        Log().info(tag, 'Обработка завершена. ')

        if self.extractor.has_urls(msg_text) or msg_attach or msg_fwd:
            response_links = []
            if self.extractor.has_urls(msg_text):
                links = self.extractor.find_urls(msg_text)
                Log().info(tag, 'Найдены объекты типа ссылка.')
                if len(links) > 1:
                    for i in range(len(links)):
                        response_links.append(self.get_cc_link(links[i], 0)['short_url'])
                else:
                    response_links.append(self.get_cc_link(links, 0)['short_url'])

            if msg_attach:
                for i in range(len(msg_attach)):
                    attach_type = msg_attach[i]['type']
                    if attach_type == 'link':
                        ath_url = msg_attach[i][attach_type]['url']
                        response_links.append(str(self.get_cc_link(ath_url, 0)['short_url']))

            if msg_fwd:
                for i_fwd in range(len(msg_fwd)):
                    fwd_text = msg_fwd[i_fwd]['text']
                    fwd_attaches = msg_fwd[i_fwd]['attachments']
                    for i_ath in range(len(fwd_attaches)):
                        fwd_ath_type = fwd_attaches[i_ath]['type']
                        if fwd_ath_type == 'link':
                            fwd_ath_link = msg_fwd[i_fwd]['attachments'][i_ath][fwd_ath_type]['url']
                            response_links.append(str(self.get_cc_link(fwd_ath_link, 0)['short_url']))

                    if self.extractor.find_urls(fwd_text):
                        response_links.append(str(self.get_cc_link(fwd_text, 0)['short_url']))

            response_links_wd = list(dict.fromkeys(response_links))

            if len(response_links_wd) > 1:
                response_str = 'Вот твои ссылки из сообщения:\n\n'
                for i_link in range(len(response_links_wd)):
                    response_str += response_links_wd[i_link] + '\n'

            else:
                response_str = 'Была найдена лишь одна ссылка в сообщении: ' + response_links_wd[0]

            self.send_message(peer_id, response_str)

        elif (from_id == 140830142) and \
                (msg_text.__contains__('info') or msg_text.__contains__('инфо') or msg_text.__contains__('i')) or \
                (msg_text.__contains__('ping') or msg_text.__contains__('пинг')):
            Log().info(tag, 'Инфо о боте.')
            self.send_message(peer_id, 'понг')
            self.send_message(peer_id, self.info.replace("%peer_id%", str(peer_id)))

        else:
            Log().info(tag, 'Неизвестная команда.')
            self.send_message(event.obj.peer_id, 'Неизвестная команда.')

    def get_cc_link(self, url, private):
        cc_link = self.api_bot_vk.utils.getShortLink(
            url=url,
            private=private
        )
        return cc_link

    def send_message(self, user_id, text):
        self.api_bot_vk.messages.send(peer_id=user_id, message=text, random_id=get_random_id(), dont_parse_links=1)
