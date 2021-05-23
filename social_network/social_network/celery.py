from __future__ import absolute_import, unicode_literals

import os
import sys


from celery import Celery

app = Celery("exec")

app.config_from_object("django.conf:settings")

# This allows easy placement of apps within the interior
# 'apps' directory.
current_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(current_path, "apps"))

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
