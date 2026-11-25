from pathlib import Path

import pytest
from pydantic import ValidationError

from synop_tree.config import SECRET_ENV_VARS, load_config

MINIMAL_YAML = """\
workspace_dir: ./ws
models:
  leaf: model-leaf
  upper: model-upper
  eval_agent_main: model-main
  eval_agent_weak: model-weak
budget:
  max_usd_per_build: 1.5
  max_usd_per_eval_run: 2.0
  max_usd_total: 3.0
summarize:
  concurrency: 4
"""


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in SECRET_ENV_VARS:
        monkeypatch.delenv(name, raising=False)


def _write(tmp_path: Path, yaml_text: str, env_text: str = "") -> tuple[Path, Path]:
    cfg, env = tmp_path / "config.yaml", tmp_path / ".env"
    cfg.write_text(yaml_text)
    env.write_text(env_text)
    return cfg, env


def test_loads_yaml_and_env_file(tmp_path: Path) -> None:
    cfg, env = _write(tmp_path, MINIMAL_YAML, "ANTHROPIC_API_KEY=sk-test-123\n")

    config = load_config(cfg, env_file=env)

    assert config.workspace_dir == Path("./ws")
    assert config.models.leaf == "model-leaf"
    assert config.summarize.concurrency == 4
    assert config.summarize.max_children == 40  # default kept
    assert config.budget.max_usd_total == 3.0
    assert config.secrets.anthropic_api_key is not None
    assert config.secrets.anthropic_api_key.get_secret_value() == "sk-test-123"


def test_real_env_var_beats_env_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    cfg, env = _write(tmp_path, MINIMAL_YAML, "SYNOP_TOKEN=from-file\n")
    monkeypatch.setenv("SYNOP_TOKEN", "from-env")

    token = load_config(cfg, env_file=env).secrets.synop_token

    assert token is not None
    assert token.get_secret_value() == "from-env"


def test_secrets_are_masked_in_repr(tmp_path: Path) -> None:
    cfg, env = _write(tmp_path, MINIMAL_YAML, "ANTHROPIC_API_KEY=sk-test-123\n")

    assert "sk-test-123" not in repr(load_config(cfg, env_file=env))


def test_models_are_required(tmp_path: Path) -> None:
    cfg, env = _write(tmp_path, MINIMAL_YAML.replace("  leaf: model-leaf\n", ""))

    with pytest.raises(ValidationError, match="leaf"):
        load_config(cfg, env_file=env)


def test_unknown_key_is_rejected(tmp_path: Path) -> None:
    cfg, env = _write(tmp_path, MINIMAL_YAML + "sumarize_typo: 1\n")

    with pytest.raises(ValidationError, match="sumarize_typo"):
        load_config(cfg, env_file=env)


def test_repo_config_yaml_is_valid() -> None:
    root = Path(__file__).resolve().parents[2]

    config = load_config(root / "config.yaml", env_file=None)

    assert config.embeddings.dim == 384


def test_secrets_key_in_yaml_is_rejected(tmp_path: Path) -> None:
    cfg, env = _write(tmp_path, MINIMAL_YAML + "secrets: {}\n")

    with pytest.raises(ValueError, match=r"secrets belong in \.env"):
        load_config(cfg, env_file=env)


def test_non_mapping_yaml_is_rejected(tmp_path: Path) -> None:
    cfg, env = _write(tmp_path, "[]\n")

    with pytest.raises(ValueError, match="top level must be a mapping"):
        load_config(cfg, env_file=env)


def test_synop_config_env_var_sets_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    cfg, env = _write(tmp_path, MINIMAL_YAML)
    monkeypatch.setenv("SYNOP_CONFIG", str(cfg))

    assert load_config(env_file=env).models.upper == "model-upper"
