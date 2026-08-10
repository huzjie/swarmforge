"""
Example: Using the SwarmForge REST API.
"""
import requests


BASE_URL = "http://localhost:8000"


def check_health():
    resp = requests.get(f"{BASE_URL}/health")
    print(f"Health: {resp.json()}")


def create_agent(name, role="worker"):
    resp = requests.post(f"{BASE_URL}/api/v1/agents/", json={
        "name": name,
        "role": role,
        "description": f"{name} agent",
        "capabilities": ["general"],
    })
    print(f"Created agent: {resp.json()}")


def list_agents():
    resp = requests.get(f"{BASE_URL}/api/v1/agents/")
    for agent in resp.json():
        print(f"  Agent: {agent['name']} ({agent['role']}) - {agent['model']}")


def create_swarm(name, topology="parallel"):
    resp = requests.post(f"{BASE_URL}/api/v1/swarms/", json={
        "name": name,
        "topology": topology,
        "agent_configs": [
            {"name": f"{name}-worker-1", "role": "worker", "capabilities": ["search"]},
            {"name": f"{name}-worker-2", "role": "worker", "capabilities": ["analysis"]},
        ],
    })
    print(f"Created swarm: {resp.json()}")


def run_swarm(swarm_name, task):
    resp = requests.post(f"{BASE_URL}/api/v1/swarms/{swarm_name}/run", json={
        "task": task,
    })
    print(f"Swarm run: {resp.json()}")


if __name__ == "__main__":
    check_health()
    create_agent("helper", "worker")
    list_agents()
    create_swarm("demo-team", "parallel")
    run_swarm("demo-team", "Summarize today's AI news")
