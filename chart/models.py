# chart/modles.py
from django.db import models

class Passenger(models.Model):  # 승객 모델
    # 성별 상수 정의
    MALE = 'M'
    FEMALE = 'F'
    SEX_CHOICES = (
        (MALE, 'male'),
        (FEMALE, 'female')
    )

    # 승선_항구 상수 정의
    CHERBOURG = 'C'
    QUEENSTOWN = 'Q'
    SOUTHAMPTON = 'S'
    PORT_CHOICES = (
        (CHERBOURG, 'Cherbourg'),
        (QUEENSTOWN, 'Queenstown'),
        (SOUTHAMPTON, 'Southampton'),
    )

    name = models.CharField(max_length=100, blank=True)                 # 이름
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)           # 성별
    survived = models.BooleanField()                                    # 생존_여부
    age = models.FloatField(null=True)                                  # 연령
    ticket_class = models.PositiveSmallIntegerField()                   # 티켓_등급
    embarked = models.CharField(max_length=1, choices=PORT_CHOICES)     # 승선_항구

    def __str__(self):
        return self.name


class Covid(models.Model):
    # 칼럼 정의
    date = models.DateField()
    france = models.FloatField(null=True)
    germany = models.FloatField(null=True)
    korea = models.FloatField(null=True)
    us = models.FloatField(null=True)
    uk = models.FloatField(null=True)

    def __float__(self):
        return self.korea


class Covid_confirmed(models.Model):
    # 칼럼 정의
    date = models.DateField()
    france = models.FloatField(null=True)
    germany = models.FloatField(null=True)
    korea = models.FloatField(null=True)
    us = models.FloatField(null=True)
    uk = models.FloatField(null=True)

    def __float__(self):
        return self.korea


class Covid_recovered(models.Model):
    # 칼럼 정의
    date = models.DateField()
    france = models.FloatField(null=True)
    germany = models.FloatField(null=True)
    korea = models.FloatField(null=True)
    us = models.FloatField(null=True)
    uk = models.FloatField(null=True)

    def __float__(self):
        return self.korea


class Covid_deaths(models.Model):
    # 칼럼 정의
    date = models.DateField()
    france = models.FloatField(null=True)
    germany = models.FloatField(null=True)
    korea = models.FloatField(null=True)
    us = models.FloatField(null=True)
    uk = models.FloatField(null=True)

    def __float__(self):
        return self.korea


