FROM python:3.13.11-trixie AS builder

ENV PATH="/venv/bin:$PATH"
RUN python -m venv /venv && \
    pip install --upgrade pip && \
    pip install uv

WORKDIR /app
COPY .python-version pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --compile-bytecode --link-mode=copy

FROM gcr.io/distroless/python3-debian13
WORKDIR /app
ENV PYTHONPATH="/.venv/lib/python3.13/site-packages" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
COPY --from=builder /app/.venv /.venv
COPY . /app
EXPOSE 8000
CMD ["main.py"]
