# Pulled Apr 24, 2023
FROM python:3.8@sha256:6aea47c16a4fe8a30f184060a2347caa24ea156b224041543fdc6b901dbec699
RUN apt-get update && apt-get install -y cpanminus && cpanm --notest IPC::Run
ENV OPENLAW_BOT_DIR=/usr/local/lib/openlaw-bot
ARG OPENLAW_BOT_VERSION=v0.2.22
RUN TEMP_DIR=$(mktemp -d) \
    && wget "https://git.org.il/resource-il/openlaw-bot/-/releases/${OPENLAW_BOT_VERSION}/downloads/openlaw-bot.tar.gz" -O "${TEMP_DIR}/openlaw-bot.tar.gz" \
    && mkdir -p "${OPENLAW_BOT_DIR}" \
    && tar xf "${TEMP_DIR}/openlaw-bot.tar.gz" -C "${OPENLAW_BOT_DIR}" \
    && rm -Rf "${TEMP_DIR}" \
    && apt-get clean \
    && rm -Rf /var/lib/apt/lists/*
WORKDIR /srv
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt && rm requirements.txt
COPY djang ./djang
WORKDIR /srv/djang
ENTRYPOINT ["/srv/djang/entrypoint.sh"]
