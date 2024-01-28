from db.mapper.mysql_mapper.mysql_mapper import MySQLMapper
from uuid import UUID

class EvaluationMapper(MySQLMapper):
    def __init__(self):
        super().__init__()

    def insert(self, applicant_id: str, score: int):
        cursor = self._connection.cursor()
        query = """
            INSERT INTO evaluation (id, applicant_id, score) 
            VALUES (UUID(), %s, %s)
        """
        data = (applicant_id, score)

        try:
            cursor.execute(query, data)
            self._connection.commit()
            print("Evaluation record inserted successfully!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def delete_by_id(self, id):
        cursor = self._connection.cursor()
        query = "DELETE FROM evaluation WHERE id = %s"
        data = (id,)

        try:
            cursor.execute(query, data)
            self._connection.commit()
            print("Evaluation record deleted successfully!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def get_all(self):
        cursor = self._connection.cursor()
        query = "SELECT * FROM evaluation"

        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def get_by_id(self, id):
        cursor = self._connection.cursor()
        query = "SELECT * FROM evaluation WHERE id = %s"
        data = (id,)

        try:
            cursor.execute(query, data)
            result = cursor.fetchone()
            return result
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()

    def update(self, id, data):
        cursor = self._connection.cursor()
        query = "UPDATE evaluation SET applicant_id = %s, score = %s WHERE id = %s"
        data = (data["applicant_id"], data["score"], id)

        try:
            cursor.execute(query, data)
            self._connection.commit()
            print("Evaluation record updated successfully!")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
