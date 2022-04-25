import sqlite3


class Db:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `bases` WHERE `telegram_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, tg_username, telegram_id, full_name):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO `bases` (`tg_username`, `telegram_id`,`full_name`) VALUES(?,?,?)",
                (tg_username, telegram_id, full_name))

    def create_profile(self, telegram_id, tg_username, name, description, age, city, photo, sex):
        with self.connection:
            return self.cursor.execute("INSERT INTO `profile_list` (`telegram_id`,`telegram_username`,`name`,"
                                       "`description`, 'age', `city`,`photo`,`sex`) VALUES(?,?,?,?,?,?,?,?)",
                                       (telegram_id, tg_username, name, description, age, city, photo, sex))

    def profile_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `profile_list` WHERE `telegram_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def set_city_search(self, city, user_id):
        with self.connection:
            return self.cursor.execute('UPDATE `profile_list` SET `city_preference` = ? WHERE `telegram_id` = ?',
                                       (city, user_id))

    def delete(self, user_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM `profile_list` WHERE `telegram_id` = ?", (user_id,))

    def search_profile(self, city):
        with self.connection:
            return self.cursor.execute(
                "SELECT `telegram_id` FROM `profile_list` WHERE `city` = ?", (city, )).fetchall()

    def get_info(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `profile_list` WHERE `telegram_id` = ?", (user_id,)).fetchone()

    def get_info_user(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `bases` WHERE `telegram_id` = ?", (user_id,)).fetchone()

    def edit_profile_status(self, user_id, num):
        with self.connection:
            return self.cursor.execute('UPDATE `bases` SET `search` = ? WHERE `telegram_id` = ?',
                                       (num, str(user_id)))

    def search_profile_status(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT `search` FROM `bases` WHERE `telegram_id` = ?", (user_id,)).fetchone()
