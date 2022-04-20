import json

class db_manager:
    """
    A class to simplify managment of the json database

    Attributes
    ----------
    db_file : str
        The name of the database file that the manager will be operating on

    Methods
    -------
    Utility methods (Private)

    __update
        Downloads json data from the file to a variable in the memory
    __write(data: dict)
        Provided with the dictionary -> overwrites existing json 
        database with the changed data from the variable in memory

    Get methods (Public)

    get_friends(user_id: str)
        Takes in the user id and returns the list of users that are in the friend list of specified user

    """


    def __init__(self, db_file: str) -> None:
        """The init function checks if the provided db_file exists and if not - creates it
        
        Attributes
        ----------
        db_file: str
            Name for the json database file
        """

        self.db_file = db_file
        self.data = dict()


    def __update(self) -> None:
        """Pull data from the json database into the variable in the memory"""

        with open(self.db_file, 'r') as db_file:
            self.data = json.load(db_file)


    def __write(self, data: dict) -> None:
        """Ovewrites the data in the json database file
        
        Attributes
        ----------
        data: dict
            A dictionary that's going to be converted to json and written to the database file
        """

        with open(self.db_file, 'w') as db_file:
            json.dump(data, db_file, indent=4)


    # Get functions
    def get_friends(self, user_id: str) -> list:
        """This function returns a list of friends of the specified user by his telegram ID

        Attributes
        ----------
        user_id: str
            The telegram id of specific user
        """
        self.__update()

        friend_list = []
        for id in self.data[user_id]["friends"]:
            name = self.data[str(id)]["name"]
            friend_list.append({
                id: name
            })

        return friend_list

    def get_name(self, user_id: str) -> str:
        """This function returns the name of the specified user by his telegram id
        
        Attributes
        ----------
        user_id: str
            The telegram id of specific user
        """

        self.__update()

        try:
            return self.data[user_id]["name"]
        except Exception as e:
            print(e)


    def add_user(self, user_id: int, name: str) -> None:
        """This function adds a new user to the json database file, 
        initial friend list of the new user is empty by default
        
        Attributes
        ----------
        user_id: str
            The telegram id of a new user
        name: str
            The name of the user
        """

        self.__update()
        new_data = self.data
        new_data[user_id] = {
            "name": name,
            "friends": []
        }
        self.__write(new_data)


    def add_friend(self, user_id: str, friend_id: int):
        """This function adds a new friend to the friend list of the specific user

        Attributes
        ----------
        user_id: str
            The telegram ID of specific user
        friend_id: int
            The telegram ID of the friend being added to users friend list
        """

        self.__update()

        new_data = self.data
        new_data[user_id]["friends"].append(friend_id)
        self.__write(new_data)


    # Check functions
    def check_if_friends(self, user_id: str, friend_id: int) -> bool:   
        """ This function takes in user id of the user and the user id of his friend, then 
        returns True if friends id is in the friend list of the user, and False if not

        Attributes
        ----------
        user_id: str
            The telegram ID of specific user
        friend_id: int
            The telegram ID of the friend
        """

        self.__update()
        return friend_id in self.data[user_id]["friends"]


    def check_if_exists(self, user_id: str) -> bool:
        """ This function checks if the specified user id is in the json database and returns boolean.

        Attributes
        ----------
        user_id: str
            The telegram ID of specific user
        """

        self.__update()

        print(self.data.keys())
        return str(user_id) in self.data.keys()