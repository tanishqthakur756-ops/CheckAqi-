# Docker has specific installation instructions for each operating system.
# Please refer to the official documentation at https://docker.com/get-started/

# Pull the Node.js Docker image:
docker pull node:26-slim

# Create a Node.js container and start a Shell session:
docker run -it --rm --entrypoint sh node:26-slim

# Verify the Node.js version:
node -v # Should print "v26.8.1".

# Verify npm version:
npm -v # Should print "11.19.0".
