
import psycopg2
from datetime import datetime

conn = psycopg2.connect(
    dbname="dbname",
    user="user",          
    password="password",  
    host="host",
    port="port"
)

cur = conn.cursor()

def add_task(description, due_date):
    try:
        due = datetime.strptime(due_date, "%Y-%m-%d").date()
        cur.execute(
            "INSERT INTO tasks (description, due_date) VALUES (%s, %s)",
            (description, due)
        )
        conn.commit()
        print("✅ Task added successfully!")
    except Exception as e:
        conn.rollback()  # 🚨 تصحيح المعاملة
        print("❌ Error adding task:", e)

def update_task(task_id, new_description):
    try:
        cur.execute(
            "UPDATE tasks SET description = %s WHERE id = %s",
            (new_description, task_id)
        )
        conn.commit()
        print("✅ Task updated successfully!")
    except Exception as e:
        conn.rollback()
        print("❌ Error updating task:", e)

def delete_task(task_id):
    try:
        cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        conn.commit()
        print("🗑️ Task deleted successfully!")
    except Exception as e:
        conn.rollback()
        print("❌ Error deleting task:", e)

def list_tasks():
    try:
        cur.execute("SELECT id, description, due_date, completed FROM tasks ORDER BY id")
        rows = cur.fetchall()
        print("\n📝 To-Do List:")
        if not rows:
            print("📭 No tasks found.")
        for row in rows:
            status = "✅" if row[3] else "❌"
            print(f"{row[0]}. {row[1]} (Due: {row[2]}) {status}")
        print()
    except Exception as e:
        print("❌ Error listing tasks:", e)

def main():
    while True:
        print("\n--- To-Do List ---")
        print("1. Add Task")
        print("2. Update Task")
        print("3. Delete Task")
        print("4. Show All Tasks")
        print("5. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            desc = input("Task description: ")
            date = input("Due date (YYYY-MM-DD): ")
            add_task(desc, date)
        elif choice == "2":
            try:
                task_id = int(input("Task ID to update: "))
                new_desc = input("New description: ")
                update_task(task_id, new_desc)
            except ValueError:
                print("❌ Invalid input.")
        elif choice == "3":
            try:
                task_id = int(input("Task ID to delete: "))
                delete_task(task_id)
            except ValueError:
                print("❌ Invalid input.")
        elif choice == "4":
            list_tasks()
        elif choice == "5":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
