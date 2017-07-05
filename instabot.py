# Importing access token from keys.py
from keys import BASE_URL, ACCESS_TOKEN

# Importing requests for accessing and rendering web file
import requests

# Importing urllib for downloading photos
import urllib

# Importing textblob for sentiment analysis of comments
from textblob import TextBlob

from textblob.sentiments import NaiveBayesAnalyzer


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

        print 'Error :- %d' % str(my_info['meta']['code'])


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

        print 'Error :- %d' % my_info['meta']['code']


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

            print 'Username: %s' \
                  '' % (user_info['data']['username'])

            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])

            print 'No. of people %s is following: %s' % (insta_username, user_info['data']['counts']['follows'])

            print 'No. of posts: %s' % (user_info['data']['counts']['media'])

        else:

            print 'User asked for is purely fictional any connection to people living or dead is coincidental!'

    else:

        print 'Error :- %d' % user_info['meta']['code']


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

        print 'Error :- %d' % recent_posts['meta']['code']

    return None


# Getting the posts posted by user
def get_users_post(insta_username):
    user_id = get_user_id(insta_username)

    # Taking extra criteria to search for posts
    print 'Enter the post selection criteria : \n' \
          '1. Post with minimum likes.\n' \
          '2. Post with maximum likes.\n' \
          '3. Post with particular caption.\n' \
          '4. Most recent post.\n'

    media_choice = int(raw_input('Enter your choice : '))

    # Getting the users recent posts
    users_post = request_decode('/users/%s/media/recent?access_token=%s', [user_id, ACCESS_TOKEN])

    if media_choice == 1:

        # Setting like count to infinity so any likes would be less than this placeholder
        like_count = ''

        # Iterating through posts to search for index of least liked post
        for post in range(0, len(users_post['data'])):

            if users_post['data'][post]['likes']['count'] < like_count:
                like_count = users_post['data'][post]['likes']['count']

                post_index = post

        # Downloading and Getting the media_id of the least liked post
        media_id = download_user_post(users_post, post_index)

        return media_id

    elif media_choice == 2:

        # Setting like_count to -1 so any like is greater than placeholder
        like_count = -1

        # Iterating through posts for index of most liked recent post
        for post in range(0, len(users_post['data'])):

            if users_post['data'][post]['likes']['count'] > like_count:
                like_count = users_post['data'][post]['likes']['count']

                post_index = post

        # Downloading and Getting the media_id of the most liked post
        media_id = download_user_post(users_post, post_index)

        return media_id

    elif media_choice == 3:

        # Getting the caption text to search for
        caption = raw_input('Enter the caption text to search for : ')

        for post in range(0, len(users_post['data'])):

            caption_text = str(users_post['data'][post]['caption'])

            # Comparing the caption regardless of case
            if caption.lower() in caption_text.lower():
                post_index = post

        # Downloading and Getting the media_id of the required captioned post
        media_id = download_user_post(users_post, post_index)

        return media_id

    elif media_choice == 4:

        # Downloading and Getting the media_id of the most recent post at top position
        media_id = download_user_post(users_post, 0)

        return media_id

    else:

        print 'Wrong Choice'
        return None


# Method to download the post and return the media_id
def download_user_post(users_post, post_index):
    if users_post['meta']['code'] == 200:

        if len(users_post['data']):

            image_name = users_post['data'][post_index]['id'] + '.jpeg'

            image_url = users_post['data'][post_index]['images']['standard_resolution']['url']

            # Saving the image in the folder
            urllib.urlretrieve(image_url, image_name)

            return users_post['data'][post_index]['id']

        else:

            print 'There is no recent post!'

    else:

        print 'Error :- %d' %str(users_post['meta']['code'])

    return None


# Method to get recent image liked by self
def get_like_list():
    users_post = request_decode('/users/self/media/liked?access_token=%s', [ACCESS_TOKEN])

    if users_post['meta']['code'] == 200:
        if len(users_post['data']):

            image_name = users_post['data'][0]['id'] + '.jpeg'

            image_url = users_post['data'][0]['images']['standard_resolution']['url']

            # Downloading the image liked
            urllib.urlretrieve(image_url, image_name)

            return users_post['data'][0]['id']
        else:
            print 'There is no recent post!'
    else:
        print 'Error :-  %d' % str(users_post['meta']['code'])

    return None


# Method to like the recent post by a user
def like_a_post(insta_username):
    media_id = get_users_post(insta_username)

    # Payload for the post request
    payload = {'access_token': ACCESS_TOKEN}

    request_url = (BASE_URL + '/media/%s/likes') % (media_id)

    print 'POST request url : %s' % request_url

    # POSTing the request
    post_like = requests.post(request_url, payload).json()

    if post_like['meta']['code'] == 200:

        print 'Like was successful!'

    else:

        print 'Couldn\'t like the post! Please try again!'


