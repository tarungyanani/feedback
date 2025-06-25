import os
import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = get_wsgi_application()

# 🚀 Auto-run migrations and superuser creation on startup (for Render free plan)
try:
    from django.core.management import call_command
    call_command('migrate', interactive=False)

    # ✅ Auto-create superuser (admin/admin123)
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        print("✅ Superuser created: admin / admin123")
    else:
        print("ℹ️ Superuser already exists")

except Exception as e:
    print("⚠️ Startup task failed:", e)
