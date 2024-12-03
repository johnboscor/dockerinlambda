# Update the installed packages and package cache on your instance
sudo yum update -y
# Install the most recent Docker Community Edition package
sudo amazon-linux-extras install docker
# Start the Docker service
sudo service docker start
# Add the ec2-user to the docker group so you can execute Docker #commands without using sudo.
sudo usermod -a -G docker ec2-user

# Ensure docker daemon restarts on system reboot.
sudo systemctl enable docker.service

# Make container automatically restarting
docker update --restart unless-stopped <container id or name>
# Make all containers automatically restarting
docker update --restart unless-stopped $(docker ps -q)