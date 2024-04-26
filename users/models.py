from django.db import models
from datetime import date
from django.db.models import QuerySet
from services.file_path_getter import get_file_path


class Faculty(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Факультет'
        verbose_name_plural = 'Факультеты'
        ordering = ["name"]

    def __str__(self):
        return self.name


class Direction(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Направление подготовки'
        verbose_name_plural = 'Направления подготовки'
        ordering = ["name"]

    def __str__(self):
        return f'{self.code} - {self.name}'


class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ["name"]

    def __str__(self):
        return self.name


class UserQuerySet(models.query.QuerySet):
    def search(self, name: str, leader_id: int | None = None, members_id: list[int] | None = None) -> QuerySet:
        """
        Возвращает QuerySet пользователей, найденных по полному или неполному имени.

        :param name: имя (полное или неполное),
        :type name: str
        :param leader_id: идентификатор руководителя команды,
        :type leader_id: int | None
        :param members_id: список идентификаторов текущих участников команды.
        :type members_id: list[int] | None
        :return: QuerySet найденных пользователей или пустой QuerySet, если пользователи не найдены.
        :rtype: QuerySet
        """
        name_parts = [word.capitalize() for word in name.strip().split()]

        if len(name_parts) > 3:
            return QuerySet()

        if len(name_parts) == 3:
            users = \
                self.filter(last_name__startswith=name_parts[0]) & \
                self.filter(first_name__startswith=name_parts[1]) & \
                self.filter(patronymic__startswith=name_parts[2])
        elif len(name_parts) == 2:
            users = \
                self.filter(last_name__startswith=name_parts[0]) & \
                self.filter(first_name__startswith=name_parts[1]) | \
                self.filter(first_name__startswith=name_parts[0]) & \
                self.filter(last_name__startswith=name_parts[1]) | \
                self.filter(first_name__startswith=name_parts[0]) & \
                self.filter(patronymic__startswith=name_parts[1])
        else:
            users = \
                self.filter(last_name__startswith=name_parts[0]) | \
                self.filter(first_name__startswith=name_parts[0]) | \
                self.filter(patronymic__startswith=name_parts[0])

        if leader_id is not None and members_id is not None:
            users = users.exclude(id__in=(leader_id, *members_id))

        return users


class BaseUserManager(models.Manager):
    pass


class UserManager(BaseUserManager.from_queryset(UserQuerySet)):
    pass


def get_photo_path(instance, file_name):
    return get_file_path(file_name, 'images/users_photos')


def get_cropped_photo_path(instance, file_name):
    return f"images/users_photos/cropped-{instance.photo.name.replace('images/users_photos/', '')}"


class User(models.Model):
    id = models.AutoField(primary_key=True)
    photo = models.ImageField(blank=True, upload_to=get_photo_path, default='images/default-user-photo.png')
    cropped_photo = models.ImageField(blank=True, upload_to=get_cropped_photo_path,
                                      default='images/cropped-default-user-photo.png')
    login = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    patronymic = models.CharField(max_length=50, blank=True, null=True)
    birthday = models.DateField()
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    e_mail = models.CharField(max_length=50, blank=True, null=True)
    vk = models.CharField(max_length=50, blank=True, null=True)
    biography = models.CharField(max_length=200, blank=True, null=True)
    faculty = models.ForeignKey(Faculty, related_name='faculty_users', null=True, on_delete=models.SET_NULL)
    direction = models.ForeignKey(Direction, related_name='direction_users', null=True, on_delete=models.SET_NULL)
    group = models.ForeignKey(Group, related_name='group_users', null=True, on_delete=models.SET_NULL)
    teams = models.ManyToManyField('teams.Team', blank=True, null=True)

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ["last_name"]

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic if self.patronymic is not None else ''}"

    @property
    def age(self):
        today = date.today()
        age = today.year - self.birthday.year

        if today.month < self.birthday.month or today.month == self.birthday.month and today.day < self.birthday.day:
            age -= 1

        if age in (16, 17, 18):
            age = f'{age} лет'
        else:
            match age % 10:
                case 0 | 5 | 6 | 7 | 8 | 9:
                    age = f'{age} лет'
                case 1:
                    age = f'{age} год'
                case 2 | 3 | 4:
                    age = f'{age} года'

        return age

    @property
    def all_projects_count(self):
        all_projects_count = self.manager_projects.count() + len(
            [
                project
                for team in self.teams.all()
                for project in team.team_projects.all()
            ]
        )
        return all_projects_count

    @property
    def done_projects_count(self):
        done_projects_count = self.manager_projects.filter(status='завершен').count() + len(
            [
                project
                for team in self.teams.all()
                for project in team.team_projects.filter(status='завершен')
            ]
        )
        return done_projects_count

    @property
    def all_tasks_count(self):
        all_tasks_count = self.responsible_tasks.count()
        return all_tasks_count

    @property
    def done_tasks_count(self):
        done_tasks_count = self.responsible_tasks.filter(status='выполнена').count()
        return done_tasks_count

    @property
    def teams_count(self):
        teams_count = self.teams.count() + self.leader_teams.count()
        return teams_count

