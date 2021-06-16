from __future__ import absolute_import
from actions.models import Action, LogAction
from actions.devicesChangesToExcel import updateDevicesToExcel
from django.contrib.auth.models import User
from .models import ScheduledTask
from celery import shared_task
#import ansible_runner
import pathlib
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def run_playbook(user_pk, action_name, devices=[], extravars={}):
    pb_path = str(pathlib.Path(__file__).parent.absolute()) + '/ansible/' #path to ansible/ folder
    host_list = ['localhost'] # localhost until lab environment created
    # We write the hosts file to add all the server that need ssh connection
    with open(pb_path + '/inventory/hosts','w') as file:
        file.write('\n'.join(host_list))
    user = User.objects.get(pk=user_pk)
    action = Action.objects.filter(name=action_name).first() #get action object to retrieve playbook name
    #r = ansible_runner.run(private_data_dir=pb_path, playbook=action.template, extravars=extravars)
    res = None
    for c in r.events:
        try:
            res = c['event_data']['res']['msg']
        except KeyError:
            pass
    log = LogAction.objects.create(user=user, action=action, result=res)
    #status = r.status
    #write_to_channel(status, action_name, res)
    return log

def write_to_channel(status, action, resp):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)('actions', {
        'type': 'send.actions',
        'action': action,
        'status': status,
        'resp': resp
        })


@shared_task
def helloWorld():
    print('Hello World!')

@shared_task()
def getWeeklyChanges():
    task = ScheduledTask.objects.filter(title='getWeeklyChanges').first()
    if task.admin == None:
        task.enabled = False
        task.save()
        return 'Define new administrator of task'
    result = updateDevicesToExcel().start(task.admin.email)
    return result