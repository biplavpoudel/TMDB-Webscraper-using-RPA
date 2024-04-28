from robocorp.tasks import task
from app.process import Process
from app.constants import *

@task
def scraping():
    process = Process(browser_lib, path)
    process.before_run_process()
    process.run_process()
    process.after_run_process()