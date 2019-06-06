import lemmy_api
import time
import json

# 3 actions per 3 minutes for register_new_user, post and community creation
# 30 actions per minute for everything else

class lemmy_test():
    def __init__(self):
        self.api = "wss://dev.lemmy.ml/api/v1/ws"  # default; if the value is set in conf then that one is read
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
        if self.run_general_expected_behavior_tests:
            #self.logging("{Running general functions expected behavior tests...}")
            self.general_functions_expected_behavior()
        if self.run_user_expected_behavior_tests:
            #self.logging("{Running user functions expected behavior tests...}")
            self.user_functions_expected_behavior()


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
        self.logging(self.lemmy.get_user_details("Hot", True, username="dessalines"))
        time.sleep(2)
        #self.logging(self.lemmy.register_new_user(username=self.username, password=self.password))
        #self.increment_username()
        #time.sleep(20)
        self.logging(self.lemmy.get_posts(type_="All", sort="All"))
        time.sleep(2)
        self.logging(self.lemmy.get_post(post_id=1)) # TODO: get post id from get_posts and use it here
        time.sleep(2)

    def user_functions_expected_behavior(self):
        self.logging(self.lemmy.login(login=self.username, password=self.password))
        time.sleep(2)



    def logging(self, log_info):
        timestamp = int(time.time())
        if self.log_file is None:
            #self.log_file = str(timestamp) + "_raw_log.txt"
            self.log_file = "raw_log.txt"
            log_file = open(self.log_file, "w")
        else:
            pass
            log_file = open(self.log_file, "a")
        if "{" not in log_info[1]:
            log_file.write("ERROR:\n")
        log_file.write(str(timestamp) + ";" + str(log_info[0]) + ";" + str(log_info[1]) + "\n")

    def increment_username(self):
        self.username = self.username + str(self.uname_counter)
        self.uname_counter += 1

    def increment_admin_username(self):
        self.admin_username = self.admin_username + str(self.auname_counter)
        self.auname_counter += 1

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
                elif line[0] == "create_admin":
                    self.create_admin = bool(line[1])
                elif line[0] == "admin_username":
                    self.admin_username = bool(line[1])
                elif line[0] == "admin_password":
                    self.admin_password = bool(line[1])
                elif line[0] == "username":
                    self.username = bool(line[1])
                elif line[0] == "password":
                    self.username = bool(line[1])
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

