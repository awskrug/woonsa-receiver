from gevent.socket import create_connection
import boto
import boto.dynamodb

class Emitter(object):
    def __init__(self, *args, **kwargs):
        pass

    def emit(self, key, value, ts):
        pass

class CarbonEmitter(Emitter):
    def __init__(self, *args, **kwargs):
        Emitter.__init__(self, *args, **kwargs)
        self.host = kwargs.get('CARBON_HOST')
        self.port = kwargs.get('CARBON_PORT')

    def _make_packet(self, key, value, ts):
        return "%s %s %d\n" % (key, value, ts)

    def emit(self, key, value, ts):
        try:
            sock = create_connection((self.host, self.port))
            sock.sendall(self._make_packet(key, value, ts))
        finally:
            sock.close()

class DynamoDbEmitter(Emitter):
    def __init__(self, *args, **kwargs):
        Emitter.__init__(self, *args, **kwargs)
        self.aws_access_key_id = kwargs.get('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = kwargs.get('AWS_SECRET_ACCESS_KEY')
        self.aws_region = kwargs.get('AWS_REGION')
        self.aws_dynamo_db_schema = kwargs.get('AWS_DYNAMODB_SCHEMA')
        self._conn = None

    def _connection(self):
        if self._conn:
            return self._conn

        region = [r for r in boto.dynamodb.regions() if r.name == self.aws_region][0]
        self._conn = boto.connect_dynamodb(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region=region)
        return self._conn

    def _get_schema(self):
        from boto.dynamodb.schema import Schema
        return Schema.create(
            hash_key=('client_id', 'S'),
            range_key=('ts', 'N'))

    def _get_table(self):
        return self._connection().table_from_schema(
            name=self.aws_dynamo_db_schema,
            schema=self._get_schema())

    def emit(self, key, value, ts):
        table = self._get_table()
        item = table.new_item(
            hash_key=key,
            range_key=ts,
            attrs={'lines': value}
        )
        item.put()

