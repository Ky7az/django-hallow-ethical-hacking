from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

from HallowWatch.models import Content, Feed


@shared_task
def run_scrap(feed_id):

    feed = Feed.objects.get(id=feed_id)
    for content_data in feed.scrap_feed():
        try:
            content = Content.objects.get(url=content_data['url'])
        except ObjectDoesNotExist:
            content = Content.objects.create(**content_data)
        content.save()

@shared_task
def scrap_feeds():

    feeds = Feed.objects.all()
    for feed in feeds:
        res = run_scrap.delay(feed.id)
        feed.celery_task_id = res.id
        feed.save()
