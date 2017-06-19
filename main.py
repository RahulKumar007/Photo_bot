from keys import base_url, ACCESS_TOKEN

import requests

import urllib

def request_decode(url, get_params):
    url = url.split('%s')

    url.remove('')

    request_url = base_url

    for part in range(0, len(url)):
        request_url += url[part] + get_params[part]

    print 'Requesting info for:' + request_url

    info = requests.get(request_url).json()

    return info


def self_info():
    get_url = '/users/self/?ACCESS_TOKEN=%s'

    get_params = [ACCESS_TOKEN]

    my_info = request_decode(get_url, get_params)

    if my_info['meta']['code'] == 200:

        if len(my_info['data']):

            print 'Username: %s' % (my_info['data']['username'])

            print 'No. of followers: %s' % (my_info['data']['counts']['followed_by'])

            print 'No. of people you are following: %s' % (my_info['data']['counts']['follows'])

            print 'No. of posts: %s' % (my_info['data']['counts']['media'])

        else:

            print 'User asked for is purely fictional any connection to people living or dead is coincidental!'

    else:

        print 'Status code other than 200 received!'


def get_user_id(insta_username):
    """request_url = (base_url + '/users/search?q=%s&ACCESS_TOKEN=%s') % (insta_username, ACCESS_TOKEN)
  
    print 'Requesting info for:' + request_url
  
    requests.get(request_url).json()
  
    """
    get_url = '/users/search?q=%s&ACCESS_TOKEN=%s'

    get_params = [insta_username, ACCESS_TOKEN]

    my_info = request_decode(get_url, get_params)

    print 'User id is:\n', my_info['data'][0]['id']

    return my_info['data'][0]['id']


def get_own_post():
    recent_posts = request_decode('/users/self/media/recent?access_token=%s', [ACCESS_TOKEN])

    if recent_posts['meta']['code'] == 200:
        if len(recent_posts['data']):

            image_name = recent_posts['data'][0]['id'] + ".jpeg"
            image_url = recent_posts['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, 'output.jpg')

            return recent_posts['data'][0]['id']
        else:
            print "There is no recent post!"
    else:
        print "Status code other than 200 received!"

    return None


def get_users_post():
    user_id = get_user_id(insta_username)

    users_post = request_decode('/users/%s/media/recent?ACCESS_TOKEN=%s', [user_id, ACCESS_TOKEN])

    print users_post


get_own_post()
# self_info()
insta_username = raw_input("Please enter your instagram username :- \n")
# get_users_post()
# user_id = get_user_id(insta_username)
