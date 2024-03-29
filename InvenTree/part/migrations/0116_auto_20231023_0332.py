# Generated by Django 3.2.22 on 2023-10-23 03:32

from django.db import migrations


def migrate_part_responsible_owner(apps, schema_editor):
    """Copy existing part.responsible field to part.responsible_owner"""

    Owner = apps.get_model('users', 'Owner')
    Part = apps.get_model('part', 'Part')
    User = apps.get_model('auth', 'user')
    ContentType = apps.get_model('contenttypes', 'contenttype')

    user_type = ContentType.objects.get_for_model(User)

    parts = Part.objects.exclude(responsible=None)

    for part in parts:

        # Find a corresponding Owner object, or create one if it does not exist
        owner, _created = Owner.objects.get_or_create(
            owner_type=user_type,
            owner_id=part.responsible.id,
        )

        part.responsible_owner = owner
        part.save()

    if parts.count() > 0:
        print(f"Added 'responsible_owner' for {parts.count()} parts")


def reverse_owner_migration(apps, schema_editor):
    """Reverse the owner migration:

    - Set the 'responsible' field to a selected user
    - Only where 'responsible_owner' is set
    - Only where 'responsible_owner' is a User object
    """

    Part = apps.get_model('part', 'Part')
    User = apps.get_model('auth', 'user')
    ContentType = apps.get_model('contenttypes', 'contenttype')

    user_type = ContentType.objects.get_for_model(User)

    parts = Part.objects.exclude(responsible_owner=None)

    for part in parts:

        if part.responsible_owner.owner_type == user_type:

            # Attempt to find matching user
            try:
                user = User.objects.get(pk=part.responsible_owner.owner_id)
                part.responsible = user
                part.save()
            except User.DoesNotExist:
                print("User does not exist:", part.responsible_owner.owner_id)

    if parts.count() > 0:
        print(f"Added 'responsible' for {parts.count()} parts")

class Migration(migrations.Migration):

    dependencies = [
        ('part', '0115_part_responsible_owner'),
        ('users', '0005_owner_model'),
    ]

    operations = [
        migrations.RunPython(
            migrate_part_responsible_owner,
            reverse_code=reverse_owner_migration,
        )
    ]
