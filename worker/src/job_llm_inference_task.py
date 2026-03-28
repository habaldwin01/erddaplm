import couchbeans
from utils import get_couch_client

import json
import io
import os
import hashlib
import time
import uuid
import io
import csv
from datetime import datetime

class JobLLMInferenceTask:
    def __init__(self):
        pass

    def execute(self, job_md, progress_func):
        self.job_md = job_md
        self.progress_func = progress_func

        print("TEST JobLLMInferenceTask")

        return patch
