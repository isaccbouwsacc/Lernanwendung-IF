import os
import subprocess
import sys
import time
import re
import requests


def start_proxy():
    print("Starting secure proxy server...")

    # Start the proxy as a subprocess
    proxy_process = subprocess.Popen(
        [sys.executable, ".\\modules\\secure_proxy.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    # Wait for the proxy to start and extract the API key
    api_key = None
    for line in iter(proxy_process.stdout.readline, ''):
        print(f"Proxy: {line.strip()}")
        # Extract API key from output
        match = re.search(r"API key: ([a-f0-9]+)", line)
        if match:
            api_key = match.group(1)
            break
        # If we've waited too long, something might be wrong
        if "Running" in line:
            break

    if not api_key:
        print("Warning: Could not extract API key from proxy output.")
        # Try to read from the first few lines of output
        output = proxy_process.stdout.read(1000)
        match = re.search(r"API key: ([a-f0-9]+)", output)
        if match:
            api_key = match.group(1)
        else:
            print("Failed to start proxy or extract API key.")
            proxy_process.terminate()
            return None, None, None

    # Configure the endpoint
    endpoint = "http://127.0.0.1:8080"

    print(f"Proxy started successfully!")
    print(f"API Key: {api_key}")
    print(f"Endpoint: {endpoint}")

    # Wait a moment to ensure the proxy is fully running
    time.sleep(1)

    # Test the connection
    try:
        response = requests.get(f"{endpoint}/v1", headers={"Authorization": f"Bearer {api_key}"})
        if response.status_code != 200:
            print(f"Warning: Proxy test returned status code {response.status_code}")
    except Exception as e:
        print(f"Warning: Could not connect to proxy: {e}")

    return api_key, endpoint, proxy_process


def main():
    # Get the virtual environment activation command
    if os.name == 'nt':  # Windows
        activate_cmd = ['.venv\\Scripts\\activate.bat']
    else:
        quit()

    # Ask if user wants to use API mode
    use_api = input("Do you want to use API mode? (y/n) ").lower().startswith('y')

    # Ask if user wants to enable sharing
    use_share = input("Do you want to enable sharing (public URL)? (y/n) ").lower().startswith('y')

    # Ask if user wants to set up authentication
    use_auth = input("Do you want to set up authentication? (y/n) ").lower().startswith('y')

    username = None
    password = None
    if use_auth:
        username = input("Enter username: ")
        password = input("Enter password: ")
        if not username or not password:
            print("Username or password not provided. Authentication will be disabled.")
            use_auth = False

    proxy_process = None
    launch_args = []

    if use_api:
        # Ask if user wants to launch the secure proxy
        use_proxy = input("Do you want to launch the secure proxy? (y/n) ").lower().startswith('y')

        if use_proxy:
            # Start the proxy and get the API key and endpoint
            api_key, api_endpoint, proxy_process = start_proxy()

            if api_key and api_endpoint:
                launch_args = ['--api-key', api_key, '--api-endpoint', api_endpoint]
                print(f"Using API mode with proxy:")
                print(f"* API Key: {api_key}")
                print(f"* API Endpoint: {api_endpoint}")
            else:
                print("Failed to start proxy. Falling back to manual API configuration.")
                use_proxy = False

        if not use_proxy:
            # Manual API configuration
            api_key = input("Enter API key: ")
            api_endpoint = input("Enter API endpoint: ")

            if api_key and api_endpoint:
                launch_args = ['--api-key', api_key, '--api-endpoint', api_endpoint]
                print(f"Using API mode with:")
                print(f"* API Key: {api_key}")
                print(f"* API Endpoint: {api_endpoint}")
            else:
                print("API key or endpoint not provided. Falling back to local mode.")
                use_api = False

    if not use_api:
        print("Running in local mode without API.")

    # Add share flag if selected
    if use_share:
        launch_args.append('--share')
        print("Sharing enabled. A public URL will be generated.")

    # Add authentication if selected
    if use_auth:
        launch_args.extend(['--username', username, '--password', password])
        print(f"Authentication enabled with username: {username}")

    # Launch the application
    print("Launching application...")
    webui_process = None
    try:
        webui_process = subprocess.Popen([sys.executable, ".\\modules\\webui.py"] + launch_args)
        webui_process.wait()
    except KeyboardInterrupt:
        print("\nReceived keyboard interrupt. Shutting down...")
    finally:
        # Clean up processes
        if webui_process and webui_process.poll() is None:
            print("Terminating WebUI process...")
            webui_process.terminate()
            webui_process.wait(timeout=5)

        if proxy_process and proxy_process.poll() is None:
            print("Terminating proxy process...")
            proxy_process.terminate()
            proxy_process.wait(timeout=5)

        print("Application closed.")


if __name__ == "__main__":
    main()
