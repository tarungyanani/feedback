import os
import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = get_wsgi_application()

# 🚀 Auto-run migrations on startup (Render free plan)
try:
    from django.core.management import call_command
    call_command('migrate', interactive=False)
except Exception as e:
    print("⚠️ Migration failed:", e)
