FROM python:3.13.11-trixie AS builder

WORKDIR /usr/src/app
ENV PATH="/opt/venv/bin:$PATH"
COPY .python-version pyproject.toml uv.lock /usr/src/app/
RUN python -m venv /opt/venv && \
    pip install uv && \
    uv export --no-dev --format requirements-txt -o requirements.txt
#    uv pip compile pyproject.toml -o requirements.txt

FROM python:3.13.11-trixie

WORKDIR /usr/src/app
ENV PATH="/opt/venv/bin:$PATH"
COPY --from=builder /usr/src/app/requirements.txt /usr/src/app/requirements.txt
RUN python -m venv /opt/venv && \
    pip install -r requirements.txt && \
    rm requirements.txt
COPY . /usr/src/app
EXPOSE 8000
CMD ["python3", "./main.py"]
