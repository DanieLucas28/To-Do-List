# ## TO-DO program from jetbrains academy. is a program that creates task lists with deadlines, being able to save
# and manipulate the information in a database using sqlalchemy.

from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

todaydate = str(datetime.today().day) + " " + datetime.today().strftime('%b')
# print(rows)

end = False
while not end:

    print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit""")

    user = input()
    if user == '0':
        print("\nBye!")
        break

    elif user == '1':
        rows = session.query(Task).filter(Task.deadline == datetime.today().date()).all()
        if len(rows) == 0:
            print("")
            print(f"Today {todaydate}:")
            print("Nothing to do!\n")

        else:
            print("")
            print(f"Today {todaydate}:")
            for x in range(len(rows)):
                print(f"{rows[x].id}. {rows[x].task}")
            print("")

    elif user == '5':
        print("")
        print("Enter task")
        task = input()
        print("Enter deadline")
        deadline = input()
        deadline = datetime.strptime(deadline, '%Y-%m-%d')
        new_row = Task(task=task, deadline=deadline)
        session.add(new_row)
        session.commit()
        print("The task has been added!")
        print("")

    elif user == '3':
        rows = session.query(Task).order_by(Task.deadline).all()
        print("")
        print("All tasks:")
        for x in range(len(rows)):
            print(f"{rows[x].id}. {rows[x].task}. {rows[x].deadline.day} {rows[x].deadline.strftime('%b')}")
        print("")

    elif user == '2':
        for x in range(7):
            newline = datetime.today() + timedelta(days=x)
            todaydate = str(newline.day) + " " + newline.strftime('%b')
            print(f"{newline.strftime('%A')} {todaydate}:")
            rows = session.query(Task).filter(Task.deadline == newline.date()).all()
            if len(rows) == 0:
                print("Nothing to do!\n")
            else:
                for y in range(len(rows)):
                    print(f"{rows[y].id}. {rows[y].task}\n")

    elif user == '6':
        rows = session.query(Task).order_by(Task.deadline).all()
        print("")
        print("Choose the number of the task you want to delete:")
        for x in range(len(rows)):
            print(f"{rows[x].id}. {rows[x].task}. {rows[x].deadline.day} {rows[x].deadline.strftime('%b')}")
        chosen = int(input())
        specific = rows[chosen-1]
        session.delete(specific)
        session.commit()
        print("The task has been deleted!\n")

    elif user == '4':
        rows = session.query(Task).filter(Task.deadline < datetime.today().date()).all()
        print("")
        print("Missed tasks:")
        if len(rows) == 0:
            print("Nothing is missed!\n")
        else:
            for x in range(len(rows)):
                print(f"{rows[x].id}. {rows[x].task}. {rows[x].deadline.day} {rows[x].deadline.strftime('%b')}")
            print("")
