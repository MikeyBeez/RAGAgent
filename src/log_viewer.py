import re
from datetime import datetime
import argparse
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

def load_log(filepath):
    with open(filepath, 'r') as f:
        return f.readlines()

def parse_log_entry(log):
    match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - (\w+) - (.+)', log)
    if match:
        return {
            'timestamp': datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S,%f'),
            'level': match.group(2),
            'message': match.group(3)
        }
    return None

def filter_logs(logs, start_date=None, end_date=None, log_type=None, keyword=None):
    filtered = []
    for log in logs:
        entry = parse_log_entry(log)
        if entry:
            if start_date and entry['timestamp'].date() < start_date:
                continue
            if end_date and entry['timestamp'].date() > end_date:
                continue
            if log_type and entry['level'] != log_type:
                continue
            if keyword and keyword.lower() not in entry['message'].lower():
                continue
            filtered.append(entry)
    return filtered

def group_by_session(logs):
    sessions = []
    current_session = []
    for log in logs:
        if "Starting chat application" in log['message']:
            if current_session:
                sessions.append(current_session)
            current_session = [log]
        else:
            current_session.append(log)
    if current_session:
        sessions.append(current_session)
    return sessions

def generate_statistics(logs):
    total_logs = len(logs)
    error_count = sum(1 for log in logs if log['level'] == 'ERROR')
    unique_users = set(log['message'].split()[2] for log in logs if "User" in log['message'] and "started a new session" in log['message'])
    return {
        'total_logs': total_logs,
        'error_count': error_count,
        'unique_users': len(unique_users)
    }

def display_report(logs, console):
    sessions = group_by_session(logs)
    stats = generate_statistics(logs)

    console.print(Panel(f"Total logs: {stats['total_logs']}, Errors: {stats['error_count']}, Unique users: {stats['unique_users']}", title="Statistics"))

    for i, session in enumerate(sessions, 1):
        table = Table(title=f"Session {i}")
        table.add_column("Timestamp", style="cyan")
        table.add_column("Level", style="magenta")
        table.add_column("Message", style="green")

        for log in session:
            level_style = "bold red" if log['level'] == 'ERROR' else "magenta"
            table.add_row(
                log['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
                Text(log['level'], style=level_style),
                log['message']
            )

        console.print(table)
        console.print()

def main():
    parser = argparse.ArgumentParser(description='Enhanced Log Viewer')
    parser.add_argument('--file', default='chat_ollama.log', help='Log file path')
    parser.add_argument('--start-date', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', help='End date (YYYY-MM-DD)')
    parser.add_argument('--type', help='Log level (INFO, ERROR, etc.)')
    parser.add_argument('--search', help='Keyword to search')
    
    args = parser.parse_args()
    
    logs = load_log(args.file)
    
    start_date = datetime.strptime(args.start_date, '%Y-%m-%d').date() if args.start_date else None
    end_date = datetime.strptime(args.end_date, '%Y-%m-%d').date() if args.end_date else None
    
    filtered_logs = filter_logs(logs, start_date, end_date, args.type, args.search)
    
    console = Console()
    display_report(filtered_logs, console)

if __name__ == "__main__":
    main()
