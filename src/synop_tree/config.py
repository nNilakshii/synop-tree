"""Configuration: secrets from the environment / `.env`, everything else from `config.yaml` (§15).

Model IDs and budget caps have no defaults on purpose: they must come from `config.yaml`.
"""

import os
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_CONFIG_PATH = Path("config.yaml")
DEFAULT_ENV_FILE = Path(".env")


class _Section(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class ModelsConfig(_Section):
    leaf: str
    upper: str
    eval_agent_main: str
    eval_agent_weak: str


class SummarizeConfig(_Section):
    concurrency: int = Field(default=8, ge=1)
    max_leaf_tokens: int = Field(default=3000, ge=1)
    max_children: int = Field(default=40, ge=1)
    trivial_max_body_lines: int = Field(default=3, ge=0)
    batch_mode: bool = False
    prompt_versions: dict[str, str] = Field(
        default_factory=lambda: {k: "v1" for k in ("function", "class", "file", "dir", "repo")}
    )


class UpdateConfig(_Section):
    default_policy: Literal["eager", "threshold", "debounced"] = "eager"
    threshold_tau: float = Field(default=0.92, ge=0, le=1)
    full_rebuild_ratio: float = Field(default=0.30, ge=0, le=1)


class EmbeddingsConfig(_Section):
    provider: Literal["local", "voyage"] = "local"
    model: str = "BAAI/bge-small-en-v1.5"
    dim: int = Field(default=384, ge=1)


class McpConfig(_Section):
    max_output_tokens: int = Field(default=1200, ge=1)
    read_code_max_lines: int = Field(default=200, ge=1)
    list_default_limit: int = Field(default=30, ge=1, le=50)


class BudgetConfig(_Section):
    max_usd_per_build: float = Field(gt=0)
    max_usd_per_eval_run: float = Field(gt=0)
    max_usd_total: float = Field(gt=0)


class Secrets(BaseSettings):
    """Read from real env vars first, then the `.env` file. Values are masked in repr/logs."""

    model_config = SettingsConfigDict(extra="ignore", frozen=True)

    anthropic_api_key: SecretStr | None = None
    database_url: SecretStr | None = None
    database_url_readonly: SecretStr | None = None
    synop_token: SecretStr | None = None
    synop_cursor_secret: SecretStr | None = None
    voyage_api_key: SecretStr | None = None


SECRET_ENV_VARS: tuple[str, ...] = tuple(name.upper() for name in Secrets.model_fields)


class Config(_Section):
    workspace_dir: Path = Path("./workspace")
    models: ModelsConfig
    summarize: SummarizeConfig = SummarizeConfig()
    update: UpdateConfig = UpdateConfig()
    embeddings: EmbeddingsConfig = EmbeddingsConfig()
    mcp: McpConfig = McpConfig()
    budget: BudgetConfig
    ignore: list[str] = Field(default_factory=list[str])
    secrets: Secrets


def load_config(
    path: Path | None = None,
    env_file: Path | None = DEFAULT_ENV_FILE,
) -> Config:
    """Load `config.yaml` (or `$SYNOP_CONFIG`) plus secrets. `env_file=None` skips `.env`."""
    path = path or Path(os.environ.get("SYNOP_CONFIG", DEFAULT_CONFIG_PATH))
    raw: Any = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise ValueError(f"{path}: top level must be a mapping")
    data: dict[str, Any] = dict(raw)  # pyright: ignore[reportUnknownArgumentType]
    if "secrets" in data:
        raise ValueError(f"{path}: secrets belong in .env, not config.yaml")
    secrets = Secrets(_env_file=env_file)  # pyright: ignore[reportCallIssue]
    return Config.model_validate({**data, "secrets": secrets})
