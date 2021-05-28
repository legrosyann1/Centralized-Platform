from __future__ import absolute_import
from actions.models import Action, LogAction
from actions.devicesChangesToExcel import updateDevicesToExcel
from django.contrib.auth.models import User
from celery import shared_task
#import ansible_runner
import pathlib
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def run_playbook(user_pk, action_name, devices=[], extravars={}):
    pb_path = str(pathlib.Path(__file__).parent.absolute()) + '/ansible/' #path to ansible/ folder
    user = User.objects.get(pk=user_pk)
    action = Action.objects.filter(name=action_name).first() #get action object to retrieve playbook name
    LogAction(user=user, action=action)
    #r = ansible_runner.run(private_data_dir=pb_path, json_mode=True, playbook=action.template, inventory=devices, extravars=extravars)
    #print(r.stats)
    #write_to_channel.delay(r.stats)
    return True

def write_to_channel(resp):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)('actions', {
        'type': 'send.actions',
        'resp': resp
        })


@shared_task
def helloWorld():
    # Do heavy computation with variables in setup model here.
    print('Hello World!')

@shared_task()
def getWeeklyChanges():
    result = updateDevicesToExcel().start()
    return result