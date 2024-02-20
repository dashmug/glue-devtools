FROM amazon/aws-glue-libs:glue_libs_4.0.0_image_01

# Runtime environment variable so our Makefile can check if it is
# running in a container.
ENV PLATFORM="docker"

# Arguments for passing the host user:group to the container.
ARG USER_ID=1000

# Switch to root to be able to make changes in the container filesystem.
USER root

# Install latest version of awscli.
RUN yum remove awscli -y \
  && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
  && unzip awscliv2.zip \
  && ./aws/install \
  # Change UID of glue_user to be the same as host user. This allows
  # JupyterLab to write to the host system as glue_user.
  && usermod -u $USER_ID glue_user \
  # Clean up /tmp which may already have glue_user-owned files with the
  # old UID.
  && rm -rf /tmp/*

# Switch to glue_user to be able to make changes for the user itself.
USER glue_user

# Copy requirements file that contains tooling.
WORKDIR /home/glue_user/workspace
COPY requirements.txt .

RUN pip3 install --no-cache-dir --user --upgrade pip==24.0 \
  # Install dev requirements.
  && pip3 install --no-cache-dir --user -r requirements.txt  \
  # Prepare a /tmp directory needed by Spark to start.
  && mkdir -p /tmp/spark-events
