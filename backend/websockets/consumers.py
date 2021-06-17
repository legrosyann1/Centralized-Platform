import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.auth import login
from actions.tasks import run_playbook
from channels.db import database_sync_to_async


class ActionsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        ''' Accept the connection and subscribe the client to the group 'actions' '''
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            await login(self.scope, self.scope['user'])
            await database_sync_to_async(self.scope["session"].save)()
            await self.channel_layer.group_add('actions', self.channel_name)
            await self.accept()

    async def disconnect(self, code):
        ''' When a client disconnect from websocket unsubscribe it from the group '''
        await self.channel_layer.group_discard('actions', self.channel_name)

    async def receive(self, text_data):
        data_json = json.loads(text_data)
        actions = data_json.get('actions')
        devices = data_json.get('devices')
        if actions is not None and devices is not None:
            for action in actions:
                ack = { 'type': 'ack',
                        'operation': action,
                        'devices': devices,
                        'status': 'Accepted' }
                await self.send(json.dumps(ack))
                database_sync_to_async(run_playbook)(self.user.pk, action, devices)

    async def send_actions(self, event):
        await self.send(text_data=json.dumps({
            'type': 'resp',
            'status': event['status'],
            'action': event['action'],
            'resp' : event['resp']
        }))