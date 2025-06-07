import json
import argparse
import os
from dataclasses import dataclass, asdict
from typing import List

DATA_FILE = 'goals.json'

@dataclass
class Goal:
    id: int
    title: str
    description: str = ''
    due: str = ''
    completed: bool = False


def load_goals() -> List[Goal]:
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return [Goal(**item) for item in data]


def save_goals(goals: List[Goal]):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump([asdict(g) for g in goals], f, ensure_ascii=False, indent=2)


def add_goal(args):
    goals = load_goals()
    next_id = (max((g.id for g in goals), default=0) + 1)
    goal = Goal(id=next_id, title=args.title, description=args.description or '', due=args.due or '')
    goals.append(goal)
    save_goals(goals)
    print(f"Added goal {goal.id}: {goal.title}")


def list_goals(args):
    goals = load_goals()
    if not goals:
        print('No goals found.')
        return
    for g in goals:
        status = '✓' if g.completed else ' '
        due = f' (due {g.due})' if g.due else ''
        print(f"[{status}] {g.id}: {g.title}{due}")
        if g.description:
            print(f"    {g.description}")


def complete_goal(args):
    goals = load_goals()
    for g in goals:
        if g.id == args.id:
            g.completed = True
            save_goals(goals)
            print(f"Completed goal {g.id}: {g.title}")
            return
    print('Goal not found.')


def delete_goal(args):
    goals = load_goals()
    new_goals = [g for g in goals if g.id != args.id]
    if len(new_goals) == len(goals):
        print('Goal not found.')
        return
    save_goals(new_goals)
    print(f'Deleted goal {args.id}')


def progress(args):
    goals = load_goals()
    if not goals:
        print('No goals found.')
        return
    total = len(goals)
    completed = sum(1 for g in goals if g.completed)
    print(f'Progress: {completed}/{total} goals completed.')


def main():
    parser = argparse.ArgumentParser(description='Simple Goal Tracking App')
    sub = parser.add_subparsers(dest='command')

    add = sub.add_parser('add', help='Add a new goal')
    add.add_argument('title')
    add.add_argument('-d', '--description')
    add.add_argument('--due')
    add.set_defaults(func=add_goal)

    list_cmd = sub.add_parser('list', help='List goals')
    list_cmd.set_defaults(func=list_goals)

    comp = sub.add_parser('complete', help='Mark goal as complete')
    comp.add_argument('id', type=int)
    comp.set_defaults(func=complete_goal)

    delete = sub.add_parser('delete', help='Delete a goal')
    delete.add_argument('id', type=int)
    delete.set_defaults(func=delete_goal)

    prog = sub.add_parser('progress', help='Show progress')
    prog.set_defaults(func=progress)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

