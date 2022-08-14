from tortoise import Model, fields


class Items(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=128)
    tooltip = fields.BinaryField()
    profession = fields.TextField(null=True)
