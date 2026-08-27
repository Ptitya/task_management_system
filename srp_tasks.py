from abc import ABC, abstractmethod


class TaskStorage(ABC):

  @abstractmethod
  def load_tasks(self):
    pass

  @abstractmethod
  def save_tasks(self, tasks):
    pass


class FileTaskStorage(TaskStorage):

  def __init__(self, filename="tasks.txt"):
    self.filename = filename

  def load_tasks(self):
    loaded_tasks = []
    try:
      with open(self.filename, "r", encoding="utf-8") as f:
        for line in f:
          parts = line.strip().split(",") # รองรับการโหลด 5 ค่า (id, description, due_date, priority, completed)
          if len(parts) == 5:
            task_id = int(parts[0])
            description = parts[1]
            due_date = parts[2] if parts[2] != "None" else None
            priority = parts[3]
            completed = parts[4] == "True"
            loaded_tasks.append(
                Task(task_id, description, due_date, priority, completed)
            )
    except FileNotFoundError:
      print(f"No existing task file '{self.filename}' found. Starting fresh.")
    return loaded_tasks

  def save_tasks(self, tasks):
    with open(self.filename, "w", encoding="utf-8") as f:
      for task in tasks:
        f.write(
            f"{task.id},{task.description},{task.due_date},{task.priority},{task.completed}\n"
        )
    print(f"Tasks saved to {self.filename}")


class Task:

  def __init__(
      self, task_id, description, due_date=None, priority="medium", completed=False
  ):
    self.id = task_id
    self.description = description
    self.due_date = due_date
    self.priority = priority # เพิ่ม priority attribute
    self.completed = completed

  def mark_completed(self):
    self.completed = True
    print(f"Task {self.id} '{self.description}' marked as completed.")

  def __str__(self):
  # ปรับแต่ง __str__ เพื่อแสดงผล priority
    status = "✓" if self.completed else " "
    due = f" (Due: {self.due_date})" if self.due_date else ""
    return f"[{status}] [{self.priority.upper()}] {self.id}. {self.description}{due}"


class TaskManager:

  def __init__(self, storage: TaskStorage):  # รับ storage object เข้ามา
    self.storage = storage
    self.tasks = self.storage.load_tasks()
    self.next_id = (
        max([t.id for t in self.tasks] + [0]) + 1 if self.tasks else 1
    )
    print(f"Loaded {len(self.tasks)} tasks. Next ID: {self.next_id}")

  def get_task_by_id(self, task_id):
    for task in self.tasks:
      if task.id == task_id:
        return task
    return None

  def list_tasks(self):
    if not self.tasks:
      print("No tasks available.")
      return
    print("\n--- Task List ---")
    for task in self.tasks:
      print(task)
    print("-----------------\n")

  def add_task(self, description, due_date=None, priority="medium"):
    task = Task(self.next_id, description, due_date, priority)
    self.tasks.append(task)
    self.next_id += 1
    self.storage.save_tasks(self.tasks)  # Save after adding
    print(f"Task '{description}' added.")
    return task

# ... (list_tasks, get_tasks_by_id, mark_task_completed methods เหมือนเดิม) ...

  def mark_task_completed(self, task_id):
    task = self.get_task_by_id(task_id)
    if task:
      task.mark_completed()
      self.storage.save_tasks(self.tasks)  # Save after marking
      return True
    print(f"Task {task_id} not found.")
    return False


if __name__ == "__main__":
  file_storage = FileTaskStorage("my_tasks.txt")
  manager = TaskManager(file_storage)  # ส่ง FileTaskStorage เข้าเป็นอาร์กิวเมนต์

  manager.list_tasks()
  manager.add_task("Review SOLID Principles", "2024-08-10", priority="high")
  manager.add_task("Prepare for Final Exam", "2024-08-15", priority="medium")
  manager.list_tasks()
  manager.mark_task_completed(1)
  manager.list_tasks()