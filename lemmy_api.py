from websocket import create_connection

"""
This is an API middle layer library for Lemmy. Each function can be called with the required and optional data needed to
be sent and the instance API provided. Each function inserts that data into the correct place in the JSON string 
required by the API. Since they are just strings, they are constructed in each function to reduce dependencies. Lemmy 
uses a websockets API. This code can be used for any Python3 application that needs to connect to Lemmy. All this
library does is return the response from the API in JSON format, it does absolutely no parsing of the returned data. 
See https://github.com/dessalines/lemmy/blob/master/docs/api.md for API documentation.
"""

class lemmy():
    def __init__(self, api):
        self.api = api

    # main connection handler.
    # All API functions call this function to connect, send request, receive response and disconnect.
    def quick_connect(self, request_string):
        connection = create_connection(self.api)
        connection.send(request_string)
        response = connection.recv()
        connection.close()
        return response

    # ADMIN FUNCTIONS. Only instance admins will get a useful response.
    def add_admin(self, user_id, added, auth):
        request_string = '{"op": "AddAdmin", "data": {"user_id": %d, "added": %d, "auth": "%s"' \
                         '}}' % (user_id, added, auth)
        return [request_string, self.quick_connect(request_string)]

    def create_site(self, name, description, auth):
        request_string = '{"op": "CreateSite", "data": {"name": "%s", "description": "%s", "auth": "%s"' \
                         '}}' % (name, description, auth)
        return [request_string, self.quick_connect(request_string)]

    def edit_site(self, name, auth, description=None):
        request_string = '{"op": "EditSite", "data": {"name": "%s", "auth": "%s"' % (name, auth)
        if description is not None: request_string += ', "description": "%s"' % description
        request_string += '}}'
        return [request_string, self.quick_connect(request_string)]

    def ban_user(self, user_id, ban, auth, reason=None, expires=None):
        request_string = '{"op": "BanUser", "data": {"user_id": %d, "ban": %s, "auth": "%s"' % (user_id, ban, auth)
        if reason is not None: request_string += ', "reason": "%s"' % reason
        if expires is not None: request_string += ', "expires": %d' % expires
        request_string += '}}'
        return [request_string, self.quick_connect(request_string)]

    # MOD FUNCTIONS. Only community moderators or instance admins will get a useful response.
    def ban_from_community(self, community_id, user_id, ban, auth, reason=None, expires=None):
        request_string = '{"op": "BanFromCommunity", "data": {"community_id": %d, "user_id": %d, "ban": %s, ' \
                         '"auth": "%s"' % (community_id, user_id, ban, auth)
        if reason is not None: request_string += ', "reason": "%s"'
        if expires is not None: request_string += ', "expires": %d'
        request_string += '}}'
        return [request_string, self.quick_connect(request_string)]

    def add_mod(self, community_id, user_id, added, auth):
        request_string = '{"op": "AddModToCommunity", "data": {"community_id": %d, "user_id": %d, "added": %s, ' \
                         '"auth": "%s"}}' % (community_id, user_id, added, auth)
        return [request_string, self.quick_connect(request_string)]

    def edit_community(self, edit_id, name, title, auth, category_id, description=None, removed=None, deleted=None,
                       reason=None, expires=None):
        request_string = '{"op": "EditCommunity", "data": {"edit_id": %d, "name": "%s", "title": "%s", ' \
                         '"category_id": %d, "auth": "%s"' % (edit_id, name, title, category_id, auth)
        if description is not None: request_string += ', "description": "%s"' % description
        if removed is not None: request_string += ', "removed": %s' % removed
        if deleted is not None: request_string += ', "deleted": %s' % deleted
        if reason is not None: request_string += ', "reason": "%s"'
        if expires is not None: request_string += ', "expires": %d'
        request_string += '}}'
        return [request_string, self.quick_connect(request_string)]

    # GENERAL FUNCTIONS. These functions perform general behavior, anyone can call these functions.
    def list_categories(self):
        request_string = '{"op": "ListCategories"}'
        return [request_string, self.quick_connect(request_string)]

    def search(self, query, type_, sort, community_id=None, page=None, limit=None):
        request_string = '{"op": "Search", "data": {"q": "%s", "type_": "%s", "sort": "%s"' % (query, type_, sort)
        if community_id is not None: request_string += ', "community_id": %d' % community_id
        if page is not None: request_string += ', "page": %d' % page
        if limit is not None: request_string += ', "limit": %d' % limit
        request_string += '}}'
        return [request_string, self.quick_connect(request_string)]

    def get_modlog(self, mod_user_id=None, community_id=None, page=None, limit=None):
        request_string = '{"op": "GetModlog", "data": {'
        if mod_user_id is not None: request_string += ', "mod_user_id": %d' % mod_user_id
        if community_id is not None: request_string += ', "community_id": %d' % community_id
        if page is not None: request_string += ', "page": %d' % page
        if page is not None: request_string += ', "limit": %d' % limit
        request_string += '}}'
        return [request_string, self.quick_connect(request_string)]

    def get_site(self):
        request_string = '{"op": "GetSite"}'
        return [request_string, self.quick_connect(request_string)]

    def get_community(self, community_id=None, name=None, auth=None):
        request_string = '{"op": "GetCommunity", "data": {'
        if community_id is not None: request_string += '"id": %d, ' % community_id
        if name is not None: request_string += '"name": "%s"' % name
        if auth is not None: request_string += ', "auth": "%s"' % auth
        request_string += '}}'
        return [request_string, self.quick_connect(request_string)]

    def list_communities(self, sort, page=None, limit=None, auth=None):
        request_string = '{"op": "ListCommunities", "data": {"sort": "%s"' % sort
        if page is not None: request_string += ', "page": %d' % page
        if limit is not None: request_string += ', "limit": %d' % limit
        if auth is not None: request_string += ', "auth": "%s"' % auth
        request_string += '}}'
        return [request_string, self.quick_connect(request_string)]

    def get_user_details(self, sort, saved_only, user_id=None, username=None, page=None, limit=None,
                         community_id=None, auth=None):
        request_string = '{"op": "GetUserDetails", "data": {"sort": "%s", "saved_only":  %s' % (sort, saved_only)
        if user_id is not None: request_string += ', "user_id": %d' % user_id
        if username is not None: request_string += ', "username": "%s"' % username
        if page is not None: request_string += ', "page": %d' % page
        if limit is not None: request_string += ', "limit": %d' % limit
        if community_id is not None: request_string += ', "community_id": %d' % community_id
        if auth is not None: request_string += ', "auth": "%s"' % auth
        request_string += '}}'
        return [request_string, self.quick_connect(request_string)]

    def register_new_user(self, username, password, email=None, admin=None):
        request_string = '{"op": "Register", "data": { "username": "%s", "password": "%s", ' \
                         '"password_verify": "%s"' % (username, password, password)
        if email is not None: request_string += ', "email": "%s"' % email
        if admin is not None: request_string += ', "admin": %s' % admin
        request_string += '}}'
        return [request_string, self.quick_connect(request_string)]

    def get_posts(self, type_, sort, page=None, limit=None, community_id=None, auth=None):
        # Get multiple posts from community ID
        request_string = '{"op": "GetPosts", "data": {"type_": "%s", "sort": "%s"' % (type_, sort)
        if page is not None: request_string += ', "page": %d' % page
        if limit is not None: request_string += ', "limit": %d' % limit
        if community_id is not None: request_string += ', "community_id": %d' % community_id
        if auth is not None: request_string += ', "auth": "%s"' % auth
        request_string += '}}'
        return [request_string, self.quick_connect(request_string)]

    def get_post(self, post_id, auth=None):
        # Get single post from post ID
        request_string = '{"op": "GetPost", "data": {"id": %d' % post_id
        if auth is not None: request_string += ', "auth": "%s"' % auth
        request_string += '}}'
        return [request_string, self.quick_connect(request_string)]

    # USER FUNCTIONS. General behavior from users only. Only registered users will get a valid response.
    def login(self, login, password):
        # "login" must be username or email address
        request_string = '{"op": "Login", "data": {"username_or_email": "%s", "password": "%s"}}' % (login, password)
        return [request_string, self.quick_connect(request_string)]

    def create_community(self, name,title, category_id, auth, description=None):
        request_string = '{"op": "CreateCommunity", "data": {"name": "%s", "title": "%s", ' \
                         '"category_id": %d, "auth": "%s"' % (name, title, category_id, auth)
        if description is not None: request_string += ', "description": "%s"' % description
        request_string += '}}'
        return [request_string, self.quick_connect(request_string)]

    def get_inbox(self, sort, auth, unread_only, page=None, limit=None):
        request_string = '{"op": "GetReplies", "data": ("sort": "%s", "unread_only": %s, ' \
                         '"auth": "%s"' % (sort, unread_only, auth)
        if page is not None: request_string += ', "page": %d' % page
        if limit is not None: request_string += ', "limit": %d' % limit
        request_string += '}}'
        return [request_string, self.quick_connect(request_string)]

    def mark_all_read(self, auth):
        request_string = '{"op": "MarkAllAsRead", "data": {"auth": "%s"}}' % auth
        return [request_string, self.quick_connect(request_string)]

    def follow_community(self, community_id, follow, auth):
        request_string = '{"op": "FollowCommunity", "data": {"community_id": %d, "follow": %s, "auth": "%s"' \
                         '}}' % (community_id, follow, auth)
        return [request_string, self.quick_connect(request_string)]

    def create_post(self, name, community_id, auth, url=None, body=None):
        request_string = '{"op": "CreatePost", "data": {"name": "%s", "community_id": %d, ' \
                         '"auth": "%s"}}' % (name, community_id, auth)
        if url is not None: request_string += ', "url": "%s"' % url
        if body is not None: request_string += ', "body": "%s"' % body
        request_string += '}}'
        return [request_string, self.quick_connect(request_string)]

    def create_post_like(self, post_id, score, auth):
        # "score" cannot be any value greater than 1 or any value lower than -1
        # that is, -1,0,1 are the only valid values
        request_string = '{"op": "CreatePostLike", "data": {"post_id": %d, "score": %d, "auth": "%s"' \
                         '}}' % (post_id, score, auth)
        return [request_string, self.quick_connect(request_string)]

    def edit_post(self, edit_id, creator_id, community_id, name, auth, url=None, body=None, removed=None, deleted=None,
                  locked=None, reason=None):
        # using the "removed" or "locked" and "reason" values will not have an effect for regular users
        # Only mods and admins can use those. Users should use "deleted" instead.
        request_string = '{"op": "EditPost", "data": {"edit_id": %d, "creator_id": %d, "community_id": %d, ' \
                         '"name": "%s", "auth": "%s"' % (edit_id, creator_id, community_id, name, auth)
        if url is not None: request_string += ', "url": "%s"' % url
        if body is not None: request_string += ', "body": "%s"' % body
        if removed is not None: request_string += ', "removed": %s' % removed
        if deleted is not None: request_string += ', "deleted": %s' % deleted
        if locked is not None: request_string += ', "locked": %s' % locked
        if reason is not None: request_string += ', "reason": "%s"' % reason
        request_string += '}}'
        return [request_string, self.quick_connect(request_string)]

    def save_post(self, post_id, save, auth):
        request_string = '{"op": "SavePost", "data": {"post_id": %d, "save": %s, "auth": "%s"' \
                         '}}' % (post_id, save, auth)
        return [request_string, self.quick_connect(request_string)]

    def create_comment(self, content, post_id, auth, parent_id=None, edit_id=None):
        request_string = '{"op": "CreateComment", "data": {"content": "%s", "post_id": %d, ' \
                         '"auth": "%s"}}' % (content, post_id, auth)
        if parent_id is not None: request_string += ', "parent_id": %d' % parent_id
        if edit_id is not None: request_string += ', "edit_id": %d' % edit_id
        request_string += '}}'
        return [request_string, self.quick_connect(request_string)]

    def edit_comment(self, content, edit_id, creator_id, post_id, auth, parent_id=None, removed=None, deleted=None,
                     reason=None, read=None):
        # using the "removed" and "reason" values will not have an effect for regular users
        # Only mods and admins can use those. Users should use "deleted" instead.
        request_string = '{"op": "EditComment", "data": {"content": "%s", "edit_id": %d, "creator_id": %d, ' \
                         '"post_id": %d, "auth": "%s"' % (content, edit_id, creator_id, post_id, auth)
        if parent_id is not None: request_string += ', "parent_id": %d' % parent_id
        if removed is not None: request_string += ', "removed": %s' % removed
        if deleted is not None: request_string += ', "deleted": %s' % deleted
        if reason is not None: request_string += ', "reason": "%s"' % reason
        if read is not None: request_string += ', "read": %s' % read
        request_string += '}}'
        return [request_string, self.quick_connect(request_string)]

    def save_comment(self, comment_id, save, auth):
        request_string = '{"op": "SaveComment", "data": {"comment_id": %d, "save": %s, "auth": "%s"' \
                        '}}' % (comment_id, save, auth)
        return [request_string, self.quick_connect(request_string)]

    def create_comment_like(self, comment_id, post_id, score, auth):
        # "score" cannot be any value greater than 1 or any value lower than -1
        # that is, -1,0,1 are the only valid values
        request_string = '{"op": "CreateCommentLike", "data": {"comment_id": %d, "post_id": %d, "score": %d, ' \
                         '"auth": "%s"}}' % (comment_id, post_id, score, auth)
        return [request_string, self.quick_connect(request_string)]

