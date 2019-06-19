import lemmy_api
import time
import json

# 3 actions per 3 minutes for register_new_user, post and community creation
# 30 actions per minute for everything else

class lemmy_test():
    def __init__(self):
        self.api = "ws://127.0.0.1:8536/api/v1/ws" # default; if the value is set in conf then that one is read
        #TODO: will not read api from conf for some reason, til it is fixed it must be changed here
        self.lemmy = lemmy_api.lemmy(self.api)
        self.log_file = None
        # admin conf settings
        self.create_admin = bool()
        self.admin_username = str()
        self.admin_password = str()
        self.auname_counter = int(0)
        # username conf settings
        self.username = str()
        self.password = str()
        self.uname_counter = int(0)
        # community and post titles
        self.community_name = str()
        self.post_title = str()
        self.community_counter = int(0)
        self.post_counter = int(0)
        # test options, read from conf
        self.run_general_expected_behavior_tests = bool()
        self.run_user_expected_behavior_tests = bool()
        self.run_mod_expected_behavior_tests = bool()
        self.run_admin_expected_behavior_tests = bool()
        # TODO: create additional tests
        self.run_general_optional_field_tests = bool()
        self.run_user_optional_field_tests = bool()
        self.run_mod_optional_field_tests = bool()
        self.run_admin_optional_field_tests = bool()
        self.run_general_bad_behavior_tests = bool()
        self.run_user_bad_behavior_tests = bool()
        self.run_mod_bad_behavior_tests = bool()
        self.run_admin_bad_behavior_tests = bool()

    # master function, this is the main function that is called
    def test_master(self):
        self.read_conf()
        #self.increment_username()
        #self.increment_admin_username()
        if self.run_general_expected_behavior_tests:
            self.general_functions_expected_behavior()
        if self.run_user_expected_behavior_tests:
            self.user_functions_expected_behavior()
        if self.run_mod_expected_behavior_tests:
            self.mod_functions_expected_behavior()
        if self.run_admin_expected_behavior_tests:
            self.admin_functions_expected_behavior()


    # GENERAL FUNCTIONS TEST. This function runs expected behavior tests for API calls that do not require auth.
    def general_functions_expected_behavior(self):
        self.logging(self.lemmy.list_categories())
        time.sleep(2)
        self.logging(self.lemmy.search("test", "Both", "Hot"))
        time.sleep(2)
        self.logging(self.lemmy.get_modlog())
        time.sleep(2)
        self.logging(self.lemmy.get_site())
        time.sleep(2)
        self.logging(self.lemmy.get_community(name="main"))
        time.sleep(2)
        self.logging(self.lemmy.list_communities(sort="Hot"))
        time.sleep(2)
        self.logging(self.lemmy.get_user_details("Hot", True, username="Admin01"))
        time.sleep(2)
        self.logging(self.lemmy.register_new_user(username=self.username, password=self.password, admin=False))
        #TODO: increment usernames, save usernames to list as they are created if needed
        #self.increment_username()
        time.sleep(20)
        self.logging(self.lemmy.get_posts(type_="All", sort="TopAll"))
        time.sleep(2)
        self.logging(self.lemmy.get_post(post_id=1)) # TODO: get post id from get_posts and use it here
        time.sleep(2)

    def user_functions_expected_behavior(self):
        response = self.lemmy.login(login=self.username, password=self.password)
        self.logging(response)
        auth = json.loads(response[1]).get('jwt')
        time.sleep(2)
        self.logging(self.lemmy.create_community(name=self.community_name, title="test community", category_id=1, auth=auth))
        time.sleep(20)
        self.logging(self.lemmy.get_inbox(sort="TopAll", auth=auth, unread_only=False))
        time.sleep(2)
        self.logging(self.lemmy.mark_all_read(auth=auth))
        response = self.lemmy.get_community(name=self.community_name)
        community_id = json.loads(response[1]).get('community').get('id')
        time.sleep(2)
        self.logging(self.lemmy.follow_community(community_id=community_id, follow=True, auth=auth))
        time.sleep(2)
        response = self.lemmy.create_post(name=self.post_title, community_id=community_id, auth=auth, body="test post")
        self.logging(response)
        post_id = json.loads(response[1]).get('post').get('id')
        post_creator_id = json.loads(response[1]).get('post').get('user_id')
        time.sleep(20)
        self.logging(self.lemmy.create_post_like(post_id=post_id, auth=auth, score=-1))
        time.sleep(2)
        self.logging(self.lemmy.edit_post(edit_id=post_id, creator_id=post_creator_id, community_id=community_id,
                                          name=str(self.post_title + "_edited"), auth=auth, body="test_post_edited"))
        time.sleep(2)
        self.logging(self.lemmy.save_post(post_id=post_id, save=True, auth=auth))
        time.sleep(2)
        response = self.lemmy.create_comment(content="test comment", post_id=post_id, auth=auth)
        self.logging(response)
        comment_id = json.loads(response[1]).get('comment').get('id')
        comment_creator_id = json.loads(response[1]).get('comment').get('user_id')
        time.sleep(2)
        self.logging(self.lemmy.edit_comment(content="test comment edited", edit_id=comment_id,
                                             creator_id=comment_creator_id, post_id=post_id, auth=auth))
        time.sleep(2)
        self.logging(self.lemmy.save_comment(comment_id=comment_id, save=True, auth=auth))
        time.sleep(2)
        self.logging(self.lemmy.create_comment_like(comment_id=comment_id, post_id=post_id, score=-1, auth=auth))
        time.sleep(2)


    def mod_functions_expected_behavior(self):
        pass

    def admin_functions_expected_behavior(self):
        pass

    def logging(self, log_info):
        timestamp = int(time.time())
        if self.log_file is None:
            #self.log_file = str(timestamp) + "_raw_log.txt"
            self.log_file = "raw_log.txt"
            log_file = open(self.log_file, "w")
        else:
            log_file = open(self.log_file, "a")
        if "{" not in log_info[1]:
            log_file.write("ERROR:\n")
        log_line =  str(timestamp) + ";" + str(log_info[0]) + ";" + str(log_info[1]) + "\n"
        log_file.write(log_line)
        print(log_line)

    def increment_username(self):
        self.username = str(self.username + str(self.uname_counter))
        self.uname_counter += 1

    def increment_admin_username(self):
        self.admin_username = str(self.admin_username + str(self.auname_counter))
        self.auname_counter += 1

    def increment_community_name(self):
        self.community_name = str(self.community_name + str(self.community_counter))
        self.community_counter += 1

    def increment_post_title(self):
        self.post_title = str(self.post_title + str(self.post_counter))
        self.post_counter += 1

    def read_conf(self):
        conf = open("conf.conf")
        conf_data = conf.readlines()
        for line in conf_data:
            if line[0] == "#":
                pass
            elif line == "\n":
                pass
            else:
                line = line.split(" = ")
                line[1] = line[1].replace("\n","")
                if line[0] == "server":
                    self.api = str(line[1])
                    #TODO: what on earth is going on with the url string from the conf?
                elif line[0] == "create_admin":
                    self.create_admin = line[1]
                elif line[0] == "admin_username":
                    self.admin_username = line[1]
                elif line[0] == "admin_password":
                    self.admin_password = line[1]
                elif line[0] == "username":
                    self.username = line[1]
                elif line[0] == "password":
                    self.password = line[1]
                elif line[0] == "community_name":
                    self.community_name = line[1]
                elif line[0] == "post_title":
                    self.post_title = line[1]
                elif line[0] == "run_general_expected_behavior_tests":
                    self.run_general_expected_behavior_tests = self.str_to_bool(line[1])
                elif line[0] == "run_user_expected_behavior_tests":
                    self.run_user_expected_behavior_tests = self.str_to_bool(line[1])
                elif line[0] == "run_mod_expected_behavior_tests":
                    self.run_mod_expected_behavior_tests = self.str_to_bool(line[1])
                elif line[0] == "run_admin_expected_behavior_tests":
                    self.run_admin_expected_behavior_tests = self.str_to_bool(line[1])
                elif line[0] == "run_general_optional_field_tests":
                    self.run_general_optional_field_tests = self.str_to_bool(line[1])
                elif line[0] == "run_user_optional_field_tests":
                    self.run_user_optional_field_tests = self.str_to_bool(line[1])
                elif line[0] == "run_mod_optional_field_tests":
                    self.run_mod_optional_field_tests = self.str_to_bool(line[1])
                elif line[0] == "run_admin_optional_field_tests":
                    self.run_admin_optional_field_tests = self.str_to_bool(line[1])
                elif line[0] == "run_general_bad_behavior_tests":
                    self.run_general_bad_behavior_tests = self.str_to_bool(line[1])
                elif line[0] == "run_user_bad_behavior_tests":
                    self.run_user_bad_behavior_tests = self.str_to_bool(line[1])
                elif line[0] == "run_mod_bad_behavior_tests":
                    self.run_mod_bad_behavior_tests = self.str_to_bool(line[1])
                elif line[0] == "run_admin_bad_behavior_tests":
                    self.run_admin_bad_behavior_tests = self.str_to_bool(line[1])
                else:
                    self.logging("unknown line in conf:" + str(line))
        conf.close()

    def str_to_bool(self, string):
        if string == "True": return True
        else: return False

if __name__ == '__main__':
    lemmy_test().test_master()

