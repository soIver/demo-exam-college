from PyQt5.QtSql import QSqlTableModel, QSqlRelationalTableModel, QSqlRelation


class UserModel(QSqlRelationalTableModel):
    MAX_AUTH_ATTEMPTS = 3
    def __init__(self, db):
        super().__init__(db=db)
        self.setTable("users")
        self.setRelation(self.fieldIndex("role"), QSqlRelation("roles", "id", "name"))
        self.setEditStrategy(QSqlTableModel.OnManualSubmit)
    
    def select_all(self):
        self.select()
        return [self.record(i) for i in range(self.rowCount())]
    
    def select_by_field(self, field_name: str, field_value):
        val = f"'{field_value}'" if isinstance(field_value, str) else field_value
        self.setFilter(f"{field_name}={val}")
        self.select()
        return self.record(0)
    
    def is_blocked(self, record_index: int = 0):
        return self.record(record_index).value("fail_auth_attempts") >= self.MAX_AUTH_ATTEMPTS