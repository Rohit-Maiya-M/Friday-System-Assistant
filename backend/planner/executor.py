from voice.executor import (
    open_app,
    close_app,
    search_web
)
from capabilities.screenshot import take_screenshot
from capabilities.calculate import calculate
from voice.reasoning_engine import (
    handle_reasoning
)
from capabilities.calculate import calculate
from capabilities.screenshot import take_screenshot
from workflows.write_note import (
    write_note
)
from voice.executor import (
    open_app,
    close_app,
    search_web
)
from voice.reasoning_engine import (
    handle_reasoning
)
from workflows.open_task_manager import (
    open_task_manager
)
import time
from utils.toast_state import (
    update_toast
)

def show_toast(message):

    update_toast(

        visible=True,

        message=message
    )

    time.sleep(4)

    update_toast(

        visible=False,

        message=""
    )

def execute_task(task):

    print(f"\n🚀 Executing Task {task.task_id}")

    print(task)

    if task.capability == "OPEN_APP":

        app = task.params["app"]

        open_app(app)

        show_toast(

            f"✅ Opened {app}"
        )

    elif task.capability == "CLOSE_APP":

        app = task.params["app"]

        close_app(app)

        show_toast(

            f"❌ Closed {app}"
        )

    elif task.capability == "SEARCH_WEB":

        query = task.params["query"]

        search_web(query)

        show_toast(

            f"🌐 Searching: {query}"
        )

    elif task.capability == "REASONING":

        query = task.params["query"]

        response = handle_reasoning(query)

        show_toast(response)

    elif task.capability == "CALCULATE":

        expression = task.params["expression"]

        result = calculate(expression)

        show_toast(

            f"🧮 {expression} = {result}"
        )

    elif task.capability == "TAKE_SCREENSHOT":

        take_screenshot()

        show_toast(

            "📸 Screenshot captured"
        )

    elif task.capability == "WRITE_NOTE":

        text = task.params.get("text")

        if not text:

            print("❌ Missing note text")

            return

        write_note(text)

        show_toast(

            "📝 Note written"
        )

    elif task.capability == "OPEN_TASK_MANAGER":

        open_task_manager()

        show_toast(

            "📊 Task Manager opened"
        )


def execute_dag(tasks):

    completed = set()

    while len(completed) < len(tasks):

        progress = False

        for task in tasks:

            if task.task_id in completed:
                continue

            if all(
                dep in completed
                for dep in task.dependencies
            ):

                execute_task(task)

                completed.add(task.task_id)

                progress = True

        if not progress:

            print(
                "\n❌ Circular dependency "
                "or blocked DAG detected"
            )

            break

    print("\n✅ DAG Execution Finished")