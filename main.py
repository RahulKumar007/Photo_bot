# Importing access token from keys.py
from keys import BASE_URL, ACCESS_TOKEN

# Importing requests for accessing and rendering web file
import requests

# Importing urllib for downloading photos
import urllib


# A function to simplify creating the get request url and getting the request
def request_decode(url, get_params):
    url = url.split('%s')

    url.remove('')

    request_url = BASE_URL

    for part in range(0, len(url)):
        request_url += url[part] + get_params[part]

    print 'GET request url:' + request_url

    return requests.get(request_url).json()


# Method to get self info like followers, following, posts and name
def self_info():
    get_url = '/users/self/?access_token=%s'

    get_params = [ACCESS_TOKEN]

    my_info = request_decode(get_url, get_params)

    # Checking if meta code is 200 which basically means everything is fine
    if my_info['meta']['code'] == 200:

        # Checking if there actually is anything in the data. It might be empty.
        if len(my_info['data']):

            print 'Username: %s' % (my_info['data']['username'])

            print 'No. of followers: %s' % (my_info['data']['counts']['followed_by'])

            print 'No. of people you are following: %s' % (my_info['data']['counts']['follows'])

            print 'No. of posts: %s' % (my_info['data']['counts']['media'])

        else:

            print 'User asked for is purely fictional any connection to people living or dead is coincidental!'

    else:

        print 'Error :- ' + str(my_info['meta']['code'])


# Method to get user_id based on user_name
def get_user_id(insta_username):
    get_url = '/users/search?q=%s&access_token=%s'

    get_params = [insta_username, ACCESS_TOKEN]

    my_info = request_decode(get_url, get_params)

    if my_info['meta']['code'] == 200:

        if len(my_info['data']):

            return my_info['data'][0]['id']

        else:

            print 'No data present! User might have a private account.'

    else:

        print 'Error :- ' + my_info['meta']['code']


# Getting the info of a user using username
def get_user_info(insta_username):
    get_url = '/users/%s/?access_token=%s'

    user_id = get_user_id(insta_username)

    get_params = [user_id, ACCESS_TOKEN]

    user_info = request_decode(get_url, get_params)

    # Checking if meta code is 200 which basically means everything is fine
    if user_info['meta']['code'] == 200:

        # Checking if there actually is anything in the data. It might be empty.
        if len(user_info['data']):

            print 'Username: %s' % (user_info['data']['username'])

            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])

            print 'No. of people %s is following: %s' % (insta_username, user_info['data']['counts']['follows'])

            print 'No. of posts: %s' % (user_info['data']['counts']['media'])

        else:

            print 'User asked for is purely fictional any connection to people living or dead is coincidental!'

    else:

        print 'Error :- ' + user_info['meta']['code']


# Getting the posts posted by self
def get_own_post():
    recent_posts = request_decode('/users/self/media/recent?access_token=%s', [ACCESS_TOKEN])

    if recent_posts['meta']['code'] == 200:

        if len(recent_posts['data']):

            image_name = recent_posts['data'][0]['id'] + '.jpeg'

            image_url = recent_posts['data'][0]['images']['standard_resolution']['url']

            # Saving the image posted
            urllib.urlretrieve(image_url, image_name)

            # Returning post id
            return recent_posts['data'][0]['id']

        else:

            print 'There are no recent posts!'
    else:

        print 'Error :- ' + recent_posts['meta']['code']

    return None


def get_users_post(insta_username):
    user_id = get_user_id(insta_username)

    users_post = request_decode('/users/%s/media/recent?access_token=%s', [user_id, ACCESS_TOKEN])

    if users_post['meta']['code'] == 200:
        if len(users_post['data']):

            image_name = users_post['data'][0]['id'] + '.jpeg'
            image_url = users_post['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)

            return users_post['data'][0]['id']
        else:
            print 'There is no recent post!'
    else:
        print 'Error :- ' + str(users_post['meta']['code'])

    return None


def get_like_list():
    users_post = request_decode('/users/self/media/liked?access_token=%s', [ACCESS_TOKEN])

    if users_post['meta']['code'] == 200:
        if len(users_post['data']):

            image_name = users_post['data'][0]['id'] + '.jpeg'
            image_url = users_post['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)

            return users_post['data'][0]['id']
        else:
            print 'There is no recent post!'
    else:
        print 'Error :- ' + str(users_post['meta']['code'])

    return None


def like_a_post(insta_username):
    media_id = get_users_post(insta_username)

    payload = {'access_token': ACCESS_TOKEN}

    request_url = (BASE_URL + '/media/%s/likes') % (media_id)

    print 'POST request url : %s' %request_url

    post_like = requests.post(request_url, payload).json()

    if post_like['meta']['code'] == 200:

        print 'Like was successful!'

    else:

        print 'Couldn\'t like the post! Please try again!'

def get_comment_list(insta_username):

    media_id = get_users_post(insta_username)

    comments_info = request_decode('/media/%s/comments?access_token=%s', [media_id, ACCESS_TOKEN])

    comments_list = []

    for comment in range(0, len(comments_info['data'])):

        comments_list.append(comments_info['data'][comment]['text'])

        print str(comment+1) + '. ' + comments_list[comment]



print 'Welcome to PhotoBot!\nWe provide some cool Instagram functionalities! '

while True:

    print 'The menu options are :-\n' \
          '1. Get your own details.\n' \
          '2. Get details of a user using username.\n' \
          '3. Get your recent posts.\n' \
          '4. Get recent posts of a user using username.\n' \
          '5. Get the recent media liked by the user.\n' \
          '6. Like the recent post of a user.\n' \
          '7. Get the list of comments on the recent post of a user.\n' \
          '8. Post a comment on the recent post of a user.\n' \
          '9. Delete negative comments from recent post of a user.\n' \
          '10. Exit.\n'

    choice = int(raw_input('Enter your choice :- '))

    if choice == 1:
        self_info()
    elif choice == 2:
        insta_username = raw_input('Please enter the instagram username :- ')
        get_user_info(insta_username)
    elif choice == 3:
        post_id = get_own_post()
        print 'Recent post with id: %s has been downloaded.' % post_id
    elif choice == 4:
        insta_username = raw_input('Please enter the instagram username :- ')
        post_id = get_users_post(insta_username)
        print 'Recent post by %s with id: %s has been downloaded.' % (insta_username, post_id)
    elif choice == 5:
        post_id = get_like_list()
        print 'Recent liked post with id: %s has been downloaded.' % post_id
    elif choice == 6:
        insta_username = raw_input('Please enter the instagram username :- ')
        like_a_post(insta_username)
    elif choice == 7:
        insta_username = raw_input('Please enter the instagram username :- ')
        get_comment_list(insta_username)
    elif choice == 8:
        insta_username = raw_input('Please enter the instagram username :- ')
        post_a_comment(insta_username)
    elif choice == 9:
        insta_username = raw_input('Please enter the instagram username :- ')
        delete_negative_comment(insta_username)
    elif choice == 10:
        exit()
    else:
        print "wrong choice"
