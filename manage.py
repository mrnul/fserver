#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from file_server_app import utils


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fserver.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if 'runserver' in sys.argv or len(sys.argv) < 2:
        execute_from_command_line(['manage.py', 'runserver', f'{utils.get_ip()}:80'])
    else:
        execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
