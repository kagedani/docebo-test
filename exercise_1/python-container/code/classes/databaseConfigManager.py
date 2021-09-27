class databaseConfigManager:
    
    def __init__(self, host: str, user: object, psw: str, database: str) -> None:
        """
        @summary: database config manager
        @param host: ip address of the database node
        @param user: connection username
        @param psw: connection password
        @param database: database name
        """
        self.database_connection_info = {}
        self.database_connection_info = {
            'host': host,
            'database': database,
            'user': user,
            'password': psw            
        }

        @property
        def get_connection_info(self) -> dict:
            """
            @rtype: dict
            @summary: return info for a database connection as a dict
            @return: connection info
            """
            return self.database_connection_info