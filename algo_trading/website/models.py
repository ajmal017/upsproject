from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Trade(models.Model):
    trade_id = models.CharField(max_length=1, blank=False, null=False, primary_key = True)
    trade_value = models.CharField(max_length=1, blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'trading_type'

class Target(models.Model):
    target_id = models.CharField(max_length=5, blank=False, null=False, primary_key = True)
    target_desc = models.CharField(max_length=20, blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'target'

class Stoploss(models.Model):
    stoploss_id = models.CharField(max_length=5, blank=False, null=False, primary_key = True)
    stoploss_desc = models.CharField(max_length=20, blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'stoploss'

class TimeFrame(models.Model):
    timeframe_id = models.AutoField(primary_key=True)
    timeframe_value = models.IntegerField(blank=False, null=False)

    class Meta:
        managed = True
        db_table = 'time_frame'

class UserRole(models.Model):
    role_id = models.BigIntegerField(blank=False, null=False, primary_key = True)
    user_id = models.CharField(max_length=6, blank=False, null=False)
    role_name = models.CharField(max_length=6, blank=False, null=False)
    description = models.CharField(max_length=20, blank=False, null=False)
    class Meta:
        managed = True
        db_table = 'user_role'

class UserProfile(models.Model):
    userprofile_id = models.AutoField(primary_key = True)
    user_id = models.CharField(max_length=6, blank=False, null=False)
    user_name = models.CharField(max_length=25, blank=False, null=False)
    secret_key = models.CharField(max_length=50, blank=False, null=False)
    api_key = models.CharField(max_length=50, blank=False, null=False)
    redirect_url = models.CharField(max_length=50, blank=False, null=False)
    access_token = models.CharField(max_length=50, blank=True, null=True)
    trade_type = models.CharField(max_length=1, blank=True, null=True)
    available_margin = models.FloatField(blank=True, null=True)
    is_today = models.BooleanField(blank=False, null=False, default=True)
    class Meta:
        managed = True
        db_table = 'Userprofile'

class Strategy(models.Model):
    strategy_id = models.AutoField(primary_key=True)
    strategy_name = models.CharField(max_length=20, blank=False, null=False)
    time_frame = models.IntegerField(blank=True, null=True)
    candle_ref = models.IntegerField(blank=True, null=True)
    no_of_candle = models.IntegerField(blank=True, null=True)
    buffer_amnt = models.FloatField(blank=False, null=False)
    chk_next_candle = models.BooleanField(blank=False, null=False, default=False)
    is_open_price = models.BooleanField(blank=False, null=False, default=False)
    combine_candle = models.BooleanField(blank=False, null=False, default=False)
    reverse_trade = models.BooleanField(blank=False, null=False, default=False)
    candle_high = models.FloatField(blank=True, null=True)
    candle_low = models.FloatField(blank=True, null=True)
    candle_close = models.FloatField(blank=True, null=True)
    candle_open = models.FloatField(blank=True, null=True)
    target_id = models.CharField(max_length=5, blank=True, null=True)
    stoploss_id = models.CharField(max_length=5, blank=True, null=True)
    condition1 = models.CharField(max_length=50, blank=True, null=True)
    condition2 = models.CharField(max_length=50, blank=True, null=True)
    condition3 = models.CharField(max_length=50, blank=True, null=True)

    def __unicode__(self):
        return u"%s" % self.name
    class Meta:
        managed = True
        db_table = 'strategy'

class Scripts(models.Model):
    script_id = models.AutoField(primary_key=True)
    script_name = models.CharField(max_length=50, blank=False, null=False)
    strategy = models.OneToOneField(Strategy, on_delete=models.CASCADE)
    trade = models.OneToOneField(Trade, on_delete=models.CASCADE)
    exchange_type = models.CharField(max_length=10, blank=True, null=True)
    is_strategy_active = models.BooleanField(blank=False, null=False, default=True)

    class Meta:
        managed = True
        db_table = 'scripts'

class Trading(models.Model):
    trading_id = models.AutoField(primary_key=True)
    script = models.OneToOneField(Scripts, on_delete=models.CASCADE)
    trade = models.OneToOneField(Trade, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'trading'
