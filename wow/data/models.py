from tortoise import Model, fields


class Items(Model):
    id = fields.IntField(pk=True)
    tooltip = fields.TextField()
    profession = fields.TextField(null=True)
