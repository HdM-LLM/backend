from db.mapper.mysql_mapper.mysql_mapper import MySQLMapper
from classes.category import Category
from uuid import UUID

class CategoryMapper(MySQLMapper):

    def __init__(self):
        super().__init__()

    def get_all(self):
        result = []
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM category")
        tuples = cursor.fetchall()

        for tuple_data in tuples:
            (id, name, chip, guideline_for_zero, guideline_for_ten) = tuple_data

            category = Category(
                name=name,
                chip=chip,
                guideline_for_zero=guideline_for_zero,
                guideline_for_ten=guideline_for_ten
                # Add other properties as needed
            )
            category.set_id(UUID(id))
            result.append(category)

        cursor.close()
        return result
    
    def get_distinct_chips(self):
        result = []
        cursor = self._connection.cursor()
        cursor.execute("SELECT DISTINCT chip FROM category")
        chips = cursor.fetchall()

        for chip_tuple in chips:
            (chip,) = chip_tuple
            result.append(chip)

        cursor.close()
        return result
    
    def get_by_id(self, category_id: str):
        result = []
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM category WHERE id = %s", (category_id,))
        tuple_data = cursor.fetchone()

        if tuple_data:
            (id, name, chip, guideline_for_zero, guideline_for_ten) = tuple_data

            category = Category(
                name=name,
                chip=chip,
                guideline_for_zero=guideline_for_zero,
                guideline_for_ten=guideline_for_ten
            )
            category.set_id(UUID(id))
            result.append(category)

        cursor.close()
        return result[0] if result else None

    def get_by_name(self, category_name: str):
        result = []
        cursor = self._connection.cursor()
        cursor.execute("SELECT * FROM category WHERE name = %s", (category_name,))
        tuple_data = cursor.fetchone()

        if tuple_data:
            (id, name, chip, guideline_for_zero, guideline_for_ten) = tuple_data

            category = Category(
                name=name,
                chip=chip,
                guideline_for_zero=guideline_for_zero,
                guideline_for_ten=guideline_for_ten
                # Add other properties as needed
            )
            category.set_id(UUID(id))
            result.append(category)

        cursor.close()
        return result[0] if result else None

    def insert(self, category: Category):
        cursor = self._connection.cursor()
        query = "INSERT INTO category (id, name, chip, guideline_for_zero, guideline_for_ten) VALUES (%s, %s, %s, %s, %s)"
        data = (
            str(category.get_id()),
            category.get_name(),
            category.get_chip(),
            category.get_guideline_for_zero(),
            category.get_guideline_for_ten()
            # Add other properties as needed
        )

        cursor.execute(query, data)
        self._connection.commit()
        cursor.close()

    def update(self, category: Category):
        cursor = self._connection.cursor()
        query = "UPDATE category SET name=%s, chip=%s, guideline_for_zero=%s, guideline_for_ten=%s WHERE id=%s"
        data = (
            category.get_name(),
            category.get_chip(),
            category.get_guideline_for_zero(),
            category.get_guideline_for_ten(),
            str(category.get_id())
        )

        cursor.execute(query, data)
        self._connection.commit()
        cursor.close()

    def delete_by_id(self, category_id: UUID):
        cursor = self._connection.cursor()
        query = "DELETE FROM category WHERE id=%s"
        cursor.execute(query, (str(category_id),))
        self._connection.commit()
        cursor.close()
