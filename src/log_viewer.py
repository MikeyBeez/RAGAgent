import re
from datetime import datetime, timedelta
import argparse

def load_log(filepath):
    with open(filepath, 'r') as f:
        return f.readlines()

def filter_by_date(logs, start_date, end_date):
    filtered = []
    for log in logs:
        match = re.match(r'(\d{4}-\d{2}-\d{2})', log)
        if match:
            log_date = datetime.strptime(match.group(1), '%Y-%m-%d')
            if start_date <= log_date <= end_date:
                filtered.append(log)
    return filtered

def filter_by_type(logs, msg_type):
    return [log for log in logs if msg_type in log]

def search_logs(logs, keyword):
    return [log for log in logs if keyword.lower() in log.lower()]

def display_logs(logs):
    for log in logs:
        print(log.strip())

def main():
    parser = argparse.ArgumentParser(description='Log file viewer')
    parser.add_argument('--file', default='chat_ollama.log', help='Log file path')
    parser.add_argument('--start-date', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', help='End date (YYYY-MM-DD)')
    parser.add_argument('--type', help='Message type (INFO, ERROR, etc.)')
    parser.add_argument('--search', help='Keyword to search')
    
    args = parser.parse_args()
    
    logs = load_log(args.file)
    
    if args.start_date and args.end_date:
        start = datetime.strptime(args.start_date, '%Y-%m-%d')
        end = datetime.strptime(args.end_date, '%Y-%m-%d')
        logs = filter_by_date(logs, start, end)
    
    if args.type:
        logs = filter_by_type(logs, args.type)
    
    if args.search:
        logs = search_logs(logs, args.search)
    
    display_logs(logs)

if __name__ == "__main__":
    main()
