import subprocess


def open_task_manager():

    subprocess.Popen(
        ["taskmgr"]
    )

    print(
        "🖥️ Opened Task Manager"
    )