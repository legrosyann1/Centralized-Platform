from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from inventory.models import Device, Change
import json
from datetime import date, datetime
import copy


@receiver(pre_save, sender=Device)
def saveChange_before(sender, instance, **kwargs):
    if instance.id is not None:
        old_info = Device.objects.get(id=instance.id)
        new_info = copy.deepcopy(instance.__dict__)
        set_change, old, new = is_change(old=old_info.__dict__, new=new_info)
        
        old['hw_end_of_life'] = json.dumps(old['hw_end_of_life'], default=json_serial)
        old['sw_end_of_life'] = json.dumps(old['sw_end_of_life'], default=json_serial)
        new['hw_end_of_life'] = json.dumps(new['hw_end_of_life'], default=json_serial)
        new['sw_end_of_life'] = json.dumps(new['sw_end_of_life'], default=json_serial)

        if set_change:
            change = Change(old_info=old, new_info=new)
            change.save()
   

'''
@receiver(post_save, sender=Device)
def saveChange_after(sender, instance, **kwargs):
    new_info = copy.deepcopy(instance.__dict__)
    new = clean_data(new_info)
    new['hw_end_of_life'] = json.dumps(new['hw_end_of_life'], default=json_serial)
    new['sw_end_of_life'] = json.dumps(new['sw_end_of_life'], default=json_serial)
    prev = Change.objects.filter(new_info=new).first()

    if prev is not None:
        prev.date = instance.updated_at
        prev.save()
'''

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


def clean_data(device):
    delete_list = ['_state', 'updated_at', 'created_at']
    for key in delete_list:
        device.pop(key, None)
    return device
    

def is_change(old, new):
    '''First delete the keys that change in every update
    then check if both objects are equal. If not then it's 
    identified as a change'''
    old = clean_data(old)
    new = clean_data(new)
    if old != new:
        return True, old, new
    else:
        return False, old, new