# Method to get the list of comments
def get_comment_list(insta_username):
    media_id = get_users_post(insta_username)

    comments_info = request_decode('/media/%s/comments?access_token=%s', [media_id, ACCESS_TOKEN])

    if comments_info['meta']['code'] == 200:

        # Returning the comment_info in json format and the media id
        return comments_info, media_id

    else:

        print 'Error :- %d' % comments_info['meta']['code']


# Method to post a comment on the recent post by a user
def post_a_comment(insta_username):
    media_id = get_users_post(insta_username)

    comment = raw_input('Enter the comment for downloaded media with name and media_id :- %s.' % media_id)

    # Payload for POST request
    payload = {'access_token': ACCESS_TOKEN, 'text': comment}

    request_url = (BASE_URL + '/media/%s/comments') % media_id

    print 'POST request url : %s' % request_url

    post_comment = requests.post(request_url, payload).json()

    if post_comment['meta']['code'] == 200:

        print 'Your comment has been applied to the post'

    else:

        print 'Error :- %d' % post_comment['meta']['code']

        print '\n Try again later!'


# Method to simplify the DELETE request and returning the response in json format
def del_comments(del_url, del_params):
    del_url = del_url.split('%s')

    del_url.remove('')

    request_url = BASE_URL

    # Forming the request_url for DELETE request
    for part in range(0, len(del_url)):
        request_url += del_url[part] + del_params[part]

    print 'DELETE request url:' + request_url

    # Returning the DELETE request response
    return requests.delete(request_url).json()


#  Method to delete any negative comments or comment containing a particular word
def delete_negative_comment(insta_username):
    # Getting the comment info
    comments_info = get_comment_list(insta_username)

    # Getting the specified word for which to delete the comment
    word = raw_input('Enter the word which when present in a comment should lead to its deletion : ')

    if comments_info[0]['meta']['code'] == 200:

        if len(comments_info[0]['data']):

            # Iterating through the comments
            for comment in range(0, len(comments_info[0]['data'])):

                # Getting the comment text
                comment_text = comments_info[0]['data'][comment]['text']

                # If specified word is in the comment
                if word in comment_text.split():

                    comment_id = comments_info[0]['data'][comment]['id']

                    request_url = '/media/%s/comments/%s?access_token=%s'

                    del_params = [comments_info[1], comment_id, ACCESS_TOKEN]

                    # Sending the request url and parameters to the del_comment method
                    delete_comment = del_comments(request_url, del_params)

                    if delete_comment['meta']['code'] == 200:

                        print 'Comment with id %s deleted' % comment_id

                    else:

                        print 'Error : ' + delete_comment['meta']['code']
                        print 'Couldn\'t delete the comment! Please try again!'

                # If specified word is not in the comment then perform sentiment analysis
                else:

                    # Performing sentiment analysis
                    blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())

                    # Getting the negative sentiment bias
                    neg_sentiment = blob.sentiment.p_neg

                    # If negative bias is greater than 0.5 i.e more negative than positive
                    if neg_sentiment > 0.5:

                        # Delete the comment
                        comment_id = comments_info[0]['data'][comment]['id']

                        request_url = '/media/%s/comments/%s?access_token=%s'

                        del_params = [comments_info[1], comment_id, ACCESS_TOKEN]

                        delete_comment = del_comments(request_url, del_params)

                        if delete_comment['meta']['code'] == 200:

                            print 'Comment with id %s deleted' % comment_id

                        else:

                            print 'Error : %d' % delete_comment['meta']['code']
                            print 'Couldn\'t delete the comment! Please try again!'


        else:

            print 'There are no existing comments on the post!'

    else:

        print 'Error :- %d' % comments_info[0]['meta']['code']

        print '\n Try again later!'


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

        comments_info = get_comment_list(insta_username)

        # Iterating through the comments
        if len(comments_info[0]['data']) > 0:

            print 'For media id :' + comments_info[1]

            for comment in range(0, len(comments_info[0]['data'])):
                print str(comment + 1) + '. ' + comments_info[0]['data'][comment]['text']

        else:

            print 'No comments posted yet! Be the first to comment!'

    elif choice == 8:
        insta_username = raw_input('Please enter the instagram username :- ')
        post_a_comment(insta_username)

    elif choice == 9:
        insta_username = raw_input('Please enter the instagram username :- ')
        delete_negative_comment(insta_username)

    # Exit choice
    elif choice == 10:
        exit()

    else:
        print "wrong choice"
