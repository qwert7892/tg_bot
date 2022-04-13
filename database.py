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
