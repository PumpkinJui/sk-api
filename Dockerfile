FROM --platform=linux/arm64 python:3.8-slim AS builder

RUN apt-get update && \
    apt-get install -y binutils patchelf && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --upgrade pip && \
    pip install pyinstaller && \
    pyinstaller --clean --onefile \
    -n sk-api sk_chat.py

FROM --platform=linux/arm64 alpine:3.18 AS termux_builder

RUN apk add --no-cache patchelf

COPY --from=builder /app/dist/sk-api /tmp/

RUN patchelf --set-interpreter /data/data/com.termux/files/usr/lib/ld-linux-aarch64.so.1 \
    --set-rpath "/data/data/com.termux/files/usr/lib" \
    /tmp/sk-api

FROM scratch AS export
COPY --from=termux_builder /tmp/sk-api /output/sk-api
