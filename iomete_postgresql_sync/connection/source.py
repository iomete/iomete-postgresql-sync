class SourceConnection:
    def __init__(self, host: str, port: str, user_name: str, user_pass: str, catalog: str):
        self.host = host
        self.port = port
        self.user_name = user_name
        self.user_pass = user_pass
        self.catalog = catalog

    def jdbc_url(self, schema):
        return None

    @property
    def jdbc_driver(self):
        return None

    def proxy_table_definition_for_info_schema(self, proxy_table_name):
        return self.proxy_table_definition(
            source_schema="information_schema",
            source_table="tables",
            proxy_table_name=proxy_table_name
        )

    def proxy_table_definition(self, source_schema, source_table, proxy_table_name):
        return f"""
            CREATE TABLE IF NOT EXISTS {proxy_table_name}
            USING org.apache.spark.sql.jdbc
            OPTIONS (
              url '{self.jdbc_url(self.catalog)}',
              dbtable '{source_schema}.{source_table}',
              user '{self.user_name}',
              password '{self.user_pass}',
              driver '{self.jdbc_driver}'
            )
        """


class PostgreSQLConnection(SourceConnection):
    def __init__(self, host: str, port: str, user_name: str, user_pass: str, catalog: str):
        super().__init__(host, port, user_name, user_pass, catalog)

    def jdbc_url(self, catalog):
        return f'jdbc:postgresql://{self.host}:{self.port}/{catalog}'

    @property
    def jdbc_driver(self):
        return 'org.postgresql.Driver'

    def __str__(self):
        return f"PostgreSQLConnection(host: '{self.host}')"
