#!/usr/bin/env python3

import argparse
from jinja2 import Environment, FileSystemLoader

def generate_docker_compose(num_workers):
    # Load the Jinja2 template
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('docker-compose.template.yml')

    # Render the template with the desired number of workers
    docker_compose_yml = template.render(num_workers=num_workers)

    # Save the rendered Docker Compose file
    with open('docker-compose.yml', 'w') as f:
        f.write(docker_compose_yml)

    print("Docker Compose file generated successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a Docker Compose file with a specified number of Celery workers.")
    parser.add_argument('num_workers', type=int, help="Number of Celery workers to generate")

    args = parser.parse_args()
    generate_docker_compose(args.num_workers)
