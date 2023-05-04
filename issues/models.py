from django.conf import settings
from django.db import models


class Project(models.Model):
    TYPE_CHOICES = [
        ('BE', 'Back-End'),
        ('FE', 'Font-End'),
        ('IO', 'iOS'),
        ('AN', 'Android'),
    ]

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    type = models.CharField(choices=TYPE_CHOICES, max_length=2)
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              related_name='Owner')


class Contributor(models.Model):
    OWNER = 'OWNER'
    CONTRIBUTOR = 'CONTRIBUTOR'

    ROLE_CHOICES = [
        (OWNER, 'Owner'),
        (CONTRIBUTOR, 'Contributor'),
    ]

    project = models.ForeignKey(to=Project,
                                on_delete=models.CASCADE,
                                related_name='contributors')

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    role = models.CharField(choices=ROLE_CHOICES,
                            max_length=30,
                            default=CONTRIBUTOR)

    class Meta:
        unique_together = ('project', 'user')

    def __str__(self):
        return f'{self.user}, {self.project}, {self.role}'


class Issue(models.Model):
    TAG_CHOICES = [
        ('BUG', 'Bug'),
        ('ENHANCEMENT', 'Enhancement'),
        ('TASK', 'Task'),
    ]

    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]

    STATUS_CHOICES = [
        ('TO_DO', 'To-Do'),
        ('IN_PROGRESS', 'In-Progress'),
        ('COMPLETED', 'Completed'),
    ]

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    tag = models.CharField(choices=TAG_CHOICES, max_length=30)
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=30)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, max_length=30)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='author')
    assignee = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='assignee')
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    description = models.CharField(max_length=2048)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                               on_delete=models.SET_NULL,
                               null=True)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
