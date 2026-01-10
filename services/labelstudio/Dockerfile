# Use the official Label Studio image as base
FROM heartexlabs/label-studio:latest


# Entry point: run HTTP server + Label Studio
# We'll use bash -c as in your compose
COPY setup_http_dataset.sh /setup_http_dataset.sh
RUN chmod +x /setup_http_dataset.sh

# Default command: serve dataset + start LS
CMD ["/bin/bash", "/setup_http_dataset.sh"]