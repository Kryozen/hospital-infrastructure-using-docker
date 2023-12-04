# Use a small web server as the base image
FROM nginx:alpine

# Copy HTML, JavaScript, CSS, and image files to the web server's root directory
COPY main.html /usr/share/nginx/html/
COPY script.js /usr/share/nginx/html/
COPY style.css /usr/share/nginx/html/
COPY background.jpg /usr/share/nginx/html/

# Expose port 80 (default HTTP port)
EXPOSE 80

# Command to start the nginx web server
CMD ["nginx", "-g", "daemon off;"]
