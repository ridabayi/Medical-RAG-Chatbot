# 🧩 Use the official Jenkins LTS image as base
FROM jenkins/jenkins:lts

# ⚙️ Switch to root user to install Docker dependencies
USER root

# 🐳 Install Docker CLI inside Jenkins container
RUN apt-get update -y && \
    apt-get install -y apt-transport-https ca-certificates curl gnupg && \
    # Add Docker official GPG key
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
    # Add Docker APT repository (match Debian trixie)
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian trixie stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update -y && \
    apt-get install -y docker-ce docker-ce-cli containerd.io && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 👤 Add Jenkins user to Docker group (create if needed)
RUN groupadd -f docker && \
    usermod -aG docker jenkins

# 📦 Prepare Docker volume for Docker-in-Docker (optional)
RUN mkdir -p /var/lib/docker
VOLUME /var/lib/docker

# 👇 Switch back to Jenkins user
USER jenkins
