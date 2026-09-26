# GitHub Actions to EC2 CI/CD demo

A small, standalone Flask app that demonstrates a practical CI/CD pipeline. GitHub Actions runs application tests, builds and smoke checks a Docker image, then transfers that image to Ubuntu EC2 over SSH and replaces the running container. Pushes to `main` deploy automatically.

## Run locally

Install Python 3.12 and Docker Desktop, then from this folder run:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m pytest -q
docker build -t ec2-cicd-demo .
docker run --rm -p 8000:8000 ec2-cicd-demo
```

Open `http://localhost:8000/`, `http://localhost:8000/health`, or `http://localhost:8000/api/message`.

## Prepare an Ubuntu EC2 instance

1. Launch an Ubuntu instance with a public IP and a key pair you control.
2. In its security group, allow inbound TCP **80** for the app. Allow TCP **22** only from a trusted source where practical. The GitHub hosted runner has changing IP addresses, so a source-IP allowlist may require a self-hosted runner or another networking setup.
3. Copy `setup-ec2-docker.sh` to the instance and run it. This disables host Nginx if present, installs Docker, and grants the Ubuntu login user Docker access:

   ```powershell
   scp setup-ec2-docker.sh ubuntu@EC2_PUBLIC_IP:/home/ubuntu/
   ssh ubuntu@EC2_PUBLIC_IP "chmod +x setup-ec2-docker.sh && ./setup-ec2-docker.sh"
   ```

4. Disconnect and reconnect so the Docker group change takes effect. Verify `docker ps` works without `sudo`.

The Docker group grants root-level control of the instance. Keep the EC2 SSH private key secret and use a dedicated deployment key where possible.

## Create a GitHub repository and add secrets

Create a new, empty GitHub repository for this project. From this folder, initialize and push the project (replace the URL with your repository URL):

```powershell
git init
git add .
git commit -m "Add EC2 GitHub Actions CI/CD demo"
git branch -M main
git remote add origin https://github.com/YOUR_ACCOUNT/YOUR_REPOSITORY.git
git push -u origin main
```

Before pushing, add these repository secrets under **Settings > Secrets and variables > Actions**:

| Secret | Value |
| --- | --- |
| `EC2_HOST` | EC2 public IPv4 address or DNS name |
| `EC2_USER` | `ubuntu` for the standard Ubuntu AMI |
| `EC2_SSH_KEY` | Contents of the private key that matches the EC2 key pair |
| `EC2_KNOWN_HOSTS` | Verified `known_hosts` entry for the EC2 host |

Get the server host key through a trusted channel and verify its fingerprint before saving the `known_hosts` entry. The workflow checks this pinned host key and does not turn off SSH host verification. Never commit private keys or add them to app configuration files.

After the secrets are set, every push to `main` runs tests, builds the image, smoke checks it, and deploys it. You can also start the workflow manually from the GitHub Actions tab. A failed test or image check prevents deployment. The deployed app is available at `http://EC2_PUBLIC_IP/`.

The workflow keeps one container named `ec2-cicd-demo` and replaces it on each successful deployment. This demo uses HTTP; for a public production service, add HTTPS, a domain, monitoring, and an appropriate rollback and data strategy.
