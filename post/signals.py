from django.core.cache import cache
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from post.models import Post


@receiver(pre_save, sender=Post)
@receiver(pre_delete, sender=Post)
def delete_cache(sender, instance, **kwargs):
    cache.delete('post_list')
    print('List cache deleted')
    pk = instance.id
    cache.delete(f'post_detail_{pk}')
    print('Detail cache deleted')
