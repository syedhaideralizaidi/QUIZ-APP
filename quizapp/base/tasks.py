from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()
@shared_task(bind = True)
def test_func(self):
    for i in range(10):
        print(i)

    async_to_sync(
        channel_layer.group_send
    )('users', {'type': 'send_jokes', 'text': 'You are inside channels and celery'})
    return "Done"