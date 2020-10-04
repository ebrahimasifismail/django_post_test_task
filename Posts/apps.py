from django.apps import AppConfig


class PostsConfig(AppConfig):
    name = 'Posts'

    def ready(self):
        import Posts.signals  # noqa
