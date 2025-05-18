from rich.console import Console
from rich.tree import Tree
from db import session
from models import Employee

console = Console()

def build_tree(emp: Employee, tree: Tree):
    branch = tree.add(f"{emp.full_name} — {emp.position}")
    for sub in emp.subordinates:
        build_tree(sub, branch)

def show_hierarchy():
    ceo = session.query(Employee).filter_by(position='CEO').first()
    tree = Tree(f"{ceo.full_name} — {ceo.position}")
    for sub in ceo.subordinates:
        build_tree(sub, tree)
    console.print(tree)

def run():
    while True:
        console.print("\n[bold cyan]Каталог сотрудников[/bold cyan]")
        console.print("1. Показать иерархию сотрудников")
        console.print("2. Выход")
        choice = input("Выберите действие: ")
        if choice == '1':
            show_hierarchy()
        elif choice == '2':
            break
        else:
            console.print("[red]Неверный выбор[/red]")

if __name__ == "__main__":
    run()
