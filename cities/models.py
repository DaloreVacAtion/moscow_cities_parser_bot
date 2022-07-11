from django.db import models


class City(models.Model):
    CITY, PGT = range(2)
    TYPES = (
        (CITY, 'Город'),
        (PGT, 'ПГТ'),
    )
    city_name = models.CharField('Наименование', max_length=128, db_index=True)
    population = models.BigIntegerField('Население', null=True)
    type = models.SmallIntegerField('Тип', choices=TYPES, default=CITY)

    @property
    def city_url(self):
        return f'https://ru.wikipedia.org/wiki/{self.city_name}'