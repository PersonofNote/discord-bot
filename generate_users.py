import requests
import json
default_avatars = ['https://i.picsum.photos/id/583/200/300.jpg?hmac=W0K2Agq4NPD6kuihywmxQfaEbIE56uEJiTl97EfK8k8', 'https://i.picsum.photos/id/507/200/300.jpg?hmac=v0NKvUrOWTKZuZFmMlLN_7-RdRgeF-qFLeBGXpufxgg', 'https://i.picsum.photos/id/822/200/300.jpg?hmac=L4-fkLPiZOUXQokdDk0s2gcjb6w_zq1DGU7WybDqrj0', 'https://i.picsum.photos/id/1081/200/300.jpg?hmac=ntCnXquH7cpEF0vi5yvz1wKAlRyd2EZwZJQbgtfknu8']
['https://i.picsum.photos/id/583/200/300.jpg?hmac=W0K2Agq4NPD6kuihywmxQfaEbIE56uEJiTl97EfK8k8', 'https://i.picsum.photos/id/507/200/300.jpg?hmac=v0NKvUrOWTKZuZFmMlLN_7-RdRgeF-qFLeBGXpufxgg', 'https://i.picsum.photos/id/822/200/300.jpg?hmac=L4-fkLPiZOUXQokdDk0s2gcjb6w_zq1DGU7WybDqrj0', 'https://i.picsum.photos/id/1081/200/300.jpg?hmac=ntCnXquH7cpEF0vi5yvz1wKAlRyd2EZwZJQbgtfknu8']

default_usernames = ['user1', 'user2', 'user3', 'user4', 'user5']

default_text = ["Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.", "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.", "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."]

def generate_avatars(num):
    avatar_list = []
    for x in range(1, num):
        r = requests.get('https://picsum.photos/200/300')
        print(r.url)
        avatar_list.append(r.url)
    return avatar_list

def generate_users(num, usernames, avatar_list):
    # TODO: randomify this, too
    user_list = []
    for x in usernames:
        #user = discord.User(name=x, avatar=avatar_list[x])
        user = {'name': x, 'avatar': avatar_list[x]}
        user_list.append(user)
    return user_list
