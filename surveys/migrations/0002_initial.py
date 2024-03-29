# Generated by Django 4.2.3 on 2023-09-02 12:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('surveys', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='response',
            name='respondent_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='response',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.survey'),
        ),
        migrations.AddField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.survey'),
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='chosen_choice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='surveys.choice'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='response',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='surveys.response'),
        ),
        migrations.AlterUniqueTogether(
            name='question',
            unique_together={('survey', 'ordinal_number')},
        ),
        migrations.AlterUniqueTogether(
            name='choice',
            unique_together={('question', 'ordinal_number')},
        ),
    ]
