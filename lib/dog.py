
import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed):
        self.id = None
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        # Create the 'dogs' table if it doesn't exist
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        # Drop the 'dogs' table if it exists
        sql = "DROP TABLE IF EXISTS dogs"
        CURSOR.execute(sql)

    def save(self):
        if self.id is None:
            # Insert a new row into the 'dogs' table
            sql = "INSERT INTO dogs (name, breed) VALUES (?, ?)"
            CURSOR.execute(sql, (self.name, self.breed))
            CONN.commit()
            # Update the 'id' of the instance with the last inserted row's ID
            self.id = CURSOR.lastrowid
        else:
            # If the instance already has an 'id', update the corresponding row
            sql = "UPDATE dogs SET name = ?, breed = ? WHERE id = ?"
            CURSOR.execute(sql, (self.name, self.breed, self.id))
            CONN.commit()

    @classmethod
    def create(cls, name, breed):
        dog = Dog(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, row):
        # Create a Dog instance from a database row
        id, name, breed = row
        dog = cls(name, breed)
        dog.id = id
        return dog

    @classmethod
    def get_all(cls):
        # Retrieve all dogs from the 'dogs' table and return them as instances
        sql = "SELECT * FROM dogs"
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        return [cls.new_from_db(row) for row in rows]

    @classmethod
    def find_by_name(cls, name):
        # Find a dog by name and return it as an instance
        sql = "SELECT * FROM dogs WHERE name = ?"
        CURSOR.execute(sql, (name,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            return None

    @classmethod
    def find_by_id(cls, id):
        # Find a dog by ID and return it as an instance
        sql = "SELECT * FROM dogs WHERE id = ?"
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            return None

    @classmethod
    def find_or_create_by(cls, name, breed):
        # Try to find a dog by name and breed
        existing_dog = cls.find_by_name(name)
        if existing_dog:
            return existing_dog
        else:
            # If the dog doesn't exist, create a new one
            return cls.create(name, breed)

    def update(self):
        # Update the corresponding row in the database with the new attributes
        self.save()
