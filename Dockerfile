FROM python:3.12.3
LABEL authors="lying"
# Make sure to not install recommends and to clean the
# install to minimize the size of the container as much as possible.

# Set the working directory within the container
WORKDIR /app

# Copy necessary files to the container
COPY requirements.txt .
COPY main.py .
COPY download_models.py .

# Create a virtual environment in the container
RUN python3 -m venv .venv

# Activate the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

    # Install Python dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt && \
    # Get the models from Hugging Face to bake into the container
    python3 download_models.py \

RUN pip3 install torch torchvision torchaudio -f https://download.pytorch.org/whl/cu111/torch_stable.html

# Make port 6000 available to the world outside this container
EXPOSE 6000

ENTRYPOINT [ "python3" ]

# Run scip.py when the container launches
CMD [ "main.py" ]