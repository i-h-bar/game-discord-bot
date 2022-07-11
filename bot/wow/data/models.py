from tortoise import Model, fields


class Items(Model):
    id = fields.IntField(pk=True)
    tooltip = fields.BinaryField()
    profession = fields.TextField(null=True)
