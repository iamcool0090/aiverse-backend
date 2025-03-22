# Aiverse Backend

Aiverse Backend is a Python-based backend service for the Aiverse project. It provides the core functionality and APIs to support the Aiverse application.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Cloudflare Tunnels](#cloudflare-tunnels)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install the required dependencies, run the following command:

```sh
pip install -r requirements.txt
```

## Usage

To start the backend service, use:

```sh
python main.py
```

Ensure all environment variables are set correctly before running the service.

## Cloudflare Tunnels

We use Cloudflare Tunnels (CFTunnels) to securely expose our backend service to the internet without opening ports on our server. This allows us to keep our infrastructure secure while making the API accessible from anywhere.

To set up and run Cloudflare Tunnel, follow these steps:

1. Install Cloudflare Tunnel:
   ```sh
   cloudflared tunnel install
   ```
2. Authenticate with Cloudflare:
   ```sh
   cloudflared tunnel login
   ```
3. Create and configure a tunnel:
   ```sh
   cloudflared tunnel create aiverse-backend
   ```
4. Run the tunnel:
   ```sh
   cloudflared tunnel run aiverse-backend
   ```

This setup ensures a reliable and secure connection between the backend and external services.

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`feature-branch`).
3. Commit your changes.
4. Push to your fork and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

