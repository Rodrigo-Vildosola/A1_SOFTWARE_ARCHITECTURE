def should_skip_migration(app_label, migration_name):
    skip_migrations = {
        "auth": True,
        "admin": True,
        "contenttypes": True,
        "sessions": True,
    }
    return skip_migrations.get(app_label, False)

class Migration:
    dependencies = []

    operations = []
