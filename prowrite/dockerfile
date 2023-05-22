FROM python:3.10

# Copy the source code and requirements
WORKDIR /prowrite
COPY templates/ /prowrite/templates/
COPY requirements.txt /prowrite
COPY combined_app.py /prowrite

# Install Python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Run the application
CMD ["python3", "combined_app.py"]
