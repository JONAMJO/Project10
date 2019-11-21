from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='genre',
            new_name='genres',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='like_users',
        ),
        migrations.AddField(
            model_name='movie',
            name='liked_users',
            field=models.ManyToManyField(related_name='liked_movies', to=settings.AUTH_USER_MODEL),
        ),
    ]
