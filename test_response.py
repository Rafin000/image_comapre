import requests
import argparse

def get_task_result(task_id: str):
    url = f'http://103.209.42.222:8000/task_result/{task_id}'
    headers = {'accept': 'application/json'}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Unable to fetch task result", "status_code": response.status_code}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get task result from the server.")
    parser.add_argument("task_id", type=str, help="Task ID to retrieve the result for")
    
    args = parser.parse_args()
    
    result = get_task_result(args.task_id)
    print(result)
