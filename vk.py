import requests
import logging
import time


class VkApi():
    def __init__(self):
        self._VK_TOKEN = '###'  # токен авторизации запросов
        self.vk_v = 5.52  # версия api вк
        self.url = 'https://api.vk.com/method/'  # url api
        self.params = {'access_token': self._VK_TOKEN, 'v': self.vk_v}  # основные параметры при запросе
        self.user = 169002303  # Мой юзер в вк Анвар Хамидов


    def get_online_info_users(self):  # функция для получения информации о пользователях
        online_users_list = requests.get(self.url + 'friends.getOnline', params=self.params).json()['response']
        users_info = requests.get(self.url + 'users.get', params={**self.params, 'user_ids': str(online_users_list), 'fields': 'photo_max_orig,city,verified'}).json()
        return users_info

    def delete_groups(self):
        groups = requests.get(self.url + 'groups.get', params=self.params).json()['response']['items'] # Получаю все мои группы  
        for group in groups:  # Проверяю каждую группа, если мне недоступны данные руководителей то выхожу из группы
            managers = self.get_members_group(group) 
            if 'error' in managers:
                response = self.leave_group(group)
                if response['response'] == 1:
                    continue
            else:
                continue
            time.sleep(0.5)  # Поставил тайм-аут для запросов,так как блокирует мои запросы


    def get_members_group(self, group):  # Получаем из группы менеджеров, то есть тех кто руководит
        members = requests.get(self.url + 'groups.getMembers', params={**self.params, 'filter': 'managers', 'group_id': str(group)}, timeout=10).json()
        return members

    def leave_group(self, group):  # выходим из группы
        response = requests.post(self.url + 'groups.leave', params={**self.params, 'group_id': group}).json()
        return response