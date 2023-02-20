from marshmallow import Schema, fields


class ItemsSchema(Schema):
    id = fields.Integer(dump_only=True, autoincrement=True)
    currency_code = fields.String(required=True)
    value = fields.String(required=True)
    date = fields.String(required=True)
