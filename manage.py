#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'currency_converter.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            ) from exc
        raise

    is_testing = 'test' in sys.argv

    if is_testing:
        import coverage
        cov = coverage.coverage(source=['currency'], omit=['*/tests/*', 'currency/apps.py'])
        cov.erase()
        cov.start()

        execute_from_command_line(sys.argv)

        cov.stop()
        cov.save()
        cov.report()
        cov.html_report()


if __name__ == '__main__':
    main()
