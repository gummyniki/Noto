import curses
import os

TODO_FILE = "tasks.txt"
COMPLETED = "✅"
WORKING = "⏳"

def load_tasks():
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, "r") as f:
        return [line.strip() for line in f.readlines()]

def save_tasks(tasks):
    with open(TODO_FILE, "w") as f:
        for task in tasks:
            f.write(f"{task}\n")

def toggle_task(task):
    if COMPLETED in task:
        return task.replace(COMPLETED, "").strip()
    elif WORKING in task:
        return task.replace(WORKING, COMPLETED).strip()
    else:
        return f"{task} {WORKING}"

def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()

    tasks = load_tasks()
    selected = 0

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        stdscr.addstr(0, 0, "To-Do List (↑↓ to move, 'a'=add, 'x'=delete, 'c'=toggle, 'q'=quit)")

        for i, task in enumerate(tasks):
            marker = "->" if i == selected else "  "
            stdscr.addstr(i + 2, 0, f"{marker} {task}")

        key = stdscr.getch()

        if key == curses.KEY_UP:
            selected = max(0, selected - 1)
        elif key == curses.KEY_DOWN:
            selected = min(len(tasks) - 1, selected + 1)
        elif key == ord('a'):
            curses.echo()
            stdscr.addstr(height - 1, 0, "Enter new task: ")
            new_task = stdscr.getstr(height - 1, 17).decode()
            curses.noecho()
            tasks.append(new_task)
            save_tasks(tasks)
        elif key == ord('x') and tasks:
            tasks.pop(selected)
            selected = max(0, selected - 1)
            save_tasks(tasks)
        elif key == ord('c') and tasks:
            tasks[selected] = toggle_task(tasks[selected])
            save_tasks(tasks)
        elif key == ord('q'):
            break

        stdscr.refresh()

if __name__ == "__main__":
    curses.wrapper(main)